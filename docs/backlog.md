_Nov 9, 2026 sweep: nothing ready. The four newest Small picks (refresh switch on phone, refresh log page, go-live notice, figures update while open) all hang on the hourly refresh, which waits on Hayden's go; the newest pick (table opens before all rows load) is Medium and the table is one page; the older Small items need data the one-page table lacks or wording/look choices for Hayden._

# Election Money Tracker: ideas to build

## Hourly Data Refresh (Small, waiting on Hayden)

The hourly FEC refresh is written (.github/workflows/refresh.yml, kept on the PC, not uploaded) but
off. Once it's uploaded, GitHub updates the live site's numbers every hour by itself; until then
they change only when rebuilt by hand. Hayden said "wait" on Nov 9, 2026; upload and push it when he says go.

## Look Up Your Own Representative (Medium)

Type your address and see who funds the people who represent you. It turns the site from a list
into something any visitor can use in ten seconds. Hayden picked this idea on Nov 8, 2026.

## Find My Reps by Location (Small)

One button uses your phone's location to find who represents you, so you don't have to type an
address. A visitor on a phone gets there in one tap. The phone asks permission first, the location
is used only for that one lookup and never saved, and typing an address still works for anyone who
says no. It builds on Look Up Your Own Representative, so it comes after that. Hayden picked this
idea on Nov 8, 2026.

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

A simple line chart on each candidate's page showing how much money came in every month of the
race. A line tells the story of a race in one glance, next to the bar charts and the biggest-jump
list. Hayden picked this idea on Nov 8, 2026.

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

## Plain Words for Money Terms (Small)

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

## Ballot Measure Money Tracker (Medium)

Who is paying for and against each ballot measure, with the amounts and a link to each filing.
Ballot measure money is filed with each state, not the FEC, so which states to start with is a
swipe card for Hayden at build time. Hayden picked this idea on Nov 8, 2026.

## Ballot Measures in Plain Words (Small)

Each ballot measure gets a two-sentence summary of what a yes and a no would change, shown next to
who funds each side. Voters need both before they vote. It builds on the Ballot Measure Money
Tracker, so it comes after that. Every summary is neutral, links to
the official measure text, and Hayden reads it before it goes live. Hayden picked this idea on Nov 8,
2026.

## Broken Source Link Checker (Small)

Once a week, a check opens every link to a public filing on the site and lists any that broke, so
they can be fixed. A dead source link quietly weakens a politically sensitive site. It runs on
GitHub alongside the hourly data refresh, and the list stays private to Hayden. Hayden picked this
idea on Nov 8, 2026.

## Stale Figures Turn Amber (Small, after the hourly refresh)

If a number's as-of date gets too old, its Data Freshness Badge turns amber and says how many days
behind it is. It comes after the hourly refresh goes live, since until then every figure ages the
same way. Hayden still picks how many days counts as stale and the exact wording before it is built.
Hayden picked this idea on Nov 8, 2026.

## Hourly Refresh Switch On Phone (Small)

A single switch on your phone turns the hourly money data refresh on or off, with the last refresh time beside it. The hourly data refresh is built but sitting off until you say go, so you shouldn't have to wait for a PC session to flip it. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Refresh Log on the Site (Small)

A small page listing the last ten data refreshes with the time and how many figures changed. The hourly refresh is ready but switched off until you say go, and a visible log shows you it works before you flip it on. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Hourly Refresh Goes Live Notice (Small)

When you say go on the hourly data refresh, your phone tells you the first refresh ran and what changed. The hourly refresh is ready but waiting for your go, and you dislike being left out of the loop. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Figures Update While Open (Small)

When the hourly refresh brings new numbers, a page you already have open updates on its own without reloading. Three refresh picks are waiting on the hourly refresh go, and open pages would otherwise show stale numbers. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Table Opens Before All Rows Load (Medium)

The money table shows its first rows right away and fills in the rest while you read, instead of making you wait for everything. Table figures now show how many filed records add up to them, which gives the table more to load, and you like things fast. An idea for Election Money Tracker. Hayden picked it from the Ideas deck on 2026-11-09, so it goes ahead of unpicked items. If it defines the look, rules, names or new content, make an options card first.

## Ballot Measure Money View (Large)

A "Ballot measures" view on this site: for each California measure on the Nov 2026 ballot, the yes
total, the no total, the top donors on each side and the result, from Cal-Access filings, with a
link to the filing behind every number. Yes and no are always side by side, same size, no adjectives.
Hayden picked this idea on Nov 8, 2026 and said on Nov 9, 2026 to merge it into this site. The full
plan, fairness rules and steps are in [ballot-measures.md](ballot-measures.md). Nothing goes public
until Hayden has seen it.
