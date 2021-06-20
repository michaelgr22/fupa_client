from datetime import datetime
from dateutil import tz


class Match:

    def __init__(self, date_time, match_link, home_name, home_link, home_image, home_goals, away_name, away_link, away_image, away_goals, cancelled, league):
        self.date_time = date_time
        self.match_link = match_link
        self.home_name = home_name
        self.home_link = home_link
        self.home_image = home_image
        self.home_goals = int(home_goals) if home_goals else None
        self.away_name = away_name
        self.away_link = away_link
        self.away_image = away_image
        self.away_goals = int(away_goals) if away_goals else None
        self.cancelled = cancelled
        self.league = league

    @classmethod
    def from_match_soup(cls, soup, date, league, match_link, base_url):
        spans = soup.findAll('span')
        time_or_result_str = cls.__find_string_with_colon(cls, spans)
        finished = not cls.__is_time(cls, time_or_result_str)
        cancelled = cls.__is_cancelled(cls, soup)
        result = cls.__result(cls, time_or_result_str, finished, cancelled)
        team_links = cls.__find_team_links(cls, soup, base_url)
        team_images = cls.__images_of_teams(cls, soup)
        return cls(
            date_time=cls.__date_time(cls, date, time_or_result_str, finished),
            match_link=match_link,
            home_name=spans[0].text,
            home_link=team_links['home_link'],
            home_image=team_images['home_image'],
            home_goals=result[0] if result else None,
            away_name=spans[-1].text,
            away_link=team_links['away_link'],
            away_image=team_images['away_image'],
            away_goals=result[1] if result else None,
            cancelled=cancelled,
            league=league
        )

    def to_dict(self):
        return {'date_time': self.date_time, 'match_link': self.match_link, 'home_name': self.home_name, 'home_link': self.home_link, 'home_image': self.home_image, 'home_goals': self.home_goals,
                'away_name': self.away_name, 'away_link': self.away_link, 'away_image': self.away_image, 'away_goals': self.away_goals, 'cancelled': self.cancelled, 'league': self.league}

    def __date_time(self, date, time_string, finished):
        if finished:
            return '{} {}'.format(date, '00:00:00')
        else:
            time = time_string.split(' ')[1] + ':00'
            utc_datetime = datetime.strptime(
                '{} {}'.format(date, time), '%Y-%m-%d %H:%M:%S')
            return self.__convert_datetime_to_local(self, utc_datetime).strftime('%Y-%m-%d %H:%M:%S')

    def __result(self, result_string, finished, cancelled):
        if finished and not cancelled and self.__is_valid_result(self, result_string):
            return [int(result_string.split(':')[0]), int(result_string.split(':')[1])]
        return None

    def __is_valid_result(self, result_string):
        if result_string.split(':')[0].isdigit() and result_string.split(':')[1].isdigit():
            return True
        return False

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
        images = soup.select('img')
        return {'home_image': images[0]['src'], 'away_image': images[1]['src']}

    def __convert_datetime_to_local(self, utc_datetime):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Berlin')
        utc_datetime = utc_datetime.replace(tzinfo=from_zone)
        return utc_datetime.astimezone(to_zone)

    def __find_team_links(self, soup, base_url):
        selector = "a[href*=\/team]"
        teams = list(dict.fromkeys(
            list(map(lambda links: links['href'], soup.select(selector)))))
        return {'home_link': base_url + teams[0], 'away_link': base_url + teams[1]}
