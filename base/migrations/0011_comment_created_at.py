# Generated by Django 4.2.3 on 2023-09-19 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_rename_comments_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
