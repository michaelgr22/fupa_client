from ..models.team import Team
from .. import helper as helper


class TeamRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_team(self):
        team = Team.from_team_link(self.team_url)
        return team.to_dict()
