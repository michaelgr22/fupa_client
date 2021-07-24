from time import sleep

from .. import helper as helper
from ..models.match import Match
from ..models.team import Team
from .league_repository import LeagueRepository


class MatchesRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_matches_as_dict(self):
        matches_soups = self.__matches_of_team()
        return self.__create_matches_from_soup(matches_soups)

    def get_match_from_link_as_dict(self, link):
        match = Match.from_match_link(link)
        return match.to_dict()

    def get_matches_of_league_as_dict(self):
        matches_soup = self.__matches_of_league()
        return self.__create_matches_from_soup(matches_soup)

    def __create_matches_from_soup(self, soup):
        matches_list = []
        for match_soup in soup:
            match = self.__match_soup_to_dict(match_soup)
            if match is not None:
                matches_list.append(match)
            sleep(5)
        return matches_list

    def __matches_of_team(self):
        team = Team.from_team_link(self.team_url)
        soup = helper.soup_of_page(self.team_url + '/matches')
        selector = 'a[href*={}-{}][href*=\/match][enablehover*=true]'.format(
            team.teamname, team.teamclass)
        return soup.select(selector)

    def __matches_of_league(self):
        league_repository = LeagueRepository(self.team_url)
        league = league_repository.get_league()
        selector = 'a[href*=\/match][enablehover*=true]'
        soup = helper.soup_of_page(league.leaguelink + '/matches')
        return soup.select(selector)

    def __match_soup_to_dict(self, soup):
        link = helper.base_url + soup['href']
        try:
            match = Match.from_match_link(link)
            if match is not None:
                return match.to_dict()
            return None
        except Exception as e:
            print('{}-{}'.format(e, link))
            return None
