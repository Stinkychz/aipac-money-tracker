"""Weekly check that the FEC source links on the page still open.

    python check_links.py

Reads the built-in snapshot in index.html, builds every FEC link the page shows, asks each one
whether it still answers, and prints the ones that don't. Exits 1 when any are broken, so the
GitHub run fails and GitHub emails the repository owner.
"""
import json, re, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PAGE = Path(__file__).with_name("index.html")
COMMITTEES = ("C00797670", "C00799031")


def source_links(candidates):
    """Every FEC page the site links to: the two committees and each candidate with a real FEC id."""
    urls = [f"https://www.fec.gov/data/committee/{c}/" for c in COMMITTEES]
    urls += [f"https://www.fec.gov/data/candidate/{c['id']}/"
             for c in candidates if re.match(r"^[HSP]\d", c["id"])]
    return urls


def find_broken(urls, status):
    """The (url, why) pairs whose status() is not a success. status(url) returns an HTTP code or raises."""
    bad = []
    for u in urls:
        try:
            code = status(u)
            if not 200 <= code < 400:
                bad.append((u, f"HTTP {code}"))
        except urllib.error.HTTPError as e:
            bad.append((u, f"HTTP {e.code}"))
        except Exception as e:
            bad.append((u, type(e).__name__))
    return bad


def http_status(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "election-money-tracker link check"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def main():
    m = re.search(r"/\*SNAPSHOT\*/(.*?)/\*END\*/", PAGE.read_text(encoding="utf-8"), flags=re.S)
    snap = json.loads(m.group(1)) if m and m.group(1) != "null" else None
    urls = source_links(snap["candidates"] if snap else [])
    chunks = [urls[i::4] for i in range(4)]
    with ThreadPoolExecutor(4) as ex:
        bad = [b for part in ex.map(lambda c: find_broken(c, http_status), chunks) for b in part]
    print(f"Checked {len(urls)} FEC links, {len(bad)} broken.")
    for u, why in sorted(bad):
        print(f"  {why}  {u}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
