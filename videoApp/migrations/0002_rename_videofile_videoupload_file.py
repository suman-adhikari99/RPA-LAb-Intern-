# Generated by Django 4.0.6 on 2022-07-20 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videoupload',
            old_name='videofile',
            new_name='file',
        ),
    ]