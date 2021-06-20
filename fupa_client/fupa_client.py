from datetime import datetime
import collections

from .fupa_remote_datasource import FupaRemoteDatasource
from .models.match import Match
from .models.player import Player
from .models.standings_row import StandingsRow
from .models.league import League


class FupaClient:

    def __init__(self, teamname, teamclass, season):
        self.teamname = teamname
        self.teamclass = teamclass
        self.season = season
        self.base_url = 'https://www.fupa.net'

    def __team_url(self):
        return '{}/team/{}-{}-{}'.format(self.base_url, self.teamname, self.teamclass, self.season)

    def __league_url(self):
        soup = self.__soup_of_page(self.__team_url())
        league_url = soup.select_one("a[href*=league]")['href']
        return self.base_url + league_url

    def __league_name_on_league_soup(self, soup):
        return soup.find('h1').text

    def __soup_of_page(self, url):
        datasource = FupaRemoteDatasource(url)
        soup = datasource.scrap_page()
        if not soup:
            raise Exception('false url' + url)
        return soup

    def get_squad(self):
        soup = self.__soup_of_page(self.__team_url())
        positions = ('Torwart', 'Abwehr', 'Mittelfeld', 'Angriff')

        squad = []
        for position in positions:
            parent = soup.find('h3', text=position).parent
            for child in parent.findChildren('div', recursive=False):
                player = Player.from_squad_soup(child, position)
                squad.append(player.to_dict())

        return squad

    def get_league(self):
        url = self.__league_url()
        soup = self.__soup_of_page(self.__league_url() + '/standing')
        league_name = self.__league_name_on_league_soup(soup)
        league = League(league_name, url)
        return league.to_dict()

    def get_matches(self):
        soup = self.__soup_of_page(self.__team_url() + '/matches')
        selector = 'a[href*={}-{}][href*=\/match][enablehover*=true]'.format(
            self.teamname, self.teamclass)
        matches_soup = soup.select(selector)

        leagues_and_dates = self.__leagues_and_dates_for_matches(soup)

        matches = []
        for match_soup in matches_soup:
            date = match_soup.parent['id']
            league = self.__find_league_of_match(
                datetime.strptime(date, '%Y-%m-%d'), leagues_and_dates)
            match_link = self.base_url + match_soup['href']
            match_div = self.__soup_of_page(match_link).find(
                'a', href='/team/{}-{}-{}'.format(self.teamname, self.teamclass, self.season)).parent.parent
            match = None
            try:
                match = Match.from_match_soup(
                    match_div, date, league, match_link, self.base_url)
            except:
                pass
            if match:
                matches.append(match.to_dict())

        return matches

    def __find_league_of_match(self, match_date, leagues_and_dates):
        league_of_match = next(iter(leagues_and_dates.values()))
        for date, league in leagues_and_dates.items():
            if match_date >= date:
                league_of_match = league

        return league_of_match

    def __leagues_and_dates_for_matches(self, soup):
        leagues = soup.findAll('h3')

        league_and_dates = {}
        for league in leagues:
            date = datetime.strptime(league.parent['id'], '%Y-%m-%d')
            league_and_dates[date] = league.text

        return collections.OrderedDict(sorted(league_and_dates.items()))

    def get_standing(self):
        soup = self.__soup_of_page(self.__league_url() + '/standing')
        league_name = self.__league_name_on_league_soup(soup)
        selector = "a[href*=\/team]"
        tablerows_soup = soup.select(selector)

        standings = {'league': league_name, 'standings': []}
        for tablerow_soup in tablerows_soup:
            standings_row = StandingsRow.from_row_soup(
                tablerow_soup, self.base_url)
            standings['standings'].append(standings_row.to_dict())

        return standings
