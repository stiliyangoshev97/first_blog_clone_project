# Generated by Django 3.1.4 on 2021-01-06 00:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210106_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 6, 2, 16, 57, 727417)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 6, 0, 16, 57, 726889, tzinfo=utc)),
        ),
    ]
