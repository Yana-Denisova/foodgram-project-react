# Generated by Django 3.2.13 on 2022-07-28 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='dont_follow_yourself',
        ),
    ]
