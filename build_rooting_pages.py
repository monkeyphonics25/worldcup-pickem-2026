import json, os

outdir = '/sessions/beautiful-elegant-johnson/mnt/outputs/wc_model'
with open(os.path.join(outdir, 'brief_payload.json')) as f:
    P = json.load(f)

FRIENDLY = P['friendly']
display_order = P['display_order']
group_brief = P['group_brief']
today_groups = P['today_groups']

GROUP_KICKOFF_ORDER = ['B', 'C', 'A']
GROUP_TIME = {'B': '12pm', 'C': '3pm', 'A': '6pm'}

ABBREV = {
    'Bosnia and Herzegovina': 'Bosnia & Herz.',
    'Korea Republic': 'Korea',
}

SLUG = {
    'Travis Winter': 'travis',
    'Dion Shaughnessy': 'dion',
    'Tommy McSweeney': 'tommy',
    'Mike Deez': 'mike',
    'mangmang (Alex Winter)': 'alex',
    'Adam Wallace': 'adam',
    'Kimberly Kendig': 'kim',
    'John Smith': 'john',
    'S N': 'sean',
    'Karly Deal': 'karly',
    'Farts (Art Panthavee)': 'art',
}

STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 24px; background: #f4f6f8; color: #1a1f2b;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.45;
}
.wrap { max-width: 1080px; margin: 0 auto; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 18px; margin: 28px 0 10px; border-bottom: 2px solid #e2e6ea; padding-bottom: 6px; }
h3 { font-size: 15px; margin: 0 0 8px; display:inline-block; }
.subtitle { color: #5b6573; font-size: 13px; margin-bottom: 18px; }
.card {
  background: #fff; border: 1px solid #e2e6ea; border-radius: 10px;
  padding: 16px 20px; margin-bottom: 14px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.callout {
  background: #eef7f0; border: 1px solid #bfe3c8; border-radius: 10px;
  padding: 16px 20px; margin-bottom: 14px;
}
.badge {
  display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 8px;
  border-radius: 999px; background: #d9ecff; color: #14538f; margin-right: 8px;
  vertical-align: middle;
}
.badge-max {
  display: inline-block; font-size: 11px; font-weight: 700; padding: 2px 8px;
  border-radius: 999px; margin-left: 8px; vertical-align: middle;
}
.max-16 { background: #d7f0dd; color: #1c6b34; }
.max-mid { background: #fdf1d6; color: #8a6d00; }
.max-low { background: #fbe2e2; color: #9c2b2b; }
.match-line { margin-bottom: 3px; }
.pill { display: inline-block; border-radius: 6px; padding: 2px 7px; font-weight: 500; margin-right: 5px; font-size: 12px; }
.pill-win { background: #d7f0dd; color: #1c6b34; }
.pill-loss { background: #fbe2e2; color: #9c2b2b; }
.pill-draw { background: #e9e8e3; color: #5f5e5a; }
.scenario-option { padding: 8px 0; border-bottom: 1px solid #edf0f3; }
.scenario-option:last-child { border-bottom: none; }
.small { font-size: 12px; color: #5b6573; }
.explainer { font-size: 14.5px; margin: 8px 0 10px; }
details.combos { margin-top: 6px; }
details.combos summary {
  cursor: pointer; font-size: 12.5px; color: #14538f; font-weight: 600;
  padding: 4px 0;
}
details.combos summary:hover { text-decoration: underline; }
details.combos[open] summary { margin-bottom: 4px; }
.tag-best { color: #1c6b34; font-weight: 700; }
.tag-worst { color: #9c2b2b; font-weight: 700; }
.backlink { display: inline-block; margin-bottom: 18px; font-size: 13px; color: #14538f; text-decoration: none; }
.backlink:hover { text-decoration: underline; }
.people-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.people-grid a {
  display: inline-block; padding: 6px 12px; border-radius: 999px; background: #d9ecff;
  color: #14538f; text-decoration: none; font-size: 13px; font-weight: 600;
}
.people-grid a:hover { background: #c3e0ff; }
footer { margin-top: 30px; padding-top: 14px; border-top: 1px solid #e2e6ea; font-size: 11.5px; color: #8a93a1; }
@media (max-width: 600px) {
  body { padding: 14px; }
  h1 { font-size: 20px; }
  .card, .callout { padding: 14px 16px; }
}
"""

def disp(team):
    return ABBREV.get(team, team)

def match_pills(home, away, outcome):
    if outcome == 'home_win':
        hc, ac = 'pill-win', 'pill-loss'
    elif outcome == 'away_win':
        hc, ac = 'pill-loss', 'pill-win'
    else:
        hc, ac = 'pill-draw', 'pill-draw'
    return f'<span class="pill {hc}">{disp(home)}</span><span class="pill {ac}">{disp(away)}</span>'

def max_class(score):
    if score >= 16:
        return 'max-16'
    if score >= 7:
        return 'max-mid'
    return 'max-low'

def person_best_scenarios(gb, name):
    """All distinct scenario combos (as tuples) that achieve this person's personal max score in this group,
    plus the same set rendered as HTML rows."""
    scenarios = gb['scenarios']
    max_score = max(sc['scores'][name] for sc in scenarios)
    matches_today = gb['matches_today']
    combos = []
    rows = []
    for sc in scenarios:
        if sc['scores'][name] == max_score:
            combo = tuple(sc['combo'])
            combos.append(combo)
            row = ''.join(
                f'<div class="match-line">{match_pills(h, a, o)}</div>'
                for (h, a), o in zip(matches_today, combo)
            )
            rows.append(row)
    return max_score, combos, rows

def result_clause(home, away, outcome):
    """Plain clause describing a single match outcome, e.g. 'Brazil beats Scotland'."""
    if outcome == 'home_win':
        return f'{home} beats {away}'
    if outcome == 'away_win':
        return f'{away} beats {home}'
    return f'{home} and {away} draw'

def condition_clause(home, away, allowed):
    """Plain noun-phrase clause for what a match needs to do, given the set of outcomes that work.
    Returns None if all three outcomes work (i.e. the match doesn't matter on its own)."""
    s = set(allowed)
    if s == {'home_win', 'draw', 'away_win'}:
        return None
    if s == {'home_win'}:
        return f'{home} to beat {away}'
    if s == {'away_win'}:
        return f'{away} to beat {home}'
    if s == {'draw'}:
        return f'{home} and {away} to draw'
    if s == {'home_win', 'draw'}:
        return f'{home} to avoid a loss to {away} — a win or a draw both work'
    if s == {'away_win', 'draw'}:
        return f'{away} to avoid a loss to {home} — a win or a draw both work'
    if s == {'home_win', 'away_win'}:
        return f'{home} vs. {away} to produce a winner — just not a draw'
    return None

def score_flourish(score):
    """A little snarky tag based on how good or bad the ceiling is."""
    if score >= 16:
        return ' Pull that off and it’s a perfect group.'
    if score >= 10:
        return ' Solid outcome, all things considered.'
    if score >= 7:
        return ' Not great, not nothing.'
    return ' Either way, it’s a pretty thin reward.'

def explain_scenario(name, g, matches_today, combos, max_score):
    """Build a short, plain-English, slightly snarky sentence describing what this person needs
    in this group's two simultaneous games."""
    (home1, away1), (home2, away2) = matches_today
    qualifying = set(combos)
    m1 = sorted({c[0] for c in qualifying})
    m2 = sorted({c[1] for c in qualifying})
    rect = {(o1, o2) for o1 in m1 for o2 in m2}
    missing = rect - qualifying

    clause1 = condition_clause(home1, away1, m1)
    clause2 = condition_clause(home2, away2, m2)
    flourish = score_flourish(max_score)

    if not missing:
        if clause1 is None and clause2 is None:
            return f'Doesn’t matter at all tonight — you’re locked in at {max_score} no matter how {home1}-{away1} or {home2}-{away2} go.{flourish}'
        if clause1 is None:
            return f'You need {clause2}. {home1} vs. {away1} doesn’t matter one bit.{flourish}'
        if clause2 is None:
            return f'You need {clause1}. {home2} vs. {away2} doesn’t matter one bit.{flourish}'
        return f'You need {clause1}, and {clause2}.{flourish}'

    if clause1 is None and clause2 is not None and len(missing) <= 2:
        exc = ' or '.join(f'{result_clause(home1, away1, o1)} while {result_clause(home2, away2, o2)}' for (o1, o2) in sorted(missing))
        return (f'You need {clause2}. {home1} vs. {away1} mostly doesn’t matter — except for one quirky exception: '
                f'if {exc}, that exact combo somehow still doesn’t get you there.{flourish}')
    if clause2 is None and clause1 is not None and len(missing) <= 2:
        exc = ' or '.join(f'{result_clause(home1, away1, o1)} while {result_clause(home2, away2, o2)}' for (o1, o2) in sorted(missing))
        return (f'You need {clause1}. {home2} vs. {away2} mostly doesn’t matter — except for one quirky exception: '
                f'if {exc}, that exact combo somehow still doesn’t get you there.{flourish}')

    # Messy fallback: no clean single-axis story.
    return (f'There’s no clean storyline here — a scattershot mix of results gets you to {max_score}, '
            f'and an equally scattershot mix doesn’t. Tonight’s just not really about Group {g} for you; '
            f'peek at the dropdown below if you want the full breakdown.{flourish}')

def nav_links(current_name):
    links = []
    for name in display_order:
        slug = SLUG[name]
        label = FRIENDLY[name]
        if name == current_name:
            links.append(f'<span class="pill" style="background:#14538f;color:#fff;">{label}</span>')
        else:
            links.append(f'<a href="rooting-{slug}.html">{label}</a>')
    return '<div class="people-grid">' + ''.join(links) + '</div>'

def build_person_page(name):
    short = FRIENDLY[name]
    parts = []
    parts.append('<a class="backlink" href="index.html">&larr; Back to the full brief</a>')
    parts.append(f"<h1>Who should {short} root for tonight?</h1>")
    parts.append('<div class="subtitle">Wednesday, June 24, 2026 &middot; Groups A, B, and C play matchday 3</div>')
    parts.append(f'<div class="card">Tonight\'s three games decide {short}\'s fate in Groups B, C, and A. Below is exactly what {short} needs to happen in each one to lock in the most points possible &mdash; root accordingly.</div>')

    for g in GROUP_KICKOFF_ORDER:
        gb = group_brief[g]
        matches_today = gb['matches_today']
        vs = ' &amp; '.join(f"{disp(h)} vs. {disp(a)}" for (h, a) in matches_today)
        max_score, combos, rows = person_best_scenarios(gb, name)
        explainer = explain_scenario(name, g, matches_today, combos, max_score)
        n = len(rows)
        summary_label = f'See all {n} winning combination{"s" if n != 1 else ""}'
        parts.append('<div class="card">')
        parts.append(f'<span class="badge">Group {g}</span><h3>{vs} &middot; {GROUP_TIME[g]}</h3>'
                      f'<span class="badge-max {max_class(max_score)}">best case: {max_score} pts</span>')
        parts.append(f'<p class="explainer">{explainer}</p>')
        parts.append(f'<details class="combos"><summary>{summary_label}</summary>')
        for row in rows:
            parts.append(f'<div class="scenario-option">{row}</div>')
        parts.append('</details>')
        parts.append('</div>')

    parts.append('<h2>Jump to someone else</h2>')
    parts.append('<div class="card">' + nav_links(name) + '</div>')
    parts.append('<footer>Based on tonight\'s matchday-3 simulation in the World Cup Pick\'em Morning Brief. Odds via CBS Sports; standings via FIFA.com.</footer>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Who should {short} root for tonight? &mdash; World Cup Pick'em</title>
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{''.join(parts)}
</div>
</body>
</html>"""
    return html

written = []
for name in display_order:
    slug = SLUG[name]
    html = build_person_page(name)
    outfile = os.path.join(outdir, f'rooting-{slug}.html')
    with open(outfile, 'w') as f:
        f.write(html)
    written.append(outfile)

print('wrote', len(written), 'pages:')
for w in written:
    print(' ', w)
