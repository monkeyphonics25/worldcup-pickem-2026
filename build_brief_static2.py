import json, os

outdir = '/sessions/beautiful-elegant-johnson/mnt/outputs/wc_model'
with open(os.path.join(outdir, 'brief_payload.json')) as f:
    P = json.load(f)

FRIENDLY = P['friendly']
display_order = P['display_order']
group_brief = P['group_brief']
today_groups = P['today_groups']
finished_groups = P['finished_groups']
leaderboard = P['leaderboard']
max_possible = P['max_possible']

GROUP_KICKOFF_ORDER = ['B', 'C', 'A']
GROUP_TIME = {'B': '12pm', 'C': '3pm', 'A': '6pm'}

ABBREV = {
    'Bosnia and Herzegovina': 'Bosnia & Herz.',
    'Korea Republic': 'Korea',
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
table { width: 100%; border-collapse: collapse; font-size: 12px; margin: 0; }
th, td { text-align: center; padding: 6px 5px; border-bottom: 1px solid #edf0f3; overflow: hidden; }
th:first-child, td:first-child { text-align: left; }
th { color: #5b6573; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: .03em; white-space: nowrap; }
.table-scroll { overflow-x: auto; margin: 10px 0 4px; -webkit-overflow-scrolling: touch; }
table.scenario { table-layout: fixed; min-width: 860px; }
table.scenario th:first-child, table.scenario td:first-child { width: 150px; }
table.leaderboard { max-width: 480px; }
.match-line { margin-bottom: 3px; white-space: nowrap; }
.match-line:last-child { margin-bottom: 0; }
.pill { display: inline-block; border-radius: 6px; padding: 2px 7px; font-weight: 500; margin-right: 5px; font-size: 12px; }
.pill-win { background: #d7f0dd; color: #1c6b34; }
.pill-loss { background: #fbe2e2; color: #9c2b2b; }
.pill-draw { background: #e9e8e3; color: #5f5e5a; }
tr.chalk { background: #d9ecff; }
tr.chalk td { font-weight: 700; }
td.score { font-weight: 700; border-radius: 6px; }
td.score-green { background: #d7f0dd; color: #1c6b34; }
td.score-yellow { background: #fdf1d6; color: #8a6d00; }
td.score-red { background: #fbe2e2; color: #9c2b2b; }
.small { font-size: 12px; color: #5b6573; }
.tag-best { color: #1c6b34; font-weight: 700; }
.tag-worst { color: #9c2b2b; font-weight: 700; }
.lb-rank1 td { background: #eef7f0; font-weight: 700; }
footer { margin-top: 30px; padding-top: 14px; border-top: 1px solid #e2e6ea; font-size: 11.5px; color: #8a93a1; }
@media (max-width: 600px) {
  body { padding: 14px; }
  h1 { font-size: 20px; }
  .card, .callout { padding: 14px 16px; }
  table.scenario { min-width: 720px; }
  table.scenario th:first-child, table.scenario td:first-child { width: 128px; }
}
"""

def band_class(score):
    if score >= 10:
        return 'score-green'
    if score >= 5:
        return 'score-yellow'
    return 'score-red'

def disp(team):
    return ABBREV.get(team, team)

def match_pills(home, away, outcome):
    if outcome == 'home_win':
        hc, ac = 'pill-win', 'pill-loss'
    elif outcome == 'away_win':
        hc, ac = 'pill-loss', 'pill-win'
    else:
        hc, ac = 'pill-draw', 'pill-draw'
    return f'<div class="match-line"><span class="pill {hc}">{disp(home)}</span><span class="pill {ac}">{disp(away)}</span></div>'

def scenario_label_cell(group, combo):
    matches = group_brief[group]['matches_today']
    return ''.join(match_pills(h, a, o) for (h, a), o in zip(matches, combo))

def scenario_table(group):
    gb = group_brief[group]
    scenarios = gb['scenarios']
    chalk_label = gb['chalk_label']
    rows = ['<tr><th>If this happens</th>' + ''.join(f'<th>{FRIENDLY[n]}</th>' for n in display_order) + '</tr>']
    for sc in scenarios:
        is_chalk = sc['label'] == chalk_label
        cls = ' class="chalk"' if is_chalk else ''
        label_cell = scenario_label_cell(group, sc['combo'])
        cells = f'<td>{label_cell}</td>'
        for name in display_order:
            score = sc['scores'][name]
            cells += f'<td class="score {band_class(score)}">{score}</td>'
        rows.append(f'<tr{cls}>{cells}</tr>')
    return '<div class="table-scroll"><table class="scenario">' + ''.join(rows) + '</table></div>'

def leaderboard_table():
    rows = ['<tr><th>Rank</th><th>Bracket</th><th>Points</th></tr>']
    for i, (name, score) in enumerate(leaderboard, 1):
        cls = ' class="lb-rank1"' if i <= 3 else ''
        rows.append(f'<tr{cls}><td>{i}</td><td>{FRIENDLY[name]}</td><td>{score}</td></tr>')
    return '<table class="leaderboard">' + ''.join(rows) + '</table>'

parts = []
parts.append("<h1>⚽ World Cup Pick'em Morning Brief</h1>")
parts.append('<div class="subtitle">Wednesday, June 24, 2026</div>')
parts.append('<div class="card">Every group has now played its first two matches. Today, Groups A, B, and C play their series-deciding matchday 3 — each group’s two matches kicking off at the same time. Here’s what today’s results mean for all eleven brackets.</div>')

parts.append('<h2>Where everyone actually stands</h2>')
if finished_groups:
    parts.append(f'<div class="small" style="margin-bottom:8px;">Counting only groups that have played all three matchdays ({", ".join(finished_groups)}, out of {max_possible} possible points) — not the pickem site’s own running totals.</div>')
    parts.append('<div class="card">' + leaderboard_table() + '</div>')
else:
    parts.append('<div class="callout">No group has finished all three matchdays yet, so there’s no real leaderboard to show — anything from the pickem site right now is just a partial snapshot, not a final score. That changes tonight: once Groups A, B, and C wrap up their matchday 3 games, those three groups lock in for good, and tomorrow’s brief opens with the first real standings. Nine groups still have one game left to play after that.</div>')

for g in GROUP_KICKOFF_ORDER:
    gb = group_brief[g]
    matches_today = gb['matches_today']
    vs = ' &amp; '.join(f"{disp(h)} vs. {disp(a)}" for (h, a) in matches_today)
    standings_line = ', '.join(f"{disp(r['team'])} ({r['Pts']} pts)" for r in gb['entering_standings'])
    parts.append('<div class="card">')
    parts.append(f'<span class="badge">Group {g}</span><h3>{vs} &middot; {GROUP_TIME[g]}</h3>')
    parts.append(f'<p class="small" style="margin:8px 0 0;">Entering tonight: {standings_line}. ' + ' '.join(gb['match_descriptions']) + '</p>')
    parts.append(scenario_table(g))
    best_name, (best_score, best_label) = max(gb['best_for'].items(), key=lambda kv: kv[1][0])
    worst_name, (worst_score, worst_label) = min(gb['worst_for'].items(), key=lambda kv: kv[1][0])
    parts.append(f'<p class="small" style="margin-top:10px;"><span class="tag-best">{FRIENDLY[best_name]}</span> has the most to gain tonight — a {best_score} is on the table if &ldquo;{best_label}&rdquo; happens. <span class="tag-worst">{FRIENDLY[worst_name]}</span> has the least margin for error — &ldquo;{worst_label}&rdquo; leaves them with just {worst_score}.</p>')
    parts.append('</div>')

parts.append('<h2>Tonight’s chalk math</h2>')
chalk_total = {name: sum(group_brief[g]['chalk_scores'][name] for g in today_groups) for name in display_order}
chalk_best = max(chalk_total.items(), key=lambda kv: kv[1])
chalk_worst = min(chalk_total.items(), key=lambda kv: kv[1])
parts.append(f'<div class="callout">If every favorite wins exactly as the odds suggest across all three groups tonight, <span class="tag-best">{FRIENDLY[chalk_best[0]]}</span> comes out best at {chalk_best[1]} of a possible 48 points, while <span class="tag-worst">{FRIENDLY[chalk_worst[0]]}</span> brings up the rear at {chalk_worst[1]}. The colored grids above show exactly how that flips if any of tonight’s games go the other way.</div>')
parts.append('<p class="small">Groups A, B, and C wrap up their group stage tonight. Tomorrow’s brief covers Groups D, E, and F.</p>')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>World Cup Pick'em Morning Brief — Wednesday, June 24</title>
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{''.join(parts)}
<footer>Odds via CBS Sports; standings and results via FIFA.com. Scoring: 5 pts exact 1st/2nd, 2 pts exact 3rd/4th, +2 bonus for a perfect group (max 16/group). Times shown are Pacific.</footer>
</div>
</body>
</html>"""

outfile = os.path.join(outdir, 'brief_static_2026-06-24_v3.html')
with open(outfile, 'w') as f:
    f.write(html)
print('wrote', outfile, '(', len(html), 'chars )')
