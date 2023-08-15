from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
                ("year", models.IntegerField(default=1)),
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
            ],
        ),
    ]
