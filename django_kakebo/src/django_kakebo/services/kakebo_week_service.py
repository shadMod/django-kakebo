from datetime import datetime

from ..types import KakeboYearWeek


class KakeboWeekService:
    def __init__(self):
        self.year = 2025
        self.week = 1

    def get_last_week(self, year: int, day: int = None):
        if day is None:
            day = 31
        last_day = datetime(year, 12, day)
        last_week = last_day.isocalendar()[1]
        if last_week == 1:
            return self.get_last_week(year, day - 1)
        return last_week

    def get_previous_year_week(
        self, year: int = None, week: int = None
    ) -> KakeboYearWeek:
        if week == 0:
            return KakeboYearWeek(year=year, week=self.get_last_week(year))
        else:
            return KakeboYearWeek(year=year, week=week)

    def get_next_year_week(self, year: int = None, week: int = None) -> KakeboYearWeek:
        if week == self.get_last_week(year):
            return KakeboYearWeek(year=year + 1, week=1)
        else:
            # +2: python start from 0, so have to do +1+1, so +2
            return KakeboYearWeek(year=year, week=week + 2)
