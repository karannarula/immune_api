# Generated by Django 2.2 on 2019-11-13 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_user', '0003_auto_20191113_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='status_bit',
            field=models.IntegerField(default=0),
        ),
    ]
