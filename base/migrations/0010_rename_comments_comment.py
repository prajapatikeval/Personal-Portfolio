# Generated by Django 4.2.3 on 2023-09-19 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='comments',
            new_name='Comment',
        ),
    ]
