# Generated by Django 4.2.7 on 2023-11-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_question_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(),
        ),
    ]
