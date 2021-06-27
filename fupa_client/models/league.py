from .. import helper as helper


class League:
    def __init__(self, showname, leaguename, season, leaguelink):
        self.showname = showname
        self.leaguename = leaguename
        self.season = season
        self.leaguelink = leaguelink

    @classmethod
    def from_link(cls, link):
        soup = helper.soup_of_page(link + '/standing')
        showname = cls.__league_name_on_league_soup(cls, soup)
        league_identifier = cls.__extract_league_identifier_from_leaguelink(
            cls, link)
        return cls(
            showname=showname,
            leaguename=league_identifier['leaguename'],
            season=league_identifier['season'],
            leaguelink=link
        )

    def to_dict(self):
        return {'showname': self.showname, 'leaguename': self.leaguename, 'season': self.season, 'leaguelink': self.leaguelink}

    def __league_name_on_league_soup(self, soup):
        return soup.find('h1').text

    def __extract_league_identifier_from_leaguelink(self, link):
        league = {'leaguename': None, 'season': None}
        splitted_link = link.split('/')
        for i in range(len(splitted_link)):
            if splitted_link[i] == 'league':
                league['leaguename'] = splitted_link[i + 1]
            if splitted_link[i] == 'season':
                league['season'] = splitted_link[i + 1]
        return league
