from django.conf import settings
from django.db import migrations, models
from django.db.models.deletion import CASCADE


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KakeboMonth",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month", models.PositiveSmallIntegerField(default=1)),
                ("year", models.PositiveSmallIntegerField(default=1980)),
                ("budget", models.JSONField(default=dict)),
                ("spare_cost", models.TextField(blank=True, default="", null=True)),
                ("target_reach", models.TextField(blank=True, default="", null=True)),
                ("spare", models.FloatField(blank=True, default=0, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Kakebo Month",
            },
        ),
        migrations.CreateModel(
            name="KakeboWeek",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week", models.IntegerField(default=1)),
                (
                    "month",
                    models.ForeignKey(
                        on_delete=CASCADE,
                        to="django_kakebo.kakebomonth",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Kakebo Week",
            },
        ),
        migrations.CreateModel(
            name="UtilitiesCost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="KakeboWeekTable",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data_row", models.JSONField(default=dict)),
                (
                    "type_cost",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "basic necessities"),
                            (1, "optional"),
                            (2, "culture and leisure"),
                            (3, "extras and unexpected"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "kakebo",
                    models.ForeignKey(
                        on_delete=CASCADE,
                        to="django_kakebo.kakeboweek",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KakeboEndOfMonthBalance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("electricity", models.FloatField(default=0)),
                ("gas", models.FloatField(default=0)),
                ("tel_internet", models.FloatField(default=0)),
                ("water", models.FloatField(default=0)),
                ("waste", models.FloatField(default=0)),
                ("costs_data", models.JSONField(default=dict)),
                ("answer_1", models.TextField(blank=True, default="", null=True)),
                ("answer_2", models.TextField(blank=True, default="", null=True)),
                ("answer_3", models.TextField(blank=True, default="", null=True)),
                (
                    "conclusion",
                    models.PositiveSmallIntegerField(
                        choices=[(0, ""), (1, "yes"), (2, "almost"), (3, "no")],
                        default=0,
                    ),
                ),
                (
                    "month",
                    models.ForeignKey(
                        on_delete=CASCADE,
                        to="django_kakebo.kakebomonth",
                    ),
                ),
            ],
        ),
    ]
