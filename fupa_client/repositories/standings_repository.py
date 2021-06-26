from .. import helper as helper
from ..models.standings_row import StandingsRow
from .league_repository import LeagueRepository


class StandingsRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_standing(self):
        league_repository = LeagueRepository(self.team_url)
        league = league_repository.get_league()

        return {'league': league['showname'], 'standings': self.__standings_rows(league['leaguelink'])}

    def __standings_rows(self, link):
        soup = helper.soup_of_page(link + '/standing')
        selector = "a[href*=\/team]"
        rows = soup.select(selector)
        return list(map(self.__row_soup_to_dict, rows))

    def __row_soup_to_dict(self, soup):
        standings_row = StandingsRow.from_row_soup(soup)
        return standings_row.to_dict()
