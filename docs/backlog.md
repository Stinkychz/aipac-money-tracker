# Election Money Tracker: ideas to build

## Outside Money Map (Medium)

A map that shades each state by how much money from outside the state went into its races; tap a
state for the biggest donors. It builds on Look Up Your Own Representative and reads at a glance.
Hayden picked this idea on Nov 8, 2026.

## Data Freshness Badge (Small)

A small badge on every number saying how old it is and which public filing it came from. A visible
date and source keeps a politically sensitive site honest. Tapping any figure jumps straight to that
official filing (Hayden also picked this as "Source Link on Every Number"). Hayden picked this idea
on Nov 8, 2026.

First step shipped Nov 8: each of the four top figures shows its data-as-of date and links to the FEC
committee page it comes from. Second step shipped Nov 8: every nonzero table figure (PAC, super PAC for and against) links to its FEC page. Still to do: the same on charts once they exist.

## Plain-Words Explainer Per Donor (Small)

Each donor page gets a two-sentence summary in plain words of who they are and where their money went. A visitor should understand the site in ten seconds. Hayden picked this idea on Nov 8, 2026.

## Search Donors by Name (Small)

A search box where you type part of a donor's name, even misspelled, and jump straight to their page.
A data site is only useful if the thing you want is one search away. Hayden picked this idea on Nov 8, 2026.

## Weekly Update Email Preview (Small)

A private preview page of a short weekly summary of what changed on the site (new filings, new
candidates, biggest moves), so Hayden can judge it before anyone is ever emailed. Fresh filings
arrive all the time and a weekly summary gives visitors a reason to come back; nothing is sent
without Hayden's yes. Hayden picked this idea on Nov 8, 2026.

## Funding Month by Month (Small)

A simple line chart under each candidate's row showing their money month by month through the
race. A line tells the story of a race in one glance, next to the bar charts and the biggest-jump
list. Hayden picked this idea on Nov 8, 2026.

Waiting on Hayden (Nov 19): cards F1 (which money) and F2 (where it shows) in `docs/decisions.md`. Once answered, the build goes in `build.py` (a separate baked block kept out of `candidates`, also written on the "No new filings" path, like `DUE`) and `index.html`. Unverified: the date format of the pas2 transaction date and the expenditure CSV's `exp_date`; read real rows before parsing (curl gets an HTML page from fec.gov, so read them with Python's urllib as `build.py` does).

## Donors Who Back Both Sides (Medium)

A short list of donors who gave to candidates in opposing parties, with the amounts and a link to
each filing. Every claim needs proof, and a surprising fact like this is what makes a data site
worth sharing; the list states only what the filings show. Hayden picked this idea on Nov 8, 2026.

## Explain This Chart Button (Small)

A small button on every chart that tells you in one plain sentence what the chart shows and what
to notice. A visitor should understand the site in ten seconds. Every chart also gets a plain text
version of its numbers that a screen reader can read aloud, such as "Top donor: X, $50,000, 40% of
the total" (Hayden also picked this as "Screen Reader Friendly Charts"). Hayden picked this idea on
Nov 8, 2026.

## Top Donors in Plain Rankings (Small)

A simple top-ten list for any race, with each donor's total and the share of the race's money they
gave. A ranked list is the quickest thing a visitor can read and share. On each candidate's page
the top five are also drawn as bars so the size gap is obvious at a glance (Hayden also picked this
as "Top Donors Shown as a Bar Chart"). Hayden picked this idea on Nov 8, 2026.

## Small Donors vs Big Donors (Small)

One bar on any candidate's page showing how much of their money came from ordinary small
donations and how much from large ones. It answers who a candidate really depends on in one
glance, and the numbers come straight from the filings. Where the line between small and large
sits (federal filings itemize gifts over $200) is a swipe card for Hayden at build time. Hayden
picked this idea on Nov 8, 2026.

## Follow One Candidate (Medium)

