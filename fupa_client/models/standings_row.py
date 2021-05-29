class StandingsRow:

    def __init__(self, position, teamname, teamimage, games, wins, draws, loses, goals, countered_goals, points):
        self.position = int(position) if position else None
        self.teamname = teamname
        self.teamimage = teamimage
        self.games = int(games) if games else None
        self.wins = int(wins) if wins else None
        self.draws = int(draws) if draws else None
        self.loses = int(loses) if loses else None
        self.goals = int(goals) if goals else None
        self.countered_goals = int(
            countered_goals) if countered_goals else None
        self.points = int(points) if points else None

    @classmethod
    def from_row_soup(cls, soup):
        spans = cls.__remove_spans_with_no_content(cls, soup.findAll('span'))
        index_of_number_of_games = cls.__find_index_of_number_of_games(cls,
                                                                       spans)  # needed because some rows have (Auf) and (Ab) behind names
        return cls(
            position=spans[0].text.split('.')[0],
            teamname=spans[1].text,
            teamimage=soup.find('img')['src'],
            games=spans[index_of_number_of_games].text,
            wins=spans[index_of_number_of_games+1].text.split('-')[0],
            draws=spans[index_of_number_of_games+1].text.split('-')[1],
            loses=spans[index_of_number_of_games+1].text.split('-')[2],
            goals=spans[index_of_number_of_games+2].text.split(':')[0],
            countered_goals=spans[index_of_number_of_games +
                                  2].text.split(':')[1],
            points=spans[index_of_number_of_games+4].text
        )

    def to_dict(self):
        return {'position': self.position, 'teamname': self.teamname, 'teamimage': self.teamimage, 'games': self.games, 'wins': self.wins, 'draws': self.draws,
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
