class Player:

    def __init__(self, name, age, deployments, goals, position, imagelink):
        self.name = name
        self.age = int(age) if age else None
        self.deployments = int(deployments) if deployments else None
        self.goals = int(goals) if goals else None
        self.position = position
        self.imagelink = imagelink

    @classmethod
    def from_squad_soup(cls, soup, position):
        datasoup = soup.findChildren(
            'a', recursive=False)[0].findChildren('div', recursive=False)[0].findChildren('div', recursive=False)[1]
        spans = datasoup.findAll('span')
        return cls(
            name=spans[0].text,
            age=spans[1].text.split(' ')[0],
            deployments=spans[2].text.split(' ')[0],
            goals=spans[3].text.split(' ')[0],
            position=position,
            imagelink=soup.find('img')['src'],
        )

    def to_dict(self):
        return {'name': self.name, 'age':  self.age, 'deployments': self.deployments,
                'goals': self.goals, 'position': self.position, 'imagelink': self.imagelink}
