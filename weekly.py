"""Weekly Update Email Preview: a private page summing up what changed in the site's data.

Compares the snapshot baked into index.html now with the newest one in git history that is at
least a week older, and writes out/weekly-preview.html (git-ignored, never published, never sent).
Run: python weekly.py
"""
import datetime
import html
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out" / "weekly-preview.html"
WEEK_MS = 7 * 24 * 3600 * 1000
KINDS = (("pac", "nPac", "AIPAC PAC gifts"), ("support", "nSupport", "Super PAC spending for"),
         ("oppose", "nOppose", "Super PAC spending against"))


def snapshot(page):
    m = re.search(r"/\*SNAPSHOT\*/(.*?)/\*END\*/", page, flags=re.S)
    return json.loads(m.group(1)) if m and m.group(1) != "null" else None


def pick_baseline(snaps, now_at, gap=WEEK_MS):
    """The newest snapshot taken at least `gap` before now_at, or None."""
    old = [s for s in snaps if s and s["at"] <= now_at - gap]
    return max(old, key=lambda s: s["at"]) if old else None


def total(c):
    return c["pac"] + c["support"] + c["oppose"]


def diff(old, new, top=5):
    was = {c["id"]: c for c in old["candidates"]}
    now = {c["id"]: c for c in new["candidates"]}
    records = None  # only when both snapshots count records; older ones did not
    if all("nPac" in c for c in old["candidates"]) and all("nPac" in c for c in new["candidates"]):
        records = {k: sum(c[n] for c in now.values()) - sum(c[n] for c in was.values()) for k, n, _ in KINDS}
    moves = []
    for cid, c in now.items():
        if cid in was and abs(total(c) - total(was[cid])) >= 0.01:
            moves.append({"c": c, "by": {k: c[k] - was[cid][k] for k, _, _ in KINDS},
                          "change": total(c) - total(was[cid])})
    moves.sort(key=lambda m: -abs(m["change"]))
    return {"from": old["at"], "to": new["at"], "records": records,
            "added": sorted((now[i] for i in now.keys() - was.keys()), key=lambda c: -total(c)),
            "dropped": sorted((was[i] for i in was.keys() - now.keys()), key=lambda c: -total(c)),
            "moves": moves[:top], "moved": len(moves),
            "totals": {k: (sum(c[k] for c in was.values()), sum(c[k] for c in now.values())) for k, _, _ in KINDS}}


def day(ms):
    d = datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc)
    return f"{d:%b} {d.day}, {d.year}"


def money(x, sign=False):
    s = f"${abs(x):,.0f}"
    return ("+" if x > 0 and sign else "-" if x < 0 else "") + s


def held(x):
    """A candidate's figure; below zero means more was refunded than given, so say so."""
    return money(x) + (" (net refund: more returned than given)" if x < 0 else "")


def who(c):
    seat = "President" if c["office"] == "P" else c["state"] + (
        " Senate" if c["office"] == "S" else "-" + c["district"] if c["district"] else "")
    return f"{html.escape(c['name'].title())} ({html.escape(c['party'])}, {html.escape(seat)})"


def render(d):
    quiet = not (d["moves"] or d["added"] or d["dropped"] or (d["records"] and any(d["records"].values())))
    parts = [f"<h1>What changed, {day(d['from'])} to {day(d['to'])}</h1>"]
    if quiet:
        parts.append("<p>No new filings changed the figures in this period.</p>")
    else:
        if d["records"]:
            rows = "".join(f"<li>{label}: {n:+,} records</li>" for (k, _, label), n in
                           ((kd, d["records"][kd[0]]) for kd in KINDS) if n)
            if rows:
                parts.append(f"<h2>New filed records</h2><ul>{rows}</ul>")
        if d["moves"]:
            top = max(abs(m["change"]) for m in d["moves"])
            items = "".join(
                f"<li><b>{who(m['c'])}</b> {money(m['change'], True)}"
                f"<span class='bar{' down' if m['change'] < 0 else ''}' aria-hidden=true "
                f"style='width:{max(2, round(100 * abs(m['change']) / top))}%'></span><span class=by>"
                + ", ".join(f"{label} {money(v, True)}" for (k, _, label), v in
                            ((kd, m['by'][kd[0]]) for kd in KINDS) if abs(v) >= 0.01)
                + "</span></li>" for m in d["moves"])
            more = f" (of {d['moved']} that changed)" if d["moved"] > len(d["moves"]) else ""
            parts.append(f"<h2>Biggest moves{more}</h2><ol>{items}</ol>")
        if d["added"]:
            items = "".join(f"<li>{who(c)} {held(total(c))}</li>" for c in d["added"])
            parts.append(f"<h2>New candidates</h2><ul>{items}</ul>")
        if d["dropped"]:
            items = "".join(f"<li>{who(c)}</li>" for c in d["dropped"])
            parts.append(f"<h2>No longer listed</h2><ul>{items}</ul>")
    rows = "".join(f"<tr><th>{label}</th><td>{money(a)}</td><td>{money(b)}</td>"
                   f"<td>{money(b - a, True) if abs(b - a) >= 0.5 else 'none'}</td></tr>"
                   for (k, _, label), (a, b) in ((kd, d["totals"][kd[0]]) for kd in KINDS))
    parts.append(f"<h2>Totals</h2><table><tr><th></th><td>{day(d['from'])[:-6]}</td><td>{day(d['to'])[:-6]}</td>"
                 f"<td>Change</td></tr>{rows}</table>")
    return ("<!doctype html><html lang=en><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'><title>Weekly update preview</title>"
            "<style>body{font:16px/1.5 system-ui,sans-serif;max-width:40rem;margin:0 auto;padding:1rem;color:#1a1a1a}"
            "h1{font-size:1.3rem}h2{font-size:1.05rem;margin-top:1.5rem}.note{background:#fff4d6;padding:.5rem .75rem}"
            ".bar{display:block;height:.5rem;background:#2457a6;margin:.2rem 0}.bar.down{background:#a64224}"
            ".by{color:#555;font-size:.9rem}li{margin:.4rem 0}table{border-collapse:collapse}td,th{padding:.25rem .75rem .25rem 0;text-align:left}"
            "td{font-variant-numeric:tabular-nums;white-space:nowrap}</style>"
            "<p class=note>Private preview. Nothing has been emailed to anyone.</p>"
            + "".join(parts) + "<p class=by>Source: FEC filings for AIPAC PAC and United Democracy Project, as baked into the site.</p></html>")


def history(repo=HERE):
    """Every snapshot index.html has had in git history (newest commit first)."""
    shas = subprocess.run(["git", "-C", str(repo), "log", "--format=%H", "--", "index.html"],
                          capture_output=True, text=True, check=True).stdout.split()
    for sha in shas:
        page = subprocess.run(["git", "-C", str(repo), "show", f"{sha}:index.html"],
                              capture_output=True, text=True, encoding="utf-8").stdout
        yield snapshot(page)


def main():
    new = snapshot((HERE / "index.html").read_text(encoding="utf-8"))
    old = pick_baseline(history(), new["at"])
    if old is None:
        raise SystemExit("No snapshot in git history is a week older than the current one.")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(render(diff(old, new)), encoding="utf-8")
    print(f"Wrote {OUT} ({day(old['at'])} to {day(new['at'])})")


if __name__ == "__main__":
    main()
