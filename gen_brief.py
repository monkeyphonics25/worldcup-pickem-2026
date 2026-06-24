import itertools, json, datetime
from data import SEEDS, GROUP_ORDER, POOL1, POOL2, decode
from matches import COMPLETED, TODAY, ODDS, TCS, TODAY_DATE
from engine import compute_stats, rank_group, score_group_pick

# ---- Merged 11-entry pool (per Alex: only the mangmang entry is his; Pool 1's
# 10 entries + Farts from Pool 2, dropping Pool 2's duplicate mangmang row) ----
POOL = dict(POOL1)
POOL['Farts (Art Panthavee)'] = POOL2['Farts (Art Panthavee, 72pts shown)']
ME = 'mangmang (Alex Winter)'

FRIENDLY = {
 'Travis Winter': 'Travis',
 'Dion Shaughnessy': 'Dion',
 'Tommy McSweeney': 'Tommy',
 'Mike Deez': 'Mike',
 'mangmang (Alex Winter)': 'Alex',
 'Adam Wallace': 'Adam',
 'Kimberly Kendig': 'Kim',
 'John Smith': 'John',
 'S N': 'Sean',
 'Karly Deal': 'Karly',
 'Farts (Art Panthavee)': 'Art',
}

base_matches = [(g,h,a,hg,ag) for (_,g,h,a,hg,ag) in COMPLETED]
OUTCOMES = {'home_win': (1,0), 'draw': (1,1), 'away_win': (0,1)}

stats0, h2h0 = compute_stats(base_matches)
current_order = {g: rank_group(g, stats0, h2h0) for g in GROUP_ORDER}

pool_decoded = {name: decode(compact) for name, compact in POOL.items()}

# ---- Leaderboard: ONLY groups that have played all 3 matchdays (6 matches) count.
# This grows day by day: 0 groups right now -> 3 (A,B,C) after tonight -> 6 after
# 6/25 (+D,E,F) -> 9 after 6/26 (+G,H,I) -> 12 (full group stage) after 6/27. We
# deliberately do NOT score partially-played groups, and we never use the
# pickem site's own running point totals. ----
group_match_count = {g: 0 for g in GROUP_ORDER}
for (_, g, h, a, hg, ag) in COMPLETED:
    group_match_count[g] += 1
FINISHED_GROUPS = [g for g in GROUP_ORDER if group_match_count[g] >= 6]
MAX_POSSIBLE = len(FINISHED_GROUPS) * 16

def total_score(decoded_picks):
    total = 0
    bd = {}
    for g in FINISHED_GROUPS:
        s = score_group_pick(decoded_picks[g], current_order[g])
        bd[g] = s
        total += s
    return total, bd

pool_totals = {}
pool_breakdowns = {}
for name, decoded in pool_decoded.items():
    t, bd = total_score(decoded)
    pool_totals[name] = t
    pool_breakdowns[name] = bd
leaderboard = sorted(pool_totals.items(), key=lambda x: -x[1])
# stable display order used for the scenario-grid columns (best to worst by current leaderboard,
# or pool order if no groups finished yet)
display_order = [name for name, _ in leaderboard]

# ---- Simulate matchday-3 for groups in TODAY (A, B, C), 2 simultaneous matches/group ----
group_matches_today = {}
for (g,h,a,t) in TODAY:
    group_matches_today.setdefault(g, []).append((h,a))

def simulate_group(group, matches_today):
    results = {}
    combos = list(itertools.product(OUTCOMES.keys(), repeat=len(matches_today)))
    for combo in combos:
        sim_matches = list(base_matches)
        for (home,away), outcome in zip(matches_today, combo):
            hg, ag = OUTCOMES[outcome]
            sim_matches.append((group, home, away, hg, ag))
        stats, h2h = compute_stats(sim_matches)
        results[combo] = rank_group(group, stats, h2h)
    return results, combos

def label_combo(matches_today, combo):
    parts = []
    for (home,away), outcome in zip(matches_today, combo):
        if outcome=='home_win': parts.append(f"{home} win")
        elif outcome=='away_win': parts.append(f"{away} win")
        else: parts.append(f"{home}-{away} draw")
    return ' & '.join(parts)

def implied_prob(odds):
    def p(o):
        return 100/(o+100) if o>0 else (-o)/(-o+100)
    raw = {'home':p(odds['home']),'draw':p(odds['draw']),'away':p(odds['away'])}
    s = sum(raw.values())
    return {k: v/s for k,v in raw.items()}

