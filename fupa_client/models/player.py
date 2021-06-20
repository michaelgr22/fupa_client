class Player:

    def __init__(self, firstname, surname, age, deployments, goals, position, imagelink):
        self.firstname = firstname
        self.surname = surname
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
        firstname = spans[0].text.split(' ')[0]
        surname = spans[0].text.split(' ')[1]
        return cls(
            firstname=firstname,
            surname=surname,
            age=spans[1].text.split(' ')[0],
            deployments=spans[2].text.split(' ')[0],
            goals=spans[3].text.split(' ')[0],
            position=position,
            imagelink=soup.find('img')['src'],
        )

    def to_dict(self):
        return {'firstname': self.firstname, 'surname': self.surname, 'age':  self.age, 'deployments': self.deployments,
                'goals': self.goals, 'position': self.position, 'imagelink': self.imagelink}
