"""Bake a snapshot of FEC data into index.html, so the page works where it can't call the FEC
(a claude.ai page, a phone). Uses the FEC's bulk files, which need no API key.

    python build.py

Same numbers as the page's live mode: AIPAC PAC (C00797670) contributions to candidates
(pas2), and United Democracy Project (C00799031) independent expenditures for / against them.
"""
import csv, io, json, re, sys, time, urllib.request, zipfile
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
    if old and old.group(1) != "null" and json.loads(old.group(1))["candidates"] == out:
        print("No new filings; index.html unchanged.")
        return
    snap = {"at": int(time.time() * 1000), "source": "snapshot", "candidates": out}
    page, n = re.subn(r"/\*SNAPSHOT\*/.*?/\*END\*/", lambda m: "/*SNAPSHOT*/" + json.dumps(snap) + "/*END*/",
                      page, flags=re.S)
    if n != 1:
        sys.exit("index.html has no /*SNAPSHOT*/ ... /*END*/ marker")
    PAGE.write_text(page, encoding="utf-8")
    print(f"{len(out)} candidates, AIPAC PAC ${sum(c['pac'] for c in out):,.0f}, "
          f"super PAC for ${sum(c['support'] for c in out):,.0f}, against ${sum(c['oppose'] for c in out):,.0f}")


if __name__ == "__main__":
    main()
