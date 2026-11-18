"""Ballot-measure money totals from California Cal-Access rows (step 1 of docs/ballot-measures.md).

Pure functions on already-parsed rows (dicts keyed like the Cal-Access TSV columns), so they can be
tested on small made-up filings. read_rows / read_zip_table stream the 1.6 GB bulk file into these rows.

    side_totals(covers, receipts, measure_committees) -> {"yes": {...}, "no": {...}}

covers: CVR_CAMPAIGN_DISCLOSURE rows (FILING_ID, AMEND_ID, FILER_ID).
receipts: RCPT_CD rows (FILING_ID, AMEND_ID, FORM_TYPE, REC_TYPE, ENTITY_CD, CTRIB_NAML, AMOUNT).
measure_committees: {filer_id: "yes" | "no"} for one measure, as recorded by the state.
"""
import csv
import datetime
import io
import re
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


def _date_parts(text):
    """(year, month, day) from "2026-11-03" or the state's "11/3/2026 " style, else None.

    Strict: only those two styles, a four-digit year and a real calendar day. Anything else
    ("2026/11/03", "13/45/2026", "Nov 3 2024") is None, never a guess."""
    t = str(text).strip().split(" ")[0]
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        y, mo, d = m.groups()
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
        if not m:
            return None
        mo, d, y = m.groups()
    try:
        datetime.date(int(y), int(mo), int(d))
    except ValueError:
        return None
    return int(y), int(mo), int(d)


# Seen once on the real Cal-Access zip (Nov 17): RPT_DATE '000', a junk placeholder, not a date style.
PLACEHOLDER_DATES = frozenset({"000"})


def unreadable_dates(covers):
    """Every non-blank ELECT_DATE / RPT_DATE on a cover that _date_parts cannot read, as sorted
    (field, text) pairs. The ballot build must stop on a non-empty list rather than drop or guess."""
    bad = set()
    for cover in covers:
        for field in ("ELECT_DATE", "RPT_DATE"):
            text = str(cover.get(field, "")).strip()
            if text and text not in PLACEHOLDER_DATES and _date_parts(text) is None:
                bad.add((field, text))
    return sorted(bad)


def check_dates(covers):
    """Raise ValueError naming the unreadable dates, so a new date style is looked at before publishing."""
    bad = unreadable_dates(covers)
    if bad:
        shown = ", ".join(f"{f}={t!r}" for f, t in bad[:10])
        raise ValueError(f"{len(bad)} unreadable cover date(s), review before publishing: {shown}")


def _is_2026_ballot(cover):
    """The cover's election date is Nov 3, 2026. Many real covers leave ELECT_DATE blank; for those
    the report date must fall in 2026 (the measure numbers were reused in 2024 and 2025). A
    non-blank election date that cannot be read is never replaced by the report date."""
    raw = str(cover.get("ELECT_DATE", "")).strip()
    elect = _date_parts(raw)
    if elect:
        return elect == (2026, 11, 3)
    if raw:
        return False
    rpt = _date_parts(cover.get("RPT_DATE", ""))
    return bool(rpt) and rpt[0] == 2026


def _alnum(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


# Initiative file numbers (Attorney General's list) matched to Nov 2026 measures by title, not stated
# by any official page. Prop 39 (25-0007A1) is left out: its match is by subject only.
INITIATIVE_NUMBERS = {"25-0016": 3, "25-0013": 37, "25-0026": 38, "25-0024": 40, "25-0040": 41,
                      "25-0041": 42, "25-0008": 44, "25-0023": 45}


def _measure_from_name(name):
    """Measure number named in a cover's free-text BAL_NAME, or None. Two sure signs only: the
    official title (its first words) or "Prop(osition) N" with N from 37 up (1 to 5 were also
    2024 and older numbers, so those need a BAL_NUM)."""
    text = _alnum(name)
    for num, title in MEASURES_2026.items():
        if _alnum(title)[:45] in text:
            return num
    for init in re.findall(r"\b25 (\d{4})", text):
        if "25-" + init in INITIATIVE_NUMBERS:
            return INITIATIVE_NUMBERS["25-" + init]
    m = re.search(r"\bprop(?:osition)?\b[ :]*(\d+)", text)
    if m and int(m.group(1)) >= 37 and int(m.group(1)) in MEASURES_2026:
        return int(m.group(1))
    return None


def match_cover(cover):
    """Which 2026 measure and side a committee cover page is for: (number, "yes"|"no") or None.

    Needs the 2026 election date on the cover (or, if blank, a 2026 report date), a BAL_NUM that is an official 2026 number and a
    SUP_OPP_CD of S or O. Anything else (older elections, no number, odd side) is left out to be
    reviewed by hand rather than guessed."""
    if not _is_2026_ballot(cover):
        return None
    num = "".join(ch for ch in str(cover.get("BAL_NUM", "")) if ch.isdigit())
    side = {"S": "yes", "O": "no"}.get(str(cover.get("SUP_OPP_CD", "")).strip().upper())
    if side is None:
        return None
    if not num:
        found = _measure_from_name(cover.get("BAL_NAME", ""))
        return (found, side) if found else None
    if int(num) not in MEASURES_2026:
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


COVER_COLUMNS = {"FILING_ID", "AMEND_ID", "FILER_ID", "ELECT_DATE", "BAL_NUM", "BAL_NAME", "SUP_OPP_CD", "RPT_DATE"}
RECEIPT_COLUMNS = {"FILING_ID", "AMEND_ID", "REC_TYPE", "FORM_TYPE", "CTRIB_NAML", "AMOUNT", "CMTE_ID", "CTRIB_ST"}


def measure_totals(zip_path):
    """Yes/no totals for every 2026 measure straight from the bulk zip: {measure: side_totals(...)}.
    Stops (ValueError) on an unreadable cover date. Reads the covers once, then streams the 3.9 GB
    receipts table keeping only rows of matched filings, so memory stays small."""
    covers = list(read_zip_table(zip_path, "CalAccess/DATA/CVR_CAMPAIGN_DISCLOSURE_CD.TSV", COVER_COLUMNS))
    check_dates(covers)
    per, filings = defaultdict(dict), set()
    for c in covers:
        m = match_cover(c)
        if m:
            per[m[0]][c["FILER_ID"]] = m[1]
            filings.add(c["FILING_ID"])
    matched = [c for c in covers if c["FILING_ID"] in filings]
    receipts = [r for r in read_zip_table(zip_path, "CalAccess/DATA/RCPT_CD.TSV", RECEIPT_COLUMNS)
                if r["FILING_ID"] in filings]
    return {m: side_totals(matched, receipts, per[m]) for m in sorted(per)}
