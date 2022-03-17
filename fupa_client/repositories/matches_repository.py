from time import sleep
from datetime import datetime, timedelta

from .. import helper as helper
from ..models.match import Match
from ..models.team import Team
from .league_repository import LeagueRepository


class MatchesRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_matches_as_dict(self):
        matches_soups = self.__matches_of_team(previous=True) + self.__matches_of_team(previous=False)
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
            sleep(3)
        return matches_list

    def __matches_of_team(self, previous):
        team = Team.from_team_link(self.team_url)
        link = self.team_url + '/matches' if previous == False else self.team_url + \
            '/matches?pointer=prev'
        soup = helper.soup_of_page(link)
        selector = 'a[href*={}-{}][href*=\/match][enablehover*=true]'.format(
            team.teamname, team.teamclass)
        return soup.select(selector)

    def __matches_of_league(self):
        league_repository = LeagueRepository(self.team_url)
        league = league_repository.get_league()

        last_sunday = self.__find_date_of_last_sunday().strftime('%Y-%m-%d')
        link = league.leaguelink + '/matches?date=' + last_sunday

        selector = 'a[href*=\/match][enablehover*=true]'
        soup = helper.soup_of_page(link)
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

    def __find_date_of_last_sunday(self):
        return datetime.now() - timedelta(days=(datetime.now().isoweekday() % 7))
