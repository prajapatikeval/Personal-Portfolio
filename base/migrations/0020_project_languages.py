# Generated by Django 4.2.5 on 2023-11-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_remove_project_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='languages',
            field=models.ManyToManyField(to='base.language'),
        ),
    ]