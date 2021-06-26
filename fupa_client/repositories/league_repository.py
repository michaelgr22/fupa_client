from ..models.league import League
from .. import helper as helper


class LeagueRepository:
    def __init__(self, base_url, team_url):
        self.base_url = base_url
        self.team_url = team_url

    def get_league(self):
        url = self.__league_url()
        league = League.from_link(url)
        return league.to_dict()

    def __league_url(self):
        soup = helper.soup_of_page(self.team_url)
        league_url = soup.select_one("a[href*=league]")['href']
        return self.base_url + league_url
