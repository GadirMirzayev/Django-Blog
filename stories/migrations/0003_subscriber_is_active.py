# Generated by Django 3.1.7 on 2021-04-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_auto_20210402_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
