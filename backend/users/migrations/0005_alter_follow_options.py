# Generated by Django 3.2.13 on 2022-07-31 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_follow_unique_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('-id',)},
        ),
    ]