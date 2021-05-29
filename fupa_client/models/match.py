from bs4 import BeautifulSoup as _BeautifulSoup
from datetime import datetime
from dateutil import tz


class Match:

    def __init__(self, date_time, home_name, home_image, home_goals, away_name, away_image, away_goals, cancelled, league):
        self.date_time = date_time
        self.home_name = home_name
        self.home_image = home_image
        self.home_goals = home_goals
        self.away_name = away_name
        self.away_image = away_image
        self.away_goals = away_goals
        self.cancelled = cancelled
        self.league = league

    @classmethod
    def from_match_soup(cls, soup, date, league):
        spans = soup.findAll('span')
        time_or_result_str = cls.__find_string_with_colon(cls, spans)
        finished = not cls.__is_time(cls, time_or_result_str)
        cancelled = cls.__is_cancelled(cls, soup)
        return cls(
            date_time=cls.__date_time(cls, date, time_or_result_str, finished),
            home_name=spans[0].text,
            home_image=cls.__images_of_teams(cls, soup)[0]['src'],
            home_goals=cls.__result(cls, time_or_result_str)[
                0] if finished and not cancelled else None,
            away_name=spans[-1].text,
            away_image=cls.__images_of_teams(cls, soup)[1]['src'],
            away_goals=cls.__result(cls, time_or_result_str)[
                1] if finished and not cancelled else None,
            cancelled=cancelled,
            league=league
        )

    def to_dict(self):
        return {'date_time': self.date_time, 'home_name': self.home_name, 'home_image': self.home_image, 'home_goals': self.home_goals,
                'away_name': self.away_name, 'away_image': self.away_image, 'away_goals': self.away_goals, 'cancelled': self.cancelled, 'league': self.league}

    def __date_time(self, date, time_string, finished):
        if finished:
            return '{} {}'.format(date, '00:00:00')
        else:
            time = time_string.split(' ')[1] + ':00'
            utc_datetime = datetime.strptime(
                '{} {}'.format(date, time), '%Y-%m-%d %H:%M:%S')
            return self.__convert_datetime_to_local(self, utc_datetime).strftime('%Y-%m-%d %H:%M:%S')

    def __result(self, result_string):
        return result_string.split(':')

    def __is_time(self, string):
        if string is None:
            return False
        days = ('Mo, Di, Mi, Do, Fr, Sa, So')
        for day in days:
            if string.startswith(day):
                return True
        return False

    def __is_cancelled(self, spans):
        for span in spans:
            if 'abgesagt' in span.text:
                return True
        return False

    def __find_string_with_colon(self, spans):
        for span in spans:
            if ':' in span.text:
                return span.text
        return None

    def __images_of_teams(self, soup):
        return soup.select('img')

    def __convert_datetime_to_local(self, utc_datetime):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Berlin')
        utc_datetime = utc_datetime.replace(tzinfo=from_zone)
        return utc_datetime.astimezone(to_zone)
