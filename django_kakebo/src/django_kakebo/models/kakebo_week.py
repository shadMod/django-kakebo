from datetime import datetime, date, timedelta

from django.conf import settings
from django.db import models

from .kakebo_month import KakeboMonth

User = settings.AUTH_USER_MODEL


class KakeboWeek(models.Model):
    """Kakebo week model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.ForeignKey(KakeboMonth, on_delete=models.CASCADE)
    week = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Kakebo Week"

    def __str__(self) -> str:
        """Return string representation of Kakebo week.

        Returns:
            str: String representation of Kakebo week.
        """
        return f"{self.user.username}'s Kakebo - {self.display_start_week} // {self.display_end_week}"

    @property
    def display_start_week(self) -> date:
        """Displays the start week for this week.

        Returns:
            date: Start week for this week.
        """
        year_week = f"{self.month.year}-{self.week}-1"
        return datetime.strptime(year_week, "%Y-%W-%w").date()

    @property
    def display_end_week(self) -> date:
        """Displays the end week for this week.

        Returns:
            date: End week for this week.
        """
        return self.display_start_week + timedelta(days=6)

    def get_total_week(self) -> list[int]:
        """Get total week for this week.

        Returns:
            list[int]: Return all total table from self week.
        """
        from .kakebo_week_table import KakeboWeekTable

        return [
            kakebo_week_table.display_total_table
            for kakebo_week_table in KakeboWeekTable.objects.filter(kakebo=self)
        ]

    @property
    def sum_total_week(self) -> int:
        """Returns the total week for this week.

        Returns:
            int: Total week for this week.
        """
        return sum(self.get_total_week())
