def extract_team_identifier_from_teamlink(link):
    team = {}
    splitted_link = link.split('/')
    for i in range(len(splitted_link)):
        if splitted_link[i] == 'team':
            team_identifiers = splitted_link[i + 1].split('-')
            team['teamname'] = '-'.join(
                team_identifiers[:len(team_identifiers)-3])
            team['teamclass'] = team_identifiers[len(team_identifiers)-3]
            team['season'] = '-'.join(team_identifiers[-2:])
    return team


def extract_league_identifier_from_leaguelink(link):
    league = {}
    splitted_link = link.split('/')
    for i in range(len(splitted_link)):
        if splitted_link[i] == 'league':
            league['leaguename'] = splitted_link[i + 1]
        if splitted_link[i] == 'season':
            league['season'] = splitted_link[i + 1]
    return league
