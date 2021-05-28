from .fupa_remote_datasource import FupaRemoteDatasource
from .models.player import Player


class FupaClient:

    def __init__(self, teamname, teamclass, season):
        self.teamname = teamname
        self.teamclass = teamclass
        self.season = season
        self.base_url = 'https://www.fupa.net/'

    def __team_url(self):
        return '{}team/{}-{}-{}'.format(self.base_url, self.teamname, self.teamclass, self.season)

    def get_squad(self):
        datasource = FupaRemoteDatasource(self.__team_url())
        soup = datasource.scrap_page()
        positions = ('Torwart', 'Abwehr', 'Mittelfeld', 'Angriff')

        squad = []
        for position in positions:
            parent = soup.find('h3', text=position).parent
            for child in parent.findChildren('div', recursive=False):
                player = Player.from_squad_soup(child, position)
                squad.append(player.to_dict())

        return squad
