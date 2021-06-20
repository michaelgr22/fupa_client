from .. import helper as helper


class League:
    def __init__(self, showname, leaguename, season, leaguelink):
        self.showname = showname
        self.leaguename = leaguename
        self.season = season
        self.leaguelink = leaguelink

    @classmethod
    def from_link(cls, showname, link):
        league_identifier = helper.extract_league_identifier_from_leaguelink(
            link)
        return cls(
            showname=showname,
            leaguename=league_identifier['leaguename'],
            season=league_identifier['season'],
            leaguelink=link
        )

    def to_dict(self):
        return {'showname': self.showname, 'leaguename': self.leaguename, 'season': self.season, 'leaguelink': self.leaguelink}
