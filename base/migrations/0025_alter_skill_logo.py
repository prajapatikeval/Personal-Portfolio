# Generated by Django 4.2.5 on 2023-11-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_profilepicture_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='logo',
            field=models.ImageField(default='skill.jpeg', null=True, upload_to=''),
        ),
    ]
