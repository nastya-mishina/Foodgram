# Generated by Django 3.2 on 2021-05-23 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='units',
            new_name='dimension',
        ),
    ]