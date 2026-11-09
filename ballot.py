"""Ballot-measure money totals from California Cal-Access rows (step 1 of docs/ballot-measures.md).

Pure functions on already-parsed rows (dicts keyed like the Cal-Access TSV columns), so they can be
tested on small made-up filings. Reading the 1.6 GB bulk file into these rows comes next.

    side_totals(covers, receipts, measure_committees) -> {"yes": {...}, "no": {...}}

covers: CVR_CAMPAIGN_DISCLOSURE rows (FILING_ID, AMEND_ID, FILER_ID).
receipts: RCPT_CD rows (FILING_ID, AMEND_ID, FORM_TYPE, REC_TYPE, ENTITY_CD, CTRIB_NAML, AMOUNT).
measure_committees: {filer_id: "yes" | "no"} for one measure, as recorded by the state.
"""
from collections import defaultdict


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
    sides = {s: {"total": 0.0, "count": 0, "donors": defaultdict(float), "viaCommittee": 0.0}
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
    return sides


def top_donors(side, n=10):
    return sorted(side["donors"].items(), key=lambda kv: -kv[1])[:n]
