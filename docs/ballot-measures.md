# Ballot Measure Money: the plan (a section of the Election Money Tracker)

Status: step 1 in progress (real download read Nov 9: no 2026 measure-to-committee map in the bulk data, committees must be matched from cover-page text, see backlog; ballot.py: yes/no totals, out-of-state total, top-3 share, and the streaming reader for the bulk zip, all tested; still to do: wire it to the real download, pick the Nov 2026 measures and check against the state's totals), nothing public. Hayden picked this idea on Nov 8, 2026 and on Nov 9, 2026 said to merge it into the Election Money Tracker site (no separate site). It was the folder `ballot-money`.

## What it is, in one paragraph
A public page that answers "who paid for the yes side and who paid for the no side?" for each
state ballot measure. Every measure gets one card: the yes total, the no total, the top donors on
each side, and how the vote came out. It is built only from public campaign filings, with a link
to the filing behind every number, the same way the AIPAC Money Tracker (folder `election-money-tracker`) does it for candidates.

## Words you need
- **Ballot measure**: a law or change that voters decide directly, like "Proposition 50".
- **Committee**: the group that raises money for one side. The state records which side each
  committee is on, and who gave it money.
- **Filing**: the public report a committee sends the state, listing every donor above a set amount.

## Where it lives
A new "Ballot measures" view on the Election Money Tracker site, next to the candidate table, with the same look and the same Download CSV and data-as-of habits. The tracker reads the federal FEC; this view reads each state's own filings (state filings are in different formats), so it needs its own data reader inside `build.py`, baked into the page like the FEC data.

## Fairness rules (the most important part)
- Only numbers from official filings, each with a link to the filing and a "data as of" date.
- Yes and no always side by side, same size, same colors on every measure. No adjectives about
  either side, and no "good" or "bad" donors.
- Money passed through another committee is shown as passed through ("via Committee X"), and
  never counted twice.
- Nothing goes public until Hayden has seen it, and the site gets a "report a mistake" link.

## What a visitor sees
1. A list of the state's measures from the latest election: title in plain words, the result
   (passed or failed, and the vote share), and a yes-versus-no money bar with
   "Yes $X" and "No $Y" written on it, so it never relies on color alone.
2. Tap a measure: the top 10 donors on each side, how much of each side came from its top 3
   donors ("3 donors paid 81% of the yes side"), and how much came from out of state.
3. A Download CSV button, like the AIPAC Money Tracker has.

Plain words, works on a phone, light and dark.

## Where the numbers come from
- **First state: California** (card B1, my pick). It has the biggest measures, and its filing
  system, Cal-Access, posts a free bulk download of all filings that needs no account or key. I checked on
  Nov 8, 2026: it is live (1.6 GB) and updated that day.
- **More states later**, one at a time, each from its own official filings. A state is added
  only when its data can be read reliably.
- The vote results come from the state's official results page, entered once per election.

## How it is built
- The tracker already builds with `build.py` (Python), so the reader goes there rather than a new Rust program: it downloads the state's filings,
  totals each side, and bakes the numbers into a single web page. The page needs no server and
  can be hosted for free, like the AIPAC Money Tracker.
- Tests on small made-up filings: a donor giving to both sides, money passed through, a corrected
  (amended) filing replacing an old one, and a measure with no money on one side.
- Before anything is public, I check the big totals against the state's own published totals.

## Steps
1. Read California's filings and total the yes and no money for the Nov 2026 measures, with tests
   and a check against the state's totals (about 1 to 2 sessions).
2. The page: measure list, measure detail, CSV, phone screenshots for Hayden (about 1 session).
3. Hayden's OK, then push to the tracker's existing site (only with his OK).
4. Later: more states, one at a time.
