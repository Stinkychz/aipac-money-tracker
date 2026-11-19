"""Bake a snapshot of FEC data into index.html, so the page works where it can't call the FEC
(a claude.ai page, a phone). Uses the FEC's bulk files, which need no API key.

    python build.py

Same numbers as the page's live mode: AIPAC PAC (C00797670) contributions to candidates
(pas2), and United Democracy Project (C00799031) independent expenditures for / against them.
Also each tracked race's top two fundraisers by total money raised (weball, the all-candidates summary).
And each tracked candidate's money from individuals split at $200 into small and big gifts (weball plus the
FEC totals API's itemized figure).
"""
import csv, datetime, io, json, os, re, sys, time, urllib.request, zipfile
from collections import defaultdict
from pathlib import Path

CYCLE = 2026
AIPAC_PAC, UDP = "C00797670", "C00799031"
BULK = "https://www.fec.gov/files/bulk-downloads"
PAGE = Path(__file__).with_name("index.html")


def get(path):
    with urllib.request.urlopen(f"{BULK}/{path}", timeout=120) as r:
        return r.read()


def unzip_lines(path):
    with zipfile.ZipFile(io.BytesIO(get(path))) as z:
        return z.read(z.namelist()[0]).decode("latin-1").splitlines()


def party(p):
    p = (p or "").upper()
    return "DEM" if p.startswith("DEM") else "REP" if p.startswith("REP") else p[:3] or "?"


def count_changed(old, new):
    """How many candidates are new, gone or have different figures between two candidate lists."""
    a = {c["id"]: c for c in old or []}
    b = {c["id"]: c for c in new}
    return sum(1 for k in a.keys() | b.keys() if a.get(k) != b.get(k))


def next_log(old_log, at, changed, keep=10):
    """The refresh log with this refresh added on top, newest first, at most `keep` entries."""
    return ([{"at": at, "changed": changed}] + list(old_log or []))[:keep]


def filing_dates(rows):
    """Due dates of the reports a monthly filer owes (monthly and year-end), oldest first, no repeats.
    `rows` are FEC /reporting-dates/ results."""
    seen = {}
    for r in rows:
        t = r.get("report_type") or ""
        if (re.fullmatch(r"M\d{1,2}", t) or t == "YE") and r.get("report_type_full"):
            seen[r["due_date"]] = r["report_type_full"].title()
    return [{"due": d, "name": seen[d]} for d in sorted(seen)]


def race_key(office, state, district):
    """One race: a House seat (H-CA-14), a state's Senate seat (S-AK) or the presidency (P)."""
    return "P" if office == "P" else f"S-{state}" if office == "S" else f"H-{state}-{district}"


def top_raisers(lines, races, n=2):
    """The `n` candidates who raised the most in each of `races`, from the FEC's all-candidates summary
    (weball, one `|` row per candidate: id, name, ..., party 4, total receipts 5, state 18, district 19,
    coverage end 27). Candidates who raised nothing are left out."""
    by_race = defaultdict(list)
    for line in lines:
        f = line.split("|")
        if len(f) < 28 or not f[0]:
            continue
        key = race_key(f[0][0], f[18], f[19])
        raised = float(f[5] or 0)
        if key in races and raised > 0:
            by_race[key].append({"id": f[0], "name": f[1], "party": party(f[4]), "raised": round(raised, 2),
                                 "through": f[27]})
    return {k: sorted(v, key=lambda c: (-c["raised"], c["id"]))[:n] for k, v in sorted(by_race.items())}


def small_big(lines, itemized):
    """Each candidate's money from individuals split at the FEC's own $200 line: `big` is gifts over $200
    (itemized, listed by name), `small` the rest (total from individuals, weball column 17, minus itemized).
    `itemized` maps candidate id to (itemized total, coverage end YYYY-MM-DD) from the FEC totals API.
    A candidate is left out when the two sources cover different periods or the numbers don't add up."""
    out = {}
    for line in lines:
        f = line.split("|")
        if len(f) < 28 or f[0] not in itemized:
            continue
        big, end = itemized[f[0]]
        try:
            m, d, y = f[27].split("/")
            same = f"{y}-{int(m):02}-{int(d):02}" == end
        except ValueError:
            same = False
        total = float(f[17] or 0)
        if same and total > 0 and 0 <= big <= total:
            out[f[0]] = {"small": round(total - big, 2), "big": round(big, 2), "through": f[27]}
    return dict(sorted(out.items()))


def fetch_itemized(ids, chunk=50):
    """Itemized individual gifts (over $200) and coverage end for each candidate id, this cycle's two years,
    from the FEC totals API (key from env FEC_API_KEY, else DEMO_KEY)."""
    key = os.environ.get("FEC_API_KEY") or "DEMO_KEY"
    ids, got = sorted(ids), {}
    for i in range(0, len(ids), chunk):
        url = (f"https://api.open.fec.gov/v1/candidates/totals/?api_key={key}&per_page=100&cycle={CYCLE}"
               f"&election_full=false&" + "&".join(f"candidate_id={c}" for c in ids[i:i + chunk]))
        with urllib.request.urlopen(url, timeout=60) as r:
            for row in json.load(r)["results"]:
                if row.get("individual_itemized_contributions") is not None and row.get("coverage_end_date"):
                    got[row["candidate_id"]] = (float(row["individual_itemized_contributions"]),
                                                row["coverage_end_date"][:10])
    return got


