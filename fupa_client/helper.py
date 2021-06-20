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