Tap Follow on a candidate and get a short alert whenever a new large donation to them is filed. It
gives visitors a reason to come back and pairs with Look Up Your Own Representative. How the alert
reaches people (email, browser notification), what counts as "large" and how often one follower
can be alerted are swipe cards for Hayden at build time; alerts stay off until Hayden says yes. Hayden picked this idea on
Nov 8, 2026.

## Money Spent Against Candidates (Medium)

For each candidate, how much outside groups spent on ads and mailers attacking them, and which
groups paid for it, straight from the spending reports those groups file with the FEC. It builds on
the donor pages and the Outside Money Map, and shows who is paying to sink each candidate. Hayden
picked this idea on Nov 8, 2026.

## Download the Raw Numbers (Small)

First step shipped Nov 8: a "Download CSV" button saves the table rows currently shown, each with
its FEC candidate page, the two committee filing pages and a data-as-of date. Per-chart buttons wait
until charts exist.

A button on every chart that downloads the exact numbers behind it as a spreadsheet (a CSV file, which opens in Excel), with the
public filing each number came from named next to it. Every claim needs proof, and letting
visitors check the numbers themselves builds trust; it pairs with the Data Freshness Badge and the
Explain This Chart Button. Hayden picked this idea on Nov 8, 2026.

## Ask a Question in Plain Words (Medium)

Type a question like "who gave the most to this candidate?" and get a short answer with a link to
the filing it came from. A visitor should get what they want in ten seconds, and every answer
comes with its proof. It answers only from the site's own filing data and says so when it can't
answer. Hayden picked this idea on Nov 8, 2026.

## Embed Charts on Other Sites (Medium)

A copy-and-paste snippet that lets a blogger or local reporter put any of the site's funding charts
on their own page, with the source shown under it. Local reporters and bloggers already write about
these races, and a live chart keeps the numbers current on their page and points readers back here.
Hayden picked this idea on Nov 8, 2026.

## Money by Industry (Medium)

A candidate's donors grouped by industry, such as energy, banks or health, with each group's share
shown as a simple bar. A list of names means little, but a few bars answer who is paying in about
ten seconds. The industry list comes from the job and employer each donor lists in their filing;
which grouping to use is a swipe card for Hayden at build time. Hayden picked this idea on Nov 8,
2026.

## Biggest Jump This Month (Small)

A short list of the candidates whose funding grew fastest this month, each with a tiny line chart.
A moving number gives visitors a reason to come back, and it shares its data with Funding Month by
Month. Hayden picked this idea on Nov 8, 2026.

## One Donor, Many Spellings (Medium)

Joins donors who appear under slightly different names, such as Acme Inc and ACME Incorporated, so
their totals are counted together. Split names quietly make the biggest donors look smaller than
they are. Every join keeps the original spellings and filings visible, so anyone can check it, and
it makes Search Donors by Name and every top-donor list more accurate. Hayden picked this idea on
Nov 8, 2026.

## Missing Filing Flags (Small)

A small flag on any campaign that is late or missing a required money report, with the due date
and a link to the official FEC record. A gap in the paperwork is a fact anyone can check; the flag
states only what the FEC's own calendar and records show. Hayden picked this idea on Nov 8, 2026.

## Report a Mistake Button (Small)

A small button on every page lets a visitor flag a number they think is wrong, and each report
lands in a private list with the page, the number and the filing it came from. On a politically
sensitive site, fixing errors fast is how you keep trust. The site is a single static page, so
where reports are stored (a GitHub issue form, a free form service or a small server) is a swipe
card for Hayden at build time, and nothing goes live until he says yes. Hayden picked this idea on
Nov 8, 2026.

## Next Filing Countdown (Small)

A small note saying when the next official FEC filing is due and which numbers will change when it
arrives. Visitors trust a data site more when they know when it updates; the dates come only from
the FEC's own filing calendar, and it shares that data with Missing Filing Flags and the Data
Freshness Badge. Hayden picked this idea on Nov 8, 2026.

Done Nov 16: the Refresh FEC data run (c9295f8) filled `DUE` with the real FEC calendar (Nov 20, Dec 20, Jan 31), so the "Next filing due" line now shows on the page; build.py tests pass. No screenshot: Hayden said skip (Nov 16), so it is marked done on the passing tests and filled dates alone.