def fetch_filing_dates(today):
    """Upcoming monthly-filer due dates from the FEC calendar (public endpoint; key from env FEC_API_KEY, else the shared DEMO_KEY)."""
    key = os.environ.get("FEC_API_KEY") or "DEMO_KEY"
    rows, page = [], 1
    while True:
        url = (f"https://api.open.fec.gov/v1/reporting-dates/?api_key={key}&per_page=100&sort=due_date"
               f"&report_year={today.year}&report_year={today.year + 1}&page={page}")
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.load(r)
        rows += data["results"]
        if page >= data["pagination"]["pages"]:
            break
        page += 1
    return [d for d in filing_dates(rows) if d["due"] >= today.isoformat()]


def main():
    yy = str(CYCLE)[2:]
    cands = defaultdict(lambda: {"pac": 0.0, "support": 0.0, "oppose": 0.0,
                                    "nPac": 0, "nSupport": 0, "nOppose": 0})

    # Candidate names and races; later cycles first so the newest record wins.
    info = {}
    for y in (CYCLE + 2, CYCLE, CYCLE - 2, CYCLE - 4):
        try:
            lines = unzip_lines(f"{y}/cn{str(y)[2:]}.zip")
        except Exception:
            continue
        for line in lines:
            f = line.split("|")
            info.setdefault(f[0], {"name": f[1], "party": party(f[2]), "office": f[5],
                                   "state": f[4], "district": f[6]})

    for line in unzip_lines(f"{CYCLE}/pas2{yy}.zip"):
        f = line.split("|")
        if f[0] == AIPAC_PAC and f[16] and f[19] != "X":
            cands[f[16]]["pac"] += float(f[14])
            cands[f[16]]["nPac"] += 1

    seen = {}
    text = get(f"{CYCLE}/independent_expenditure_{CYCLE}.csv").decode("latin-1")
    for r in csv.DictReader(io.StringIO(text)):
        if r["spe_id"] != UDP or not r["cand_id"]:
            continue
        key = r["tran_id"]  # an amendment repeats the transaction: keep the latest filing
        if key in seen and int(seen[key]["file_num"] or 0) >= int(r["file_num"] or 0):
            continue
        seen[key] = r
    for r in seen.values():
        c = cands[r["cand_id"]]
        kind = "support" if r["sup_opp"] == "S" else "oppose"
        c[kind] += float(r["exp_amo"] or 0)
        c["n" + kind.capitalize()] += 1
        info.setdefault(r["cand_id"], {"name": r["cand_name"], "party": party(r["cand_pty_aff"]),
                                       "office": r["can_office"], "state": r["can_office_state"],
                                       "district": r["can_office_dis"]})

    out = []
    for cid, money in cands.items():
        i = info.get(cid, {"name": cid, "party": "?", "office": cid[0], "state": cid[2:4], "district": ""})
        out.append({"id": cid, **i, **{k: round(v, 2) if isinstance(v, float) else v for k, v in money.items()}})

    out.sort(key=lambda c: c["id"])
    page = PAGE.read_text(encoding="utf-8")
    old = re.search(r"/\*SNAPSHOT\*/(.*?)/\*END\*/", page, flags=re.S)
    prev = json.loads(old.group(1)) if old and old.group(1) != "null" else None
    weball = None
    try:  # each tracked race's top two fundraisers; if the file is down, keep the ones already in the page
        weball = unzip_lines(f"{CYCLE}/weball{yy}.zip")
        races = top_raisers(weball, {race_key(c["office"], c["state"], c["district"]) for c in out})
    except Exception as e:
        print("FEC candidate totals not read:", e)
        races = (prev or {}).get("races", {})
    try:  # small vs big gifts for each tracked candidate; if either source is down, keep the page's
        donor_size = small_big(weball, fetch_itemized({c["id"] for c in out})) if weball else None
    except Exception as e:
        print("FEC itemized totals not read:", e)
        donor_size = None
    if donor_size is None:
        donor_size = (prev or {}).get("donorSize", {})
    try:  # the next-filing note; if the FEC calendar is down, keep the dates already in the page
        due = fetch_filing_dates(datetime.date.today())
        page = re.sub(r"/\*DUE\*/.*?/\*END\*/", lambda m: "/*DUE*/" + json.dumps(due) + "/*END*/", page, flags=re.S)
    except Exception as e:
        print("FEC filing calendar not read:", e)
    if prev and prev["candidates"] == out and prev.get("races") == races and prev.get("donorSize") == donor_size:
        if page != PAGE.read_text(encoding="utf-8"):
            PAGE.write_text(page, encoding="utf-8")
        print("No new filings.")
        return
    at = int(time.time() * 1000)
    changed = count_changed(prev and prev["candidates"], out)
    snap = {"at": at, "source": "snapshot", "candidates": out, "races": races,
            "donorSize": donor_size, "log": next_log(prev and prev.get("log"), at, changed)}
    page, n = re.subn(r"/\*SNAPSHOT\*/.*?/\*END\*/", lambda m: "/*SNAPSHOT*/" + json.dumps(snap) + "/*END*/",
                      page, flags=re.S)
    if n != 1:
        sys.exit("index.html has no /*SNAPSHOT*/ ... /*END*/ marker")
    PAGE.write_text(page, encoding="utf-8")
    print(f"{len(out)} candidates, AIPAC PAC ${sum(c['pac'] for c in out):,.0f}, "
          f"super PAC for ${sum(c['support'] for c in out):,.0f}, against ${sum(c['oppose'] for c in out):,.0f}")


if __name__ == "__main__":
    main()
