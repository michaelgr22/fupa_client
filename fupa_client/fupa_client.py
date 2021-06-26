from datetime import datetime
import collections

from .fupa_remote_datasource import FupaRemoteDatasource
from .models.match import Match
from .models.player import Player
from .models.standings_row import StandingsRow

from .repositories.league_repository import LeagueRepository
from .repositories.standings_repository import StandingsRepository


class FupaClient:

    def __init__(self, teamname, teamclass, season):
        self.teamname = teamname
        self.teamclass = teamclass
        self.season = season
        self.base_url = 'https://www.fupa.net'
        self.team_url = '{}/team/{}-{}-{}'.format(
            self.base_url, self.teamname, self.teamclass, self.season)

    def __team_url(self):
        return '{}/team/{}-{}-{}'.format(self.base_url, self.teamname, self.teamclass, self.season)

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
        league_repository = LeagueRepository(self.team_url)
        return league_repository.get_league()

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
        standings_repository = StandingsRepository(self.team_url)
        return standings_repository.get_standing()
