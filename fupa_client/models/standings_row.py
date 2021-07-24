from .. import helper as helper

from .team import Team


class StandingsRow:

    def __init__(self, position, showname, teamname, teamclass, season, teamlink, teamimage, games, wins, draws, loses, goals, countered_goals, points):
        self.position = int(position) if isinstance(position, int) else None
        self.showname = showname
        self.teamname = teamname
        self.teamclass = teamclass
        self.season = season
        self.teamlink = teamlink
        self.teamimage = teamimage
        self.games = int(games) if isinstance(games, int) else None
        self.wins = int(wins) if isinstance(wins, int) else None
        self.draws = int(draws) if isinstance(draws, int) else None
        self.loses = int(loses) if isinstance(loses, int) else None
        self.goals = int(goals) if isinstance(goals, int) else None
        self.countered_goals = int(
            countered_goals) if isinstance(countered_goals, int) else None
        self.points = int(points) if isinstance(points, int) else None

    @classmethod
    def from_row_soup(cls, soup):
        spans = cls.__remove_spans_with_no_content(cls, soup.findAll('span'))
        index_of_number_of_games = cls.__find_index_of_number_of_games(cls,
                                                                       spans)  # needed because some rows have (Auf) and (Ab) behind names
        team = Team.from_team_link(
            helper.base_url + cls.__find_team_link(cls, soup))
        position = spans[0].text.split('.')[0]
        teamimage = soup.find('img')['src']
        games = spans[index_of_number_of_games].text
        wins = spans[index_of_number_of_games+1].text.split('-')[0]
        draws = spans[index_of_number_of_games+1].text.split('-')[1]
        loses = spans[index_of_number_of_games+1].text.split('-')[2]
        goals = spans[index_of_number_of_games+2].text.split(':')[0]
        countered_goals = spans[index_of_number_of_games +
                                2].text.split(':')[1]
        points = spans[index_of_number_of_games+4].text

        return cls(
            position=position,
            showname=team.showname,
            teamname=team.teamname,
            teamclass=team.teamclass,
            season=team.teamseason,
            teamlink=team.teamlink,
            teamimage=teamimage,
            games=games,
            wins=wins,
            draws=draws,
            loses=loses,
            goals=goals,
            countered_goals=countered_goals,
            points=points
        )

    def to_dict(self):
        return {'position': self.position, 'showname': self.showname, 'teamname': self.teamname, 'teamclass': self.teamclass, 'season': self.season, 'teamlink': self.teamlink, 'teamimage': self.teamimage, 'games': self.games, 'wins': self.wins, 'draws': self.draws,
                'loses': self.loses, 'goals': self.goals, 'countered_goals': self.countered_goals, 'points': self.points}

    def __remove_spans_with_no_content(self, spans):
        for span in spans:
            if not span.text:
                spans.remove(span)

        return spans

    def __find_index_of_number_of_games(self, spans):
        for i in range(len(spans)):
            if spans[i].text.isdigit():
                return i

    def __find_team_link(self, soup):
        return soup['href']
