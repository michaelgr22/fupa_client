from .fupa_remote_datasource import FupaRemoteDatasource

base_url = 'https://www.fupa.net'


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
    league = {'leaguename': None, 'season': None}
    splitted_link = link.split('/')
    for i in range(len(splitted_link)):
        if splitted_link[i] == 'league':
            league['leaguename'] = splitted_link[i + 1]
        if splitted_link[i] == 'season':
            league['season'] = splitted_link[i + 1]
    return league


def soup_of_page(url):
    datasource = FupaRemoteDatasource(url)
    soup = datasource.scrap_page()
    if not soup:
        raise Exception('false url' + url)
    return soup
