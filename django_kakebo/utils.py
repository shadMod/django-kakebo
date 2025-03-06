import logging
from datetime import datetime
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model

from .models import KakeboMonth, KakeboWeek
from .models.kakebo_week_table import KakeboWeekTable, KakeboCostColors

logger = logging.getLogger(__name__)
User = get_user_model()


def get_user_from_user_kakebo_composed(
    user_kakebo_composed: str, week_composed: bool = False
) -> tuple[User, KakeboMonth]:
    """
    Get user from user-kakebo composed.

    Args:
        user_kakebo_composed (str): The user-kakebo composed is a kakebo user pk field, month, year
            in one word (e.g. 'username-month-year').
        week_composed (bool, optional): Add me. Defaults to False.

    Returns:
        tuple[User, KakeboMonth]: Return user and KakeboMonth instance.
    """
    if not week_composed:
        user_pk, month, year = user_kakebo_composed.split("-")
    else:
        user_pk, year, week = user_kakebo_composed.split("-")
        month = datetime.strptime(f"{year}-{int(week) - 1}-1", "%Y-%W-%w").month

    user_model_pk_field = {getattr(settings, "USER_FIELD_KAKEBO", "username"): user_pk}
    user = get_user_model().objects.get(**user_model_pk_field)
    kakebo_month, created = KakeboMonth.objects.get_or_create(
        user=user, month=month, year=year
    )
    if created:
        logger.debug("Created new KakeboMonth instance %s", kakebo_month)
    return user, kakebo_month


def find_indices(data_list: list[Any], value_to_find: Any) -> list[int]:
    """Find indices of value_to_find in data_list.

    Args:
        data_list (list[Any]): List of values.
        value_to_find (Any): Value to find.

    Returns:
        list[int]: List of indices from data_list.
    """
    return [index for index, value in enumerate(data_list) if value == value_to_find]


def get_data_row_from_kakebo_week(
    kakebo_week: KakeboWeek, cost_name: str, row: int = 0, column: int = 0
) -> dict[str, Any] | None:
    """Get value from specific column and row from KakeboWeekTable data row.

    Args:
        kakebo_week (KakeboWeek): KakeboWeek instance.
        cost_name (str): Cost name from KakeboCostColors.
        row (int, optional): Row number. Defaults to 0.
        column (int, optional): Column number. Defaults to 0.

    Returns:
        dict[str, Any]: Value from specific column and row from KakeboWeekTable data row.
    """
    type_cost_index = KakeboCostColors.constant_choices.index(cost_name)
    kakebo_data_row = KakeboWeekTable.objects.get(
        kakebo=kakebo_week, type_cost=type_cost_index
    ).data_row

    if not any(
        kakebo_data_row
        and kakebo_data_row.get(f"{column}", "")
        and kakebo_data_row.get(f"{column}", "").get(f"{row}", "")
    ):
        return None

    return kakebo_data_row[f"{column}"][f"{row}"]


class KeyKakebo:
    """Kay kakebo class."""

    field_list = ["username", "month", "year"]

    @property
    def get_key_kakebo(self) -> str | None:
        """Get key kakebo from username, month and year.

        Returns:
            str | None: Return key kakebo. None if self has no request and kwargs attribute.
        """
        if hasattr(self, "request") and hasattr(self, "kwargs"):
            field_user = getattr(settings, "USER_FIELD_KAKEBO", self.field_list[0])
            username = getattr(self.request.user, field_user)
            return f"{username}-{self.kwargs[self.field_list[1]]}-{self.kwargs[self.field_list[2]]}"
        return None
