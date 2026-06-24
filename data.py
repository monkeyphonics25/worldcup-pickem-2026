# Seed -> team mapping (same for both pools, same tournament)
SEEDS = {
 'A': {1:'Mexico',2:'South Africa',3:'Korea Republic',4:'Czechia'},
 'B': {1:'Canada',2:'Bosnia and Herzegovina',3:'Qatar',4:'Switzerland'},
 'C': {1:'Brazil',2:'Morocco',3:'Haiti',4:'Scotland'},
 'D': {1:'USA',2:'Paraguay',3:'Australia',4:'Türkiye'},
 'E': {1:'Germany',2:'Curaçao',3:'Côte d\'Ivoire',4:'Ecuador'},
 'F': {1:'Netherlands',2:'Japan',3:'Sweden',4:'Tunisia'},
 'G': {1:'Belgium',2:'Egypt',3:'IR Iran',4:'New Zealand'},
 'H': {1:'Spain',2:'Cabo Verde',3:'Saudi Arabia',4:'Uruguay'},
 'I': {1:'France',2:'Senegal',3:'Iraq',4:'Norway'},
 'J': {1:'Argentina',2:'Algeria',3:'Austria',4:'Jordan'},
 'K': {1:'Portugal',2:'Congo DR',3:'Uzbekistan',4:'Colombia'},
 'L': {1:'England',2:'Croatia',3:'Ghana',4:'Panama'},
}
GROUP_ORDER = ['A','B','C','D','E','F','G','H','I','J','K','L']

# Pool 1 compact picks (48 chars, 12 groups x 4 digits, order A-L, digit=seed predicted for 1st..4th)
POOL1 = {
 'Travis Winter':'143241231423412341321234213414321423132441231234',
 'Dion Shaughnessy':'132441321423312414321234132414321243123414231234',
 'Tommy McSweeney':'312414231243413214322134123414321423123414231234',
 'Mike Deez':'132414232143431241321234132414231423123441232143',
 'mangmang (Alex Winter)':'431212431243134213421234312414231234123441321423',
 'Adam Wallace':'132414231243142314321234123414321243132441231243',
 'Kimberly Kendig':'134241231234142314321324123414231432132414231243',
 'John Smith':'134241231234143214321234123414321243123441231234',
 'S N':'134214232143142314321243312414231243123414321423',
 'Karly Deal':'132441231234143213421234123414321423132414231234',
}

# Pool 2 compact picks
POOL2 = {
 'mangmang (own entry, 44pts shown)':'134241324213134213423214431243124123134242131342',
 'Farts (Art Panthavee, 72pts shown)':'132441231243142314321234132414231243132414231243',
}

def decode(compact):
    groups = {}
    for i,g in enumerate(GROUP_ORDER):
        chunk = compact[i*4:(i+1)*4]
        seeds = [int(c) for c in chunk]
        groups[g] = [SEEDS[g][s] for s in seeds]
    return groups

if __name__ == '__main__':
    import json
    print("=== POOL 1 ===")
    for name, compact in POOL1.items():
        assert len(compact)==48, f"{name} len {len(compact)}"
        d = decode(compact)
        print(name)
        for g in GROUP_ORDER:
            print(f"  {g}: {d[g]}")
    print("\n=== POOL 2 ===")
    for name, compact in POOL2.items():
        assert len(compact)==48
        d = decode(compact)
        print(name)
        for g in GROUP_ORDER:
            print(f"  {g}: {d[g]}")
