# Generated by Django 4.1 on 2022-09-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_alter_choice_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=60),
        ),
    ]
