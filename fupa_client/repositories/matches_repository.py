from time import sleep

from .. import helper as helper
from ..models.match import Match
from ..models.team import Team


class MatchesRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_matches(self):
        matches_soups = self.__matches_of_team()
        matches_list = []
        for match_soup in matches_soups:
            match = self.__match_soup_to_dict(match_soup)
            if match is not None:
                matches_list.append(match)
            sleep(2)
        return matches_list

    def get_match_from_link(self, link):
        match = Match.from_match_link(link)
        return match.to_dict()

    def __matches_of_team(self):
        team = Team.from_team_link(self.team_url)
        soup = helper.soup_of_page(self.team_url + '/matches')
        selector = 'a[href*={}-{}][href*=\/match][enablehover*=true]'.format(
            team.teamname, team.teamclass)
        return soup.select(selector)

    def __match_soup_to_dict(self, soup):
        link = helper.base_url + soup['href']
        try:
            match = Match.from_match_link(link)
            if match is not None:
                return match.to_dict()
            return None
        except Exception as e:
            print(e) + " " + link
            return None