## Plain Words for Money Terms (Small)

Shipped Nov 16 (first step): a "Money terms in plain words" fold-out under the table with PAC, super PAC, independent expenditure and earmarked contribution, each with an FEC link (all checked 200). Not yet seen on a screenshot (headless Edge made none). Left: tap-a-term inline popups, and itemized donation / bundler once those words appear on the page. Wording is Hayden's to read.

Tap a term such as super PAC, bundler or itemized donation anywhere on the site and get a
one-sentence explanation in plain words. A visitor should understand the site in ten seconds, and
it pairs with the Plain-Words Explainer Per Donor and the Explain This Chart Button. Each
explanation is neutral and links to the FEC's own definition. Hayden picked this idea on Nov 8,
2026.

## Spanish Version of the Site (Medium)

A switch at the top that shows every page, label and explanation in Spanish, with the same numbers
and sources. A data site is only useful to people who can read it, and the plain-words explainers
are already part of the plan. Names, dollar figures and FEC links stay exactly as filed; only the
words around them change. Who checks the Spanish wording before it goes live is a swipe card for
Hayden at build time. Hayden picked this idea on Nov 8, 2026.

## Biggest Gap Between Rivals (Small)

For any race, one line says how far apart the two top candidates are in money raised, with a small
bar showing the gap. It gives a visitor the key fact about a race in a few seconds, and both totals
link to their filings. It needs each candidate's total money raised from the FEC, not just the
AIPAC money the site tracks today. Hayden picked this idea on Nov 8, 2026.

## Which Way Each Industry Leans (Medium)

For each industry, a two-color bar showing how its donations split between the parties, with a link
to the filings behind it. It answers a visitor's next question after Money by Industry, so it comes
after that and uses the same industry grouping. Each side's percentage is written on the bar, so it
never relies on color alone. Hayden picked this idea on Nov 8, 2026.

## Ballot Measures in Plain Words (Small)

Each ballot measure gets a two-sentence summary of what a yes and a no would change, shown next to
who funds each side. Voters need both before they vote. It builds on the Ballot Measure Money
Tracker, so it comes after that. Every summary is neutral, links to
the official measure text, and Hayden reads it before it goes live. Hayden picked this idea on Nov 8,
2026.

## Stale Figures Turn Amber (Small, after the hourly refresh)

If a number's as-of date gets too old, its Data Freshness Badge turns amber and says how many days
behind it is. It comes after the hourly refresh goes live, since until then every figure ages the
same way. Hayden still picks how many days counts as stale and the exact wording before it is built.
Hayden picked this idea on Nov 8, 2026.

## Hourly Refresh Switch On Phone (Small)

Note Nov 9: the hourly refresh is already ON (GitHub Action `refresh.yml`), so this is now only an off/on switch. Needs a GitHub token from Hayden (fine-grained, Actions write on this repo) saved on the HQ hub before it can be built.

A single switch on your phone turns the hourly money data refresh on or off, with the last refresh time beside it. The hourly data refresh went live on Nov 9 (workflow "Refresh FEC data", .github/workflows/refresh.yml, active), so this switch would enable/disable that workflow from the phone through a new HQ hub endpoint (hq/hub). Not built: it needs a new hub endpoint and phone screen plus GitHub sign-in on the hub; taken up by the next step. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Ballot Measure Money View (Large)

A "Ballot measures" view on this site: for each California measure on the Nov 2026 ballot, the yes
total, the no total, the top donors on each side and the result, from Cal-Access filings, with a
link to the filing behind every number. Yes and no are always side by side, same size, no adjectives.
Hayden picked this idea on Nov 8, 2026 and said on Nov 9, 2026 to merge it into this site. The full
plan, fairness rules and steps are in [ballot-measures.md](ballot-measures.md). Nothing goes public
until Hayden has seen it. This also holds the older "Ballot Measure Money Tracker" idea (Medium, picked
Nov 8, 2026: who is paying for and against each ballot measure, with the amounts and a link to each
filing). Ballot measure money is filed with each state, not the FEC, so if more states than
California are added later, which states to start with is a swipe card for Hayden at that time.

