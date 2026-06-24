# All completed group-stage matches as of 2026-06-23 end of day.
# Every group has now played exactly 2 of 3 matchdays (matchday 3 begins 6/24).
# format: (date, group, home, away, home_goals, away_goals)
COMPLETED = [
 ('2026-06-11','A','Mexico','South Africa',2,0),
 ('2026-06-11','A','Korea Republic','Czechia',2,1),
 ('2026-06-12','B','Canada','Bosnia and Herzegovina',1,1),
 ('2026-06-12','D','USA','Paraguay',4,1),
 ('2026-06-13','B','Qatar','Switzerland',1,1),
 ('2026-06-13','C','Brazil','Morocco',1,1),
 ('2026-06-13','C','Haiti','Scotland',0,1),
 ('2026-06-13','D','Australia','Türkiye',2,0),
 ('2026-06-14','E','Germany','Curaçao',7,1),
 ('2026-06-14','F','Netherlands','Japan',2,2),
 ('2026-06-14','E',"Côte d'Ivoire",'Ecuador',1,0),
 ('2026-06-14','F','Sweden','Tunisia',5,1),
 ('2026-06-15','H','Spain','Cabo Verde',0,0),
 ('2026-06-15','G','Belgium','Egypt',1,1),
 ('2026-06-15','H','Saudi Arabia','Uruguay',1,1),
 ('2026-06-15','G','IR Iran','New Zealand',2,2),
 ('2026-06-16','I','France','Senegal',3,1),
 ('2026-06-16','I','Iraq','Norway',1,4),
 ('2026-06-16','J','Argentina','Algeria',3,0),
 ('2026-06-16','J','Austria','Jordan',3,1),
 ('2026-06-17','K','Portugal','Congo DR',1,1),
 ('2026-06-17','L','England','Croatia',4,2),
 ('2026-06-17','L','Ghana','Panama',1,0),
 ('2026-06-17','K','Uzbekistan','Colombia',1,3),
 ('2026-06-18','A','Czechia','South Africa',1,1),
 ('2026-06-18','B','Switzerland','Bosnia and Herzegovina',4,1),
 ('2026-06-18','B','Canada','Qatar',6,0),
 ('2026-06-18','A','Mexico','Korea Republic',1,0),
 ('2026-06-19','D','USA','Australia',2,0),
 ('2026-06-19','C','Scotland','Morocco',0,1),
 ('2026-06-19','C','Brazil','Haiti',3,0),
 ('2026-06-19','D','Türkiye','Paraguay',0,1),
 ('2026-06-20','F','Netherlands','Sweden',5,1),
 ('2026-06-20','E','Germany',"Côte d'Ivoire",2,1),
 ('2026-06-20','E','Ecuador','Curaçao',0,0),
 ('2026-06-20','F','Tunisia','Japan',0,4),
 ('2026-06-21','H','Spain','Saudi Arabia',4,0),
 ('2026-06-21','G','Belgium','IR Iran',0,0),
 ('2026-06-21','H','Uruguay','Cabo Verde',2,2),
 ('2026-06-21','G','New Zealand','Egypt',1,3),
 ('2026-06-22','J','Argentina','Austria',2,0),
 ('2026-06-22','I','France','Iraq',3,0),
 ('2026-06-22','I','Norway','Senegal',3,2),
 ('2026-06-22','J','Jordan','Algeria',1,2),
 ('2026-06-23','K','Portugal','Uzbekistan',5,0),
 ('2026-06-23','L','England','Ghana',0,0),
 ('2026-06-23','L','Panama','Croatia',0,1),
 ('2026-06-23','K','Colombia','Congo DR',1,0),
]

TODAY_DATE = '2026-06-23'

# The next slate of matches (matchday 3 for Groups A, B, C) is what the morning
# brief is built around. All 3 groups' matchday-3 games kick off in pairs on
# Wednesday 2026-06-24 (times below are US/Eastern, matching CBS Sports broadcast listings).
# format: (group, home, away, kickoff_et)
TODAY = [
 ('B','Switzerland','Canada','3:00pm ET'),
 ('B','Bosnia and Herzegovina','Qatar','3:00pm ET'),
 ('C','Morocco','Haiti','6:00pm ET'),
 ('C','Scotland','Brazil','6:00pm ET'),
 ('A','Czechia','Mexico','9:00pm ET'),
 ('A','South Africa','Korea Republic','9:00pm ET'),
]

# Betting odds (American moneyline, CBS Sports consensus, as of 2026-06-23) for the
# matchday-3 pairs covered in TODAY. Used to gauge likelihood of pickem-relevant outcomes.
ODDS = {
 ('Switzerland','Canada'): {'home':135,'draw':210,'away':230},
 ('Bosnia and Herzegovina','Qatar'): {'home':-260,'draw':420,'away':600},
 ('Morocco','Haiti'): {'home':-599,'draw':600,'away':1600},
 ('Scotland','Brazil'): {'home':800,'draw':420,'away':-310},
 ('Czechia','Mexico'): {'home':270,'draw':290,'away':-115},
 ('South Africa','Korea Republic'): {'home':450,'draw':280,'away':-155},
}

# Remaining matchday-3 fixtures beyond "today", for reference / future scheduled runs.
UPCOMING = [
 ('D','Türkiye','USA','2026-06-25'),
 ('D','Paraguay','Australia','2026-06-25'),
 ('E','Curaçao',"Côte d'Ivoire",'2026-06-25'),
 ('E','Ecuador','Germany','2026-06-25'),
 ('F','Japan','Sweden','2026-06-25'),
 ('F','Tunisia','Netherlands','2026-06-25'),
 ('G','Egypt','IR Iran','2026-06-26'),
 ('G','New Zealand','Belgium','2026-06-26'),
 ('H','Cabo Verde','Saudi Arabia','2026-06-26'),
 ('H','Uruguay','Spain','2026-06-26'),
 ('I','Norway','France','2026-06-26'),
 ('I','Senegal','Iraq','2026-06-26'),
 ('J','Algeria','Austria','2026-06-27'),
 ('J','Jordan','Argentina','2026-06-27'),
 ('K','Colombia','Portugal','2026-06-27'),
 ('K','Congo DR','Uzbekistan','2026-06-27'),
 ('L','Panama','England','2026-06-27'),
 ('L','Croatia','Ghana','2026-06-27'),
]

# Team Conduct Score (TCS), refreshed from FIFA standings page as of 2026-06-23 (post matchday 2).
TCS = {
 'Mexico':-5,'Korea Republic':-3,'Czechia':-1,'South Africa':-12,
 'Switzerland':-2,'Canada':-3,'Qatar':-11,'Bosnia and Herzegovina':-9,
 'Scotland':-4,'Morocco':-1,'Brazil':-3,'Haiti':-4,
 'USA':-4,'Australia':-4,'Türkiye':-3,'Paraguay':-11,
 'Germany':0,"Côte d'Ivoire":-3,'Ecuador':-2,'Curaçao':-5,
 'Sweden':-3,'Japan':0,'Netherlands':-3,'Tunisia':-1,
 'New Zealand':-2,'IR Iran':-2,'Belgium':-7,'Egypt':-3,
 'Uruguay':-2,'Saudi Arabia':-3,'Spain':-1,'Cabo Verde':-3,
 'Norway':0,'France':0,'Senegal':0,'Iraq':-2,
 'Argentina':-2,'Austria':-3,'Jordan':-1,'Algeria':-1,
 'Colombia':-3,'Congo DR':-2,'Portugal':-4,'Uzbekistan':-2,
 'England':-1,'Ghana':-2,'Panama':-3,'Croatia':-1,
}
