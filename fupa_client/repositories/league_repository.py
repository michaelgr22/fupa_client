from ..models.league import League
from ..models.team import Team
from .. import helper as helper


class LeagueRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_league_as_dict(self):
        league = self.__league()
        return league.to_dict()

    def get_league(self):
        return self.__league()

    def __league_url(self):
        soup = helper.soup_of_page(self.team_url)
        league_url = soup.select_one("a[href*=league]")['href']
        return helper.base_url + league_url

    def __season(self):
        team = Team.from_team_link(self.team_url)
        return team.teamseason

    def __league(self):
        url = self.__league_url()
        return League.from_link(url, self.__season())
