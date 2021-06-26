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
        team_identifier = helper.extract_team_identifier_from_teamlink(link)

        return cls(
            showname=showname,
            teamname=team_identifier['teamname'],
            teamclass=team_identifier['teamclass'],
            teamseason=team_identifier['season'],
            teamlink=link
        )