Progress Nov 9: step 1 code done and tested in ballot.py (totals, out-of-state, top-3 share, bulk-zip reader). Left: run it on the real Cal-Access download, map the Nov 2026 measures to their committees, check against the state's totals, then the page (step 2).

Progress Nov 9 (later): downloaded the real Cal-Access zip (1.6 GB, kept at %TEMP%\calaccess\dbwebexport.zip) and read it. Finding: `BALLOT_MEASURES_CD.TSV` is stale (110 rows, last election 2000), so the state's bulk data has NO measure-to-committee map for 2026. The only link is each committee's cover page (`CVR_CAMPAIGN_DISCLOSURE_CD`: BAL_NAME, BAL_NUM, SUP_OPP_CD S/O, filed with free text), and it is messy: the same measure appears as 'Prop 39', 'PROPOSITION 39', 'Initiative 25-0022' with no number, and numbers 1-4, 39-45, 50 mix Nov 2024, 2025 and 2026 filings. Next: take the official Nov 2026 measure list and numbers from the Secretary of State, match committees by RPT_DATE/ELECT_DATE (2026-11-03) plus BAL_NAME text, list the matches for review, then run side_totals and compare with the state's published totals.

Progress Nov 12: official Nov 2026 list (Props 1-5 and 37-45, 14 measures, from sos.ca.gov) is now in ballot.py as MEASURES_2026, with match_cover(cover) turning a committee cover page (ELECT_DATE, BAL_NUM, SUP_OPP_CD) into (measure, yes/no); tested. Left: re-download the Cal-Access zip (the Nov 9 copy in %TEMP% is gone), run match_cover over CVR_CAMPAIGN_DISCLOSURE_CD, list unmatched 2026 covers for review, run side_totals per measure and compare with the state totals, then the page (step 2).

Progress Nov 15: re-downloaded the zip (kept at %TEMP%\emt-calaccess\dbwebexport.zip) and ran match_cover over the real CVR_CAMPAIGN_DISCLOSURE_CD. Fixed a bug: real ELECT_DATE looks like "11/3/2026 " (not 2026-11-03) and is often blank, so it matched nothing; now both date styles work and a blank date falls back to a 2026 RPT_DATE (tested). Result: all 14 measures now have committees (e.g. Prop 39: 14 yes, 18 no; Prop 44: 1 yes, 11 no). Still unmatched (208 covers): ones with no BAL_NUM, filed only with the measure's title or initiative number (e.g. "INITIATIVE 25-0022", "Requires New State Taxes..."). Left: match those by title text (MEASURES_2026 names) and review, run side_totals per measure (RCPT_CD table), compare with the state's published totals, then the page (step 2).

Progress Nov 16: ran side_totals on the real RCPT_CD for all 14 measures (script `%TEMP%\emt-side-totals.py`, output `%TEMP%\emt-side-totals.json`). Itemized yes/no dollars from the matched committees: Prop 1 yes 6.07M/no 0; 3 yes 61.7M/no 0; 37 yes 11.4M/no 0; 39 yes 8.97M (388 gifts)/no 30.3M (102); 40 no 119.2M; 41 yes 58.4M/no 0.95M; 42 yes 128.0M; 43 no 7.1M; 44 no 9.1M; 45 yes 31.4M/no 21.1M; Props 2 and 5 nothing found; Prop 38 no 8.5K, yes 0. Many measures show only one side, likely because the other side's covers carry no BAL_NUM (the 208 unmatched covers). Unverified: these figures are not yet checked against the state's published totals. Left: match the unmatched covers by title text, compare with the state's totals, then the page (step 2).

