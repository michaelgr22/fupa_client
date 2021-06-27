from .. import helper as helper


class Team:
    def __init__(self, showname, teamname, teamclass, teamseason, teamlink):
        self.showname = showname
        self.teamname = teamname
        self.teamclass = teamclass
        self.teamseason = teamseason
        self.teamlink = teamlink

    @classmethod
    def from_team_link(cls, link):
        soup = helper.soup_of_page(link)
        showname = soup.find('h1').text
        team_identifier = cls.__extract_team_identifier_from_teamlink(
            cls, link)

        return cls(
            showname=showname,
            teamname=team_identifier['teamname'],
            teamclass=team_identifier['teamclass'],
            teamseason=team_identifier['season'],
            teamlink=link
        )

    def to_dict(self):
        return {'showname': self.showname, 'teamname': self.teamname, 'teamclass': self.teamclass, 'teamseason': self.teamseason, 'teamlink': self.teamlink}

    def __extract_team_identifier_from_teamlink(self, link):
        team = {}
        splitted_link = link.split('/')
        for i in range(len(splitted_link)):
            if splitted_link[i] == 'team':
                team_identifiers = splitted_link[i + 1].split('-')
                team['teamname'] = '-'.join(
                    team_identifiers[:len(team_identifiers)-3])
                team['teamclass'] = team_identifiers[len(team_identifiers)-3]
                team['season'] = '-'.join(team_identifiers[-2:])
        return team
