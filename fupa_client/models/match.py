from datetime import datetime

from .. import helper as helper
from .team import Team


class Match:

    def __init__(self, date_time, match_link, home_showname, home_teamname, home_teamclass, home_season, home_link, home_image, home_goals, away_showname, away_teamname, away_teamclass, away_season, away_link, away_image, away_goals, cancelled, league):
        self.date_time = date_time
        self.match_link = match_link
        self.home_showname = home_showname
        self.home_teamname = home_teamname
        self.home_teamclass = home_teamclass
        self.home_season = home_season
        self.home_link = home_link
        self.home_image = home_image
        self.home_goals = int(home_goals) if home_goals else None
        self.away_showname = away_showname
        self.away_teamname = away_teamname
        self.away_teamclass = away_teamclass
        self.away_season = away_season
        self.away_link = away_link
        self.away_image = away_image
        self.away_goals = int(away_goals) if away_goals else None
        self.cancelled = cancelled
        self.league = league

    @classmethod
    def from_match_link(cls, link):
        soup = helper.soup_of_page(link)
        teams = cls.__find_teams(cls, soup)
        images = cls.__find_images_of_teams(cls, soup)
        result = cls.__find_result(cls, soup)
        league = cls.__find_league(cls, soup)
        date_time = cls.__find_date_time(cls, link)

        return cls(
            date_time=date_time,
            match_link=link,
            home_showname=teams[0].showname,
            home_teamname=teams[0].teamname,
            home_teamclass=teams[0].teamclass,
            home_season=teams[0].teamseason,
            home_link=teams[0].teamlink,
            home_image=images['home_image'],
            home_goals=result['home_goals'],
            away_showname=teams[1].showname,
            away_teamname=teams[1].teamname,
            away_teamclass=teams[1].teamclass,
            away_season=teams[1].teamseason,
            away_link=teams[1].teamlink,
            away_image=images['away_image'],
            away_goals=result['away_goals'],
            cancelled=result['cancelled'],
            league=league
        )

    def to_dict(self):
        return {'date_time': self.date_time, 'match_link': self.match_link, 'home_showname': self.home_showname, 'home_teamname': self.home_teamname, 'home_teamclass': self.home_teamclass, 'home_season': self.home_season, 'home_link': self.home_link, 'home_image': self.home_image, 'home_goals': self.home_goals,
                'away_showname': self.away_showname, 'away_teamname': self.away_teamname, 'away_teamclass': self.away_teamclass, 'away_season': self.away_season, 'away_link': self.away_link, 'away_image': self.away_image, 'away_goals': self.away_goals, 'cancelled': self.cancelled, 'league': self.league}

    def __find_teams(self, soup):
        selector = "a[href*=\/team]"
        team_links = list(dict.fromkeys(
            list(map(lambda a: helper.base_url + a['href'], soup.select(selector)))))
        return list(map(lambda link: Team.from_team_link(link), team_links))

    def __find_images_of_teams(self, soup):
        images = soup.select('img')
        return {'home_image': images[0]['src'], 'away_image': images[1]['src']}

    def __find_result(self, soup):
        selector = "a[href*=\/team]"
        spans = soup.select_one(selector).parent.parent.findAll('span')
        cancelled = self.__is_cancelled(self, spans)
        if cancelled:
            return {'home_goals': None, 'away_goals': None, 'cancelled': cancelled}
        result = self.__find_string_with_colon_in_spans(self, spans)
        if not result or not self.__is_valid_result(self, result):
            return {'home_goals': None, 'away_goals': None, 'cancelled': cancelled}
        return {'home_goals': int(result.split(':')[0]), 'away_goals': int(result.split(':')[1]), 'cancelled': cancelled}

    def __find_league(self, soup):
        link = helper.base_url + soup.find('h2').parent.parent['href']
        soup = helper.soup_of_page(link)
        return soup.find('h1').text

    def __find_date_time(self, link):
        info_link = link + '/info'
        soup = helper.soup_of_page(info_link)
        spans = soup.findAll('span')
        for i in range(len(spans)):
            if spans[i].text.startswith('Anstoß'):
                time = spans[i].text.split(' ')[2]
                date = spans[i+1].text.split(' ')[1]
                return datetime.strptime("{} {}".format(date, time), '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')

    def __find_string_with_colon_in_spans(self, spans):
        for span in spans:
            if ':' in span.text:
                return span.text
        return None

    def __is_valid_result(self, result_string):
        if result_string.split(':')[0].isdigit() and result_string.split(':')[1].isdigit():
            return True
        return False

    def __is_cancelled(self, spans):
        for span in spans:
            if 'abgesagt' in span.text:
                return True
        return False
