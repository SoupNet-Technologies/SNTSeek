# SPEC — SNTSeek

## Purpose

A Tkinter desktop GUI for running Shodan searches and eyeballing the results: a query box, a results table, a detail pane for the selected host, and CSV export. Single file, ~180 lines. Part of the SoupNet security tooling.

Authorized use note: this queries Shodan's public dataset, which is passive recon by definition. It does not touch the hosts it reports on. Use it on scopes you are allowed to touch, which for Shodan means "all of it" — the tool never sends packets to targets.

## Quick facts

- Language: Python 3
- Deps: `shodan`, `beautifulsoup4`, `python-dotenv` (stdlib: `tkinter`, `csv`, `ast`)
- Entry point: `main.py`
- Config: `.env` in the project root, key `SHODAN_API_KEY` (loaded via `load_dotenv()` at startup)
- Install: `pip install shodan beautifulsoup4 python-dotenv`
- Run: `python main.py`

## Architecture

One class, `ShodanGUI`. Startup order in `__init__`: load `.env` → read `SHODAN_API_KEY` → if missing, show an error dialog and destroy the window (no key, no app) → build `shodan.Shodan(key)` client → build widgets.

The window is 1000x700 with four stacked frames:

1. Search frame — `tk.Entry` (Enter key bound) + Search button, both call `perform_search()`
2. Results frame — `ttk.Treeview` in "headings" mode, columns: IP, Port, Hostnames, Organization, ISP; vertical scrollbar
3. Details frame — read-only `tk.Text` (15 rows) showing the full record for the selected row
4. Buttons frame — "Save Results" (disabled until a search succeeds) plus a status bar at the bottom (`tk.StringVar` label)

## Interfaces

- Input: a single Shodan query string, passed verbatim to `api.search(query)` (default page only — first page of results, Shodan's standard limit)
- Treeview columns: `IP`, `Port`, `Hostnames`, `Organization`, `ISP` (widths 150/60/200/200/200, non-stretch)
- Detail pane fields: IP, Port, Hostnames, Organization, ISP, Location (`city, region_code, country_name`, N/A when empty), then banner `data` with HTML stripped via `BeautifulSoup(data, 'html.parser').get_text()`
- Export: Save Results opens `asksaveasfilename` (default extension `.csv`), writes one row per match with header `IP, Port, Hostnames, Organization, ISP, Location, Data` (banner text is HTML-stripped, same as the detail pane)
- Status bar messages: "Searching...", "Search completed: N results found.", "Error occurred during search."

## Data & storage

No persistent state. The only output is the CSV you explicitly save. The full result dict for each row is smuggled into the treeview via `tree.set(item_id, 'data', result)` and parsed back with `ast.literal_eval` on selection — it works, but it is a hack resting on repr round-tripping.

## Testing

None. No tests, no CI.

## Limitations & known issues

- The search runs synchronously on the UI thread; the window freezes during the request. The "Searching..." status only shows cause `update_idletasks()` is called before the blocking call
- The existing README is stale in three ways: it says to run `python SNTSeek.py` (the file is `main.py`), claims results auto-save to `shodan_results.csv` (saving is manual, via file dialog), and lists the columns as "IP, Port, OS, Organization, and Data" (actual: IP, Port, Hostnames, Organization, ISP)
- Only the first page of Shodan results is shown; no pagination or `pages` parameter
- API errors are surfaced via modal `messagebox` — fine, but it kills any batch workflow
- No retry/timeout tuning on the Shodan client

## File map

```
main.py        the entire application (ShodanGUI + __main__ block)
.gitignore     single line, presumably .env
README.md      existing (see stale-docs note above)
```