def describe_match(home, away, odds):
    """Qualitative (no-percentage) description of favorite/underdog/draw chance."""
    probs = implied_prob(odds)
    ph, pd, pa = probs['home'], probs['draw'], probs['away']
    if ph >= pa:
        fav, dog, pf = home, away, ph
    else:
        fav, dog, pf = away, home, pa
    if pf >= 0.75:
        strength = f"a heavy favorite over {dog}"
    elif pf >= 0.60:
        strength = f"a clear favorite over {dog}"
    elif pf >= 0.52:
        strength = f"a slight favorite over {dog}"
    else:
        strength = f"barely ahead of {dog} — about as close to a coin flip as this slate gets"
    draw_note = " There's a real chance this one ends level." if pd >= 0.27 else ""
    return f"{fav} is {strength}.{draw_note}", fav, probs

today_groups = sorted(set(g for (g,h,a,t) in TODAY))
group_brief = {}
for g in today_groups:
    matches_today = group_matches_today[g]
    res, combos = simulate_group(g, matches_today)
    scenarios = []
    for combo in combos:
        order = res[combo]
        scores = {name: score_group_pick(d[g], order) for name, d in pool_decoded.items()}
        scenarios.append({
            'label': label_combo(matches_today, combo),
            'combo': combo,
            'order': order,
            'scores': scores,
        })

    match_descriptions = []
    chalk_outcome = []
    for (home,away) in matches_today:
        desc, fav, probs = describe_match(home, away, ODDS[(home,away)])
        match_descriptions.append(desc)
        fav_key = 'home_win' if fav==home else 'away_win'
        # if it's basically a coin flip, don't pretend a tiny edge is "the chalk" -
        # still need a pick for the chalk-math section, so just take the favorite as computed
        chalk_outcome.append(fav_key)
    chalk_label = label_combo(matches_today, tuple(chalk_outcome))
    chalk_order = res[tuple(chalk_outcome)]
    chalk_scores = {name: score_group_pick(d[g], chalk_order) for name, d in pool_decoded.items()}

    best_for = {}
    worst_for = {}
    for name in POOL:
        s_sorted = sorted(scenarios, key=lambda s: -s['scores'][name])
        best_for[name] = (s_sorted[0]['scores'][name], s_sorted[0]['label'])
        worst_for[name] = (s_sorted[-1]['scores'][name], s_sorted[-1]['label'])

    group_brief[g] = {
        'matches_today': matches_today,
        'match_descriptions': match_descriptions,
        'entering_standings': [{'team':t, **{k:stats0[g][t][k] for k in ['P','W','D','L','GF','GA','GD','Pts']}} for t in current_order[g]],
        'scenarios': scenarios,
        'chalk_label': chalk_label,
        'chalk_order': chalk_order,
        'chalk_scores': chalk_scores,
        'best_for': best_for,
        'worst_for': worst_for,
    }

payload = {
    'generated_at': datetime.datetime.now().astimezone().isoformat(),
    'as_of_date': TODAY_DATE,
    'brief_for_date': '2026-06-24',
    'today_groups': today_groups,
    'finished_groups': FINISHED_GROUPS,
    'max_possible': MAX_POSSIBLE,
    'leaderboard': leaderboard,
    'display_order': display_order,
    'pool_breakdowns': pool_breakdowns,
    'group_brief': group_brief,
    'friendly': FRIENDLY,
    'me_name': ME,
    'pool_picks': pool_decoded,
    'current_order': current_order,
    'group_order': GROUP_ORDER,
}

with open('brief_payload.json','w') as f:
    json.dump(payload, f, indent=1, ensure_ascii=False, default=list)
print('wrote brief_payload.json')
print('\nFinished groups (count toward leaderboard):', FINISHED_GROUPS or '(none yet)')
print('Leaderboard:')
for name, score in leaderboard:
    print(f"  {FRIENDLY[name]:8s} {score}")
print('\nGroups in brief:', today_groups)
for g in today_groups:
    print(f"\nGroup {g} entering standings:", [r['team'] for r in group_brief[g]['entering_standings']])
    print('  chalk result:', group_brief[g]['chalk_label'], '->', group_brief[g]['chalk_order'])
