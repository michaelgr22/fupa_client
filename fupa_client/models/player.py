from datetime import datetime

from .. import helper as helper


class Player:

    def __init__(self, firstname, surname, birthday, deployments, goals, position, imagelink, playerlink):
        self.firstname = firstname
        self.surname = surname
        self.birthday = birthday
        self.deployments = int(deployments) if deployments else None
        self.goals = int(goals) if goals else None
        self.position = position
        self.imagelink = imagelink
        self.playerlink = playerlink

    @classmethod
    def from_squad_soup(cls, soup):
        positions = ('Torwart', 'Abwehr', 'Mittelfeld', 'Angriff')

        spans = cls.__find_spans_in_base_soup(cls, soup)
        playerlink = cls.__find_player_link(cls, soup)
        playersoup = helper.soup_of_page(playerlink)

        firstname = spans[0].text.split(' ')[0]
        surname = spans[0].text.split(' ')[1]
        birthday = cls.__find_birthday(cls, playersoup)
        deployments = spans[2].text.split(' ')[0]
        goals = spans[3].text.split(' ')[0]
        position = cls.__find_position(cls, playersoup)
        imagelink = soup.find('img')['src']

        if position in positions and deployments.isdigit() and goals.isdigit():
            return cls(
                firstname=firstname,
                surname=surname,
                birthday=birthday,
                deployments=deployments,
                goals=goals,
                position=position,
                imagelink=imagelink,
                playerlink=playerlink
            )
        return None

    def to_dict(self):
        return {'firstname': self.firstname, 'surname': self.surname, 'birthday': self.birthday, 'deployments': self.deployments,
                'goals': self.goals, 'position': self.position, 'imagelink': self.imagelink, 'playerlink': self.playerlink}

    def __find_spans_in_base_soup(self, soup):
        datasoup = soup.findChildren(
            'a', recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('div', recursive=False)[1]
        return datasoup.findAll('span')

    def __find_player_link(self, soup):
        return helper.base_url + soup.find('a')['href']

    def __find_position(self, soup):
        spans = soup.findAll('span')
        for i in range(len(spans)):
            if spans[i].text == 'Position':
                return spans[i+1].text

    def __find_birthday(self, soup):
        spans = soup.findAll('span')
        for i in range(len(spans)):
            if spans[i].text == 'Geburtstag':
                try:
                    return datetime.strptime(spans[i+1].text, '%d.%m.%Y').strftime('%Y-%m-%d %H:%M:%S')
                except:
                    return None
