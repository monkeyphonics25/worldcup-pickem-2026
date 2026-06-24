import itertools, json
from data import SEEDS, GROUP_ORDER, POOL1, POOL2, decode
from matches import COMPLETED, TODAY, TCS

def team_group(team):
    for g in GROUP_ORDER:
        if team in SEEDS[g].values():
            return g
    raise ValueError(team)

def compute_stats(matches):
    """matches: list of (group, home, away, hg, ag). Returns dict[group][team] -> stats dict, plus head2head results."""
    stats = {g: {t: {'P':0,'W':0,'D':0,'L':0,'GF':0,'GA':0} for t in SEEDS[g].values()} for g in GROUP_ORDER}
    h2h = {g: {} for g in GROUP_ORDER}  # (teamA,teamB) sorted tuple -> list of (scorer_goals_for_each)
    for (g, h, a, hg, ag) in matches:
        sh, sa = stats[g][h], stats[g][a]
        sh['P']+=1; sa['P']+=1
        sh['GF']+=hg; sh['GA']+=ag
        sa['GF']+=ag; sa['GA']+=hg
        if hg>ag:
            sh['W']+=1; sa['L']+=1
        elif hg<ag:
            sa['W']+=1; sh['L']+=1
        else:
            sh['D']+=1; sa['D']+=1
        key = (h,a)
        h2h[g].setdefault(h, {})[a] = (hg, ag)
        h2h[g].setdefault(a, {})[h] = (ag, hg)
    for g in GROUP_ORDER:
        for t, s in stats[g].items():
            s['Pts'] = s['W']*3 + s['D']
            s['GD'] = s['GF'] - s['GA']
    return stats, h2h

def rank_group(group, stats, h2h):
    """Apply FIFA tiebreaker rules to produce ordered list of 4 teams (best first)."""
    teams = list(stats[group].keys())
    seed_rank = {SEEDS[group][s]: s for s in SEEDS[group]}  # lower seed number = higher ranked (proxy for step 3)

    def sort_key_primary(t):
        s = stats[group][t]
        return (-s['Pts'], -s['GD'], -s['GF'])

    # group teams into tiers by (Pts, GD, GF)
    teams_sorted = sorted(teams, key=sort_key_primary)
    result = []
    i = 0
    while i < len(teams_sorted):
        j = i
        key0 = sort_key_primary(teams_sorted[i])
        while j < len(teams_sorted) and sort_key_primary(teams_sorted[j]) == key0:
            j += 1
        tier = teams_sorted[i:j]
        if len(tier) == 1:
            result.extend(tier)
        else:
            result.extend(break_tie(group, tier, stats, h2h, seed_rank))
        i = j
    return result

def break_tie(group, tier, stats, h2h, seed_rank):
    # Step 1: head-to-head among tied teams only (points, GD, GF from matches between them)
    h2h_stats = {t: {'Pts':0,'GF':0,'GA':0} for t in tier}
    any_missing = False
    for a in tier:
        for b in tier:
            if a==b: continue
            res = h2h[group].get(a, {}).get(b)
            if res is None:
                any_missing = True
                continue
            gf, ga = res
            h2h_stats[a]['GF'] += gf
            h2h_stats[a]['GA'] += ga
            if gf>ga: h2h_stats[a]['Pts'] += 3
            elif gf==ga: h2h_stats[a]['Pts'] += 1
    def h2h_key(t):
        hs = h2h_stats[t]
        return (-hs['Pts'], -(hs['GF']-hs['GA']), -hs['GF'])
    sorted_tier = sorted(tier, key=h2h_key)
    # check if head-to-head fully separates them
    keys = [h2h_key(t) for t in sorted_tier]
    if len(set(keys)) == len(keys):
        return sorted_tier
    # Step 2 & 3: re-group remaining ties by overall GD, GF, TCS, then seed/ranking
    final = []
    i = 0
    while i < len(sorted_tier):
        j = i
        while j < len(sorted_tier) and h2h_key(sorted_tier[j]) == h2h_key(sorted_tier[i]):
            j += 1
        subtier = sorted_tier[i:j]
        if len(subtier) == 1:
            final.extend(subtier)
        else:
            def step2_key(t):
                s = stats[group][t]
                return (-s['GD'], -s['GF'], -TCS.get(t,0), seed_rank[t])
            final.extend(sorted(subtier, key=step2_key))
        i = j
    return final

def score_group_pick(pick_order, actual_order):
    pts_table = [5,5,2,2]
    pts = 0
    perfect = True
    for i in range(4):
        if pick_order[i] == actual_order[i]:
            pts += pts_table[i]
        else:
            perfect = False
    if perfect:
        pts += 2
    return pts

def score_all_groups(picks_decoded, actual_by_group):
    total = 0
    breakdown = {}
    for g in GROUP_ORDER:
        p = score_group_pick(picks_decoded[g], actual_by_group[g])
        breakdown[g] = p
        total += p
    return total, breakdown

if __name__ == '__main__':
    stats, h2h = compute_stats([(g,h,a,hg,ag) for (_,g,h,a,hg,ag) in COMPLETED])
    for g in GROUP_ORDER:
        order = rank_group(g, stats, h2h)
        print(g, order, [stats[g][t] for t in order])
