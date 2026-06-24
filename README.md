# World Cup 2026 Pick'em Tracker

Generates a daily "morning brief" for an 11-person World Cup 2026 group-stage pick'em pool, simulating every possible outcome of that day's matches and showing what each scenario means for everyone's bracket.

## How it works

1. **`data.py`** — the pool's seed-to-team mapping per group, and each person's 1st/2nd/3rd/4th picks for all 12 groups.
2. **`matches.py`** — completed match results, today's not-yet-played matches, and betting odds, updated daily as the tournament progresses.
3. **`engine.py`** — scoring rules and FIFA's official tiebreaker cascade, used to rank a group's final standings from any set of results (real or hypothetical) and score everyone's pick against it.
4. **`gen_brief.py`** — for each of today's groups, simulates all 9 possible outcome combinations (2 simultaneous matches x 3 results each), scores every person under each scenario, computes the "chalk" (betting-favorite) outcome, and writes it all to `brief_payload.json`.
5. **`build_brief_static2.py`** — renders `brief_payload.json` into a single self-contained static HTML page (`brief_static_2026-06-24_v3.html`): a card per group with a color-coded scenario grid (win/loss/draw pills, green/yellow/red score bands), plus a leaderboard counted only from groups that have finished all 3 matchdays.

## Running it

```
python3 gen_brief.py            # re-simulate today's groups -> brief_payload.json
python3 build_brief_static2.py  # render brief_payload.json -> static HTML
```

The leaderboard intentionally ignores the pickem site's own running point totals — it only counts a group once all 6 of its group-stage matches have been played, to avoid crediting partial/in-progress standings.

## Output

The generated HTML (see `brief_static_2026-06-24_v3.html`) is a fully static page — no JavaScript — styled as a light card/dashboard theme, with a horizontally-scrollable scenario table on narrow screens so all 11 names stay readable on mobile.