Progress Nov 16 (later): tried a first full read of the zip (covers + RCPT_CD) with a scratch script in the temp folder; it did not finish in 10 minutes and was stopped, so side_totals has not yet run on real data. Next: stream RCPT_CD without list() (keep only matched filers' FILING_IDs and needed columns), run it in the background with a 2-hour timeout, then compare with the state's totals. The heavy-run tool is at hq-heavy/tools/heavy.mjs (hq-live/tools/heavy.mjs no longer exists).

Progress Nov 16 (name match): match_cover now falls back to the cover's free-text BAL_NAME when BAL_NUM is blank: the measure's official title (first 45 characters) or "Prop(osition) N" for N 37 and up (1 to 5 need a BAL_NUM since those numbers were reused); tested. On the real zip, 8 more committees matched (2026 covers with a name but no match: 116 to 108 committees). Most of the rest name initiative numbers (25-0022, 25-0024) or other measures (Prop 50 is not on this ballot). Left: map initiative numbers to measures from the SoS list, re-run `%TEMP%\emt-side-totals.py` (it streams, so the earlier 10-minute run that held the whole table in memory is not the way), compare with the state's totals, then the page (step 2).

Progress Nov 17 (initiative numbers): matched 8 initiative file numbers to measures by title against the Attorney General's active-measures list (25-0016 Prop 3, 25-0013 Prop 37, 25-0026 Prop 38, 25-0024 Prop 40, 25-0040 Prop 41, 25-0041 Prop 42, 25-0008 Prop 44, 25-0023 Prop 45) and put them in `ballot.INITIATIVE_NUMBERS`; `match_cover` uses them when BAL_NUM is blank; tested (21 pass). Inferred: no official page states the link, it is by title. Prop 39 (25-0007A1) is by subject only so it is left out; Props 1, 2, 4, 5, 43 are legislative (no number); 25-0022 is not on this ballot. Left: re-run `%TEMP%\emt-side-totals.py` on the real zip, compare with the state's totals, then the page (step 2).

Progress Nov 19 (match check): listed every committee matched to Props 1 to 5 and 43 on the real zip. Props 4 and 43 are real 2026 committees (Prop 4 is SB 42 by Umberg, so "Umberg" was right; Prop 43 yes is the Howard Jarvis committee), not older-year ones. Fixed a counting bug: a committee's filing was credited to every measure that committee ever filed about; now each filing counts only for the measure on its own cover (tested, 22 ballot tests pass). Re-run on the real zip (`%TEMP%\emt-measure-totals.json`, 103 s): the only change is about $0.05M from "Citizens for a Just California - No on 39" no longer also counted under Prop 3 yes and Prop 45 no. Found one false match with no money in it: a 2024 school-bond Prop 2 committee (filer 1473035, blank election date, Jan 2026 report) matches 2026 Prop 2; harmless today, needs a rule if it ever has receipts. Props 2 and 5 have only F496 spending reports (no primarily-formed committee), so $0 raised is expected there. Left: compare with the state's own totals (Cal-Access measure pages), then the page (step 2, Hayden sees it first).

## Freeze the Final Numbers (Small)

After election day, each measure's money total is saved as a dated final snapshot that stops changing, so the page shows what was settled. The tracker just got its official Nov 2026 measure list, and late filings will keep moving those totals after the vote is over. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-12, so it goes ahead of unpicked items. Category: Want. Fable research (2026-11-12): good idea, with one change to when it freezes. Freezing on election day would lock in totals that miss the last weeks of spending: the FPPC 2026 schedule has committees report Oct 18 to Dec 31 in a statement due Feb 1, 2027, so mark totals "still being reported" after the vote, save the dated final snapshot in early Feb 2027 with its date shown and the copy kept in the repo, and build it after the Ballot Measure Money View page. If it defines the look, rules, names or new content, make an options card first.

## Unseen Date Format Alarm (Small)

When a state's filings use a date style the tracker has never seen, it flags the state for a look before any wrong date goes live. The ballot money fix just taught it to read one state's real date style and blank election dates, and other states will have their own surprises. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-16, so it goes ahead of unpicked items. Category: Want. Opus research (2026-11-16): good idea, but aim it at California now, not other states (only California is planned). A probe of `ballot._date_parts` showed it already guesses silently: "2026/11/03" reads as year 3, "13/45/2026" is accepted, and a cover with an unreadable election date ("Nov 3 2024") but a 2026 report date is counted as a 2026 measure; so make the reader strict (only the known styles, real months and days) and have the ballot build list any non-blank date it cannot read and stop before the page is published, instead of dropping or guessing. If it defines the look, rules, names or new content, make an options card first.

Done Nov 16 (first step): `ballot._date_parts` is now strict (only `YYYY-MM-DD` and `M/D/YYYY`, four-digit year, real calendar day), an unreadable non-blank ELECT_DATE is no longer rescued by the report date, and `unreadable_dates(covers)` / `check_dates(covers)` list or raise on any date it cannot read; tested (20 ballot tests pass). Left: call `check_dates` on the real covers in the ballot build (page step 2) and run it once on the real zip to see which styles exist.

Done Nov 17: ran `unreadable_dates` on the real zip's 727,105 covers (6 seconds): exactly one unreadable date, RPT_DATE `'000'` (a junk placeholder, not a date style); every other ELECT_DATE and RPT_DATE is `YYYY-MM-DD` or `M/D/YYYY`. Left: call `check_dates` in the ballot build (page step 2), treating `'000'` as blank (not a date, so no decision needed).

Done Nov 17 (later): `'000'` is now a known placeholder (`ballot.PLACEHOLDER_DATES`), skipped by the alarm; tested (21 ballot tests pass). Left for this item: call `check_dates` in the ballot build (page step 2).

Done Nov 18: `ballot.measure_totals(zip_path)` is the ballot build's data step: reads covers, calls `check_dates` (stops on an unreadable date), matches measures, streams `RCPT_CD.TSV` keeping only matched filings, returns each measure's yes/no totals; tested on a made-up zip (22 ballot tests pass). That finishes the alarm item. Left for Ballot Measure Money View: run `measure_totals` on the real zip via `heavy.mjs` (`%TEMP%\emt-calaccess\dbwebexport.zip`), compare with the state's totals, then the page (step 2, Hayden sees it before it goes public).

Done Nov 18 (real run): `ballot.measure_totals` ran on the real zip in 109 seconds (via `heavy.mjs`; output `%TEMP%\emt-measure-totals.json`). Itemized yes/no: Prop 1 yes 6.07M; 3 yes 61.7M; 4 yes 0.80M; 37 yes 22.1M; 38 no 8.5K; 39 yes 8.97M / no 30.3M; 40 no 129.8M; 41 yes 58.4M / no 0.70M; 42 yes 127.95M; 43 yes 1.2M / no 7.1M; 44 no 37.6M; 45 yes 31.1M / no 21.1M; Props 2 and 5 have no matched committee money. Props 37, 40, 44 rose against Nov 16 because the initiative-number matches added committees. Inferred: Prop 3 "yes" donors include committees named "No on Prop 39 ...", so transfers between committees may need the viaCommittee handling checked. Left: compare with the state's own totals (sos.ca.gov / Cal-Access), check Props 2, 5 and 38 for missing committees, then the page (step 2, Hayden sees it before it goes public).

Progress Nov 18 (real run): `ballot.measure_totals` ran on the real zip through heavy.mjs in 107 seconds with no unreadable date (script `%TEMP%\emt-run-totals.py`, output `%TEMP%\emt-measure-totals.json`). Itemized yes/no dollars now: Prop 1 yes 6.07M; 3 yes 61.7M; 4 yes 0.80M; 37 yes 22.1M; 38 no 8.5K; 39 yes 8.97M; 40 no 129.8M; 41 yes 58.4M/no 0.70M; 42 yes 127.95M; 43 yes 1.20M; 44 no 37.6M; 45 yes 31.1M; Props 2 and 5 nothing found. Inferred: Prop 4 and Prop 43 yes look suspicious (many small gifts, names like Lee-Chang/Umberg) and may be older-year committees sharing BAL_NUM 4/43; 1 to 5 need a check. Unverified: not compared with the state's published totals (needs a look at the SoS/Cal-Access measure pages). Left: check Props 4 and 43 matches, compare with the state's totals, then the page (step 2, Hayden sees it before it goes public).
