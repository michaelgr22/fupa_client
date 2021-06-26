from . import helper

from .repositories.league_repository import LeagueRepository
from .repositories.standings_repository import StandingsRepository
from .repositories.squad_repository import SquadRepository
from .repositories.matches_repository import MatchesRepository


class FupaClient:

    def __init__(self, teamname, teamclass, season):
        self.teamname = teamname
        self.teamclass = teamclass
        self.season = season
        self.team_url = '{}/team/{}-{}-{}'.format(
            helper.base_url, self.teamname, self.teamclass, self.season)
        self.squad_repository = SquadRepository(self.team_url)
        self.matches_repository = MatchesRepository(self.team_url)
        self.standings_repository = StandingsRepository(self.team_url)
        self.league_repository = LeagueRepository(self.team_url)

    def get_squad(self):
        return self.squad_repository.get_squad()

    def get_league(self):
        return self.league_repository.get_league()

    def get_matches(self):
        return self.matches_repository.get_matches()

    def get_match_from_link(self, link):
        return self.matches_repository.get_match_from_link(link)

    def get_standing(self):
        return self.standings_repository.get_standing()
