import sys

from .. import helper as helper
from ..models.player import Player


class SquadRepository:
    def __init__(self, team_url):
        self.team_url = team_url

    def get_squad(self):
        return self.__players()

    def __players(self):
        soup = helper.soup_of_page(self.team_url)
        selector = "a[enablehover*=true][href*=\/player]"
        players = soup.select(selector)
        return [player for player in map(self.__player_soup_to_dict, players) if player is not None]

    def __player_soup_to_dict(self, soup):
        try:
            player = Player.from_squad_soup(soup.parent)
            if player is not None:
                return player.to_dict()
        except Exception as e:
            print(e)
