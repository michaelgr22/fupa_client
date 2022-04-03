# Client to get data from fupa.net

[fupa.net](https://www.fupa.net) is a website providing squads, standings, games and results for German amateur soccer leagues.
With this package you can load the provided data of your team to implement it to your website or app.

Example:
https://www.fupa.net/team/vfb-franken-schillingsfuerst-m1-2021-22

```python
from fupa_client import FupaClient
    
teamname = 'vfb-franken-schillingsfuerst'
teamclass = 'm1'
season = '2021-22'
client = FupaClient(teamname, teamclass, season)
```

## Functions
```python
client.get_squad()
```
**Output:**
```
[{'firstname': 'Thorsten', 'surname': 'Leopoldseder', 'birthday': None, 'deployments': 0, 'goals': 0, 'position': 'Torwart', 'imagelink': 'https://image.fupa.net/player/sTNGSHLIdyAr/64x64.jpeg', 'playerlink': 'https://www.fupa.net/player/thorsten-leopoldseder-492365'}, ...]
```
------------------------
```python
client.get_league()
```
**Output:**
```
{'showname': 'Kreisliga Nürnberg/Frankenhöhe 1', 'leaguename': 'kreisliga-nuernberg-frankenhoehe-1', 'season': '2021-22', 'leaguelink': 'https://www.fupa.net/league/kreisliga-nuernberg-frankenhoehe-1'}
```
-----------------
```python
client.get_matches()
```
**Output:**
```
[{'date_time': '2022-03-27 15:00:00', 'match_link': 'https://www.fupa.net/match/tsv-markt-erlbach-m1-vfb-franken-schillingsfuerst-m1-220327', 'home_showname': 'TSV Markt Erlbach', 'home_teamname': 'tsv-markt-erlbach', 'home_teamclass': 'm1', 'home_season': '2021-22', 'home_link': 'https://www.fupa.net/team/tsv-markt-erlbach-m1-2021-22', 'home_image': 'https://image.fupa.net/club/jXjFMlM0z32X/32x32.jpeg', 'home_goals': 2, 'away_showname': 'VfB Franken Schillingsfürst', 'away_teamname': 'vfb-franken-schillingsfuerst', 'away_teamclass': 'm1', 'away_season': '2021-22', 'away_link': 'https://www.fupa.net/team/vfb-franken-schillingsfuerst-m1-2021-22', 'away_image': 'https://image.fupa.net/club/Q7Ici8KBaFhw/32x32.jpeg', 'away_goals': 1, 'cancelled': False, 'league_showname': 'KL1, 21. Spieltag', 'league_name': 'KL1, 21. Spieltag', 'league_link': None}, ...]
```
--------------------------
```python
client.get_match_from_link("https://www.fupa.net/match/vfb-franken-schillingsfuerst-m1-sv-mosbach-m1-220514")
```
**Output:**
```
{'date_time': '2022-05-14 16:00:00', 'match_link': 'https://www.fupa.net/match/vfb-franken-schillingsfuerst-m1-sv-mosbach-m1-220514', 'home_showname': 'VfB Franken Schillingsfürst', 'home_teamname': 'vfb-franken-schillingsfuerst', 'home_teamclass': 'm1', 'home_season': '2021-22', 'home_link': 'https://www.fupa.net/team/vfb-franken-schillingsfuerst-m1-2021-22', 'home_image': 'https://image.fupa.net/club/Q7Ici8KBaFhw/32x32.jpeg', 'home_goals': None, 'away_showname': 'SV Mosbach', 'away_teamname': 'sv-mosbach', 'away_teamclass': 'm1', 'away_season': '2021-22', 'away_link': 'https://www.fupa.net/team/sv-mosbach-m1-2021-22', 'away_image': 'https://image.fupa.net/club/eitrbYQRt33q/32x32.jpeg', 'away_goals': None, 'cancelled': False, 'league_showname': 'KL1, 28. Spieltag', 'league_name': 'KL1, 28. Spieltag', 'league_link': None}
```
-----------------
```python
client.get_standing()
```
**Output:**
```
{'league_showname': 'Kreisliga Nürnberg/Frankenhöhe 1', 'league_name': 'kreisliga-nuernberg-frankenhoehe-1', 'league_season': '2021-22', 'leaguelink': 'https://www.fupa.net/league/kreisliga-nuernberg-frankenhoehe-1', 'standings': [{'position': 1, 'showname': '1. FV Uffenheim', 'teamname': '1-fv-uffenheim', 'teamclass': 'm1', 'season': '2021-22', 'teamlink': 'https://www.fupa.net/team/1-fv-uffenheim-m1-2021-22', 'teamimage': 'https://image.fupa.net/club/HQgKofsBEQX2/32x32.jpeg', 'games': 21, 'wins': 16, 'draws': 4, 'loses': 1, 'goals': 56, 'countered_goals': 20, 'points': 52}, {'position': 2, 'showname': 'TV Markt Weiltingen', 'teamname': 'tv-markt-weiltingen', 'teamclass': 'm1', 'season': '2021-22', 'teamlink': 'https://www.fupa.net/team/tv-markt-weiltingen-m1-2021-22', 'teamimage': 'https://image.fupa.net/club/mUSqPT2HtTE4/32x32.jpeg', 'games': 21, 'wins': 13, 'draws': 3, 'loses': 5, 'goals': 51, 'countered_goals': 27, 'points': 42},...]}
```
-----------------
```python
client.get_team()
```
**Output:**
```
{'showname': 'VfB Franken Schillingsfürst', 'teamname': 'vfb-franken-schillingsfuerst', 'teamclass': 'm1', 'teamseason': '2021-22', 'teamlink': 'https://www.fupa.net/team/vfb-franken-schillingsfuerst-m1-2021-22'}
