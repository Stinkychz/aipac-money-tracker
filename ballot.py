"""Ballot-measure money totals from California Cal-Access rows (step 1 of docs/ballot-measures.md).

Pure functions on already-parsed rows (dicts keyed like the Cal-Access TSV columns), so they can be
tested on small made-up filings. read_rows / read_zip_table stream the 1.6 GB bulk file into these rows.

    side_totals(covers, receipts, measure_committees) -> {"yes": {...}, "no": {...}}

covers: CVR_CAMPAIGN_DISCLOSURE rows (FILING_ID, AMEND_ID, FILER_ID).
receipts: RCPT_CD rows (FILING_ID, AMEND_ID, FORM_TYPE, REC_TYPE, ENTITY_CD, CTRIB_NAML, AMOUNT).
measure_committees: {filer_id: "yes" | "no"} for one measure, as recorded by the state.
"""
import csv
import io
import zipfile
from collections import defaultdict

csv.field_size_limit(1 << 24)

# The statewide measures on the Nov 3, 2026 California ballot, copied Nov 12, 2026 from
# https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures
MEASURES_2026 = {
    1: "Authorizes Bonds for Housing Affordability Programs",
    2: "Increases State's Rainy Day Fund",
    3: "Provides Permanent Funding for Schools and Health Care by Extending Existing Tax on High Incomes",
    4: "Repeals Prohibition Against Public Funding of Election Campaigns",
    5: "Changes Recall Election Process for Statewide Officers",
    37: "Creates Loan Program for Middle-Income Buyers of Qualified New Homes",
    38: "Authorizes Bonds for Immunology Medical Research",
    39: "Prohibits Citizens from Voting Unless They Present Government-Issued Identification",
    40: "Imposes One-Time Tax on Certain Taxpayers",
    41: "Prohibits New State Taxes That Exclude Revenues from State Spending Limit",
    42: "Prohibits New State Personal Property Taxes and Certain Retroactive State Taxes",
    43: "Limits Voters' Ability to Raise Revenues for Local Government Services",
    44: "Requires Community Health Clinics Spend 90% Of Revenue on Program Services",
    45: "Modifies Environmental Review for Certain Projects",
}
ELECTION_2026 = "2026-11-03"


def match_cover(cover):
    """Which 2026 measure and side a committee cover page is for: (number, "yes"|"no") or None.

    Needs the 2026 election date on the cover, a BAL_NUM that is an official 2026 number and a
    SUP_OPP_CD of S or O. Anything else (older elections, no number, odd side) is left out to be
    reviewed by hand rather than guessed."""
    if not str(cover.get("ELECT_DATE", "")).startswith(ELECTION_2026):
        return None
    num = "".join(ch for ch in str(cover.get("BAL_NUM", "")) if ch.isdigit())
    side = {"S": "yes", "O": "no"}.get(str(cover.get("SUP_OPP_CD", "")).strip().upper())
    if not num or side is None or int(num) not in MEASURES_2026:
        return None
    return int(num), side


def read_rows(f, wanted=None):
    """Stream rows of a Cal-Access TSV (text file object) as dicts. Quoted fields may contain tabs,
    blank lines are skipped, short rows are padded with "". `wanted` keeps only those columns."""
    reader = csv.reader(f, delimiter="	", quotechar='"')
    header = next(reader, None)
    if not header:
        return
    keep = [(i, h) for i, h in enumerate(header) if wanted is None or h in wanted]
    for row in reader:
        if not row:
            continue
        yield {h: (row[i] if i < len(row) else "") for i, h in keep}


def read_zip_table(zip_path, member, wanted=None):
    """Stream one table out of the bulk zip without unpacking it to disk."""
    with zipfile.ZipFile(zip_path) as z, z.open(member) as raw:
        yield from read_rows(io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""), wanted)


def latest_amendments(covers):
    """Keep only the newest version (highest AMEND_ID) of each filing: an amended filing replaces
    the old one, it does not add to it. Returns {filing_id: (amend_id, filer_id)}."""
    best = {}
    for c in covers:
        fid, amend = c["FILING_ID"], int(c["AMEND_ID"] or 0)
        if fid not in best or amend > best[fid][0]:
            best[fid] = (amend, c["FILER_ID"])
    return best


def side_totals(covers, receipts, measure_committees):
    latest = latest_amendments(covers)
    sides = {s: {"total": 0.0, "count": 0, "donors": defaultdict(float), "viaCommittee": 0.0, "outOfState": 0.0}
             for s in ("yes", "no")}
    for r in receipts:
        fid = r["FILING_ID"]
        if fid not in latest or int(r["AMEND_ID"] or 0) != latest[fid][0]:
            continue  # row belongs to a replaced (older) version of the filing
        if r.get("REC_TYPE") != "RCPT" or r.get("FORM_TYPE") != "A":
            continue  # only itemized money received (schedule A)
        side = measure_committees.get(latest[fid][1])
        if side is None:
            continue
        if r.get("CTRIB_NAML") in ("", None):
            continue
        amount = float(r["AMOUNT"] or 0)
        # Money from another committee of the same measure is a transfer between its own
        # committees: show it as passed through, never add it to the side's total twice.
        if r.get("CMTE_ID") and r["CMTE_ID"] in measure_committees:
            sides[side]["viaCommittee"] += amount
            continue
        s = sides[side]
        s["total"] += amount
        s["count"] += 1
        s["donors"][r["CTRIB_NAML"]] += amount
        if r.get("CTRIB_ST") and r["CTRIB_ST"] != "CA":
            s["outOfState"] += amount
    return sides


def top_donors(side, n=10):
    return sorted(side["donors"].items(), key=lambda kv: -kv[1])[:n]


def top_share(side, n=3):
    """Share (0 to 1) of a side's money that came from its n biggest donors; 0 for an empty side."""
    if not side["total"]:
        return 0.0
    return sum(a for _, a in top_donors(side, n)) / side["total"]
