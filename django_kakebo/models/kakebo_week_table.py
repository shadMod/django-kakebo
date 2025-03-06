from django.db import models

from .kakebo_week import KakeboWeek


class KakeboCostColors:
    BASIC = "basic necessities", "orange"
    OPTIONAL = "optional", "green"
    LEISURE = "culture and leisure", "mediumvioletred"
    EXTRAS = "extras and unexpected", "steelblue"

    @classmethod
    @property
    def type_list(cls) -> list[str]:
        return [
            key
            for key, constant in cls.__dict__.items()
            if isinstance(constant, tuple) and len(constant) == 2
        ]

    @classmethod
    @property
    def colors_costs(cls) -> list[str]:
        return [
            constant[1]
            for _, constant in cls.__dict__.items()
            if isinstance(constant, tuple) and len(constant) == 2
        ]

    @classmethod
    @property
    def constant_choices(cls) -> list[str]:
        return [
            constant[0]
            for constant in cls.__dict__.values()
            if isinstance(constant, tuple) and len(constant) == 2
        ]

    @classmethod
    @property
    def choices(cls) -> list[tuple[int, str]]:
        """Return a list of tuples describing the colors available.

        Returns:
            list[tuple[int, str]]: List of tuples describing the colors available.
        """
        return [
            (index, constant) for index, constant in enumerate(cls.constant_choices)
        ]


class KakeboWeekTable(models.Model):
    """Kakebo week table model."""

    kakebo = models.ForeignKey(KakeboWeek, on_delete=models.CASCADE)
    data_row: dict = models.JSONField(default=dict)
    type_cost: int = models.PositiveSmallIntegerField(
        choices=KakeboCostColors.choices, default=0
    )

    @property
    def display_type_cost_color(self) -> str:
        """Displays the type cost color.

        Returns:
            str: Type cost color.
        """
        return KakeboCostColors.colors_costs[self.type_cost]

    @property
    def display_total_table(self) -> float:
        """Displays the total table for this week.

        Returns:
            float: Total table for this week.
        """
        return sum([self.total_column(i) for i in range(len(self.data_row))])

    @property
    def list_sort_cost(self) -> list:
        """Returns the list of costs for this week.

        Returns:
            list: List of costs for this week.
        """
        data = []
        for row in self.data_row.values():
            data.extend([value for value in row.values()])
        return sorted(
            [value for value in data], key=lambda value: value["value"], reverse=True
        )

    def get_column(self, column_index: int) -> list[tuple[str, int]]:
        """Get rows with description and value from determinate column.

        Args:
            column_index (int): Column index.

        Returns:
            list[tuple[str, int]]: Return column with description and value.
        """
        column = self.data_row.get(f"{column_index}")
        if column:
            return [
                (value.get("desc", ""), value.get("value", 0))
                for value in column.values()
            ]
        return []

    def get_cell(self, column_index: int, row_number: int) -> tuple[str, int]:
        """Get cell with description and value from determinate column index.

        Args:
            column_index (int): Column index.
            row_number (int): Row index.

        Returns:
            tuple[str, int]: Return cell with description and value.
        """
        return self.get_column(column_index)[row_number]

    def get_list_sort_cost(self, max_row: int) -> list[tuple[str, int]]:
        """Returns the list of costs for this week.

        Args:
            max_row (int): Maximum row index.

        Returns:
            list[tuple[str, int]]: Return list of costs for this week with description and value.
        """
        max_row -= 1
        list_cost = self.list_sort_cost[:max_row]
        if list_cost:
            other_cost = 0
            for i in self.list_sort_cost[max_row:]:
                other_cost += i["value"]
            if len(list_cost) >= max_row:
                list_cost.append({"desc": "others", "value": other_cost})
        return list_cost

    def total_column(self, column_index: int) -> int | float:
        """Returns the total column for this week.

        Args:
            column_index (int): Column index.

        Returns:
            int | float: Total column for this week.
        """
        column = self.get_column(column_index)
        return sum([cell[1] for cell in column]) if column else 0
