# AIPAC Money Tracker 2026

A one-page tracker of money from AIPAC's PAC (FEC `C00797670`) and its super PAC, United Democracy
Project (FEC `C00799031`), to each 2026 federal candidate, from public FEC filings.

- **Live:** the page pulls the newest filings from the FEC API (`api.open.fec.gov`) in the viewer's
  browser every 30 minutes (every 5 with a free key from https://api.data.gov/signup/, saved in the
  browser only).
- **Built-in data:** `build.py` bakes the FEC bulk files into `index.html`, so the page still works when
  the API is rate-limited. Run `python build.py` and push to refresh it.
- **Download CSV** saves the rows shown (after filters) with FEC source links and a data-as-of date.
- **Each top figure** shows its data-as-of date and links to the FEC committee page behind it.
- **"Rejects AIPAC" icons** come only from the sourced `STANCES` list in `index.html`; the FEC does not
  record public statements. Add entries with a source link.

This counts lobby money from US committees, not money from the Israeli government: US law bars foreign
governments and foreign nationals from funding US campaigns.
