# Generated by Django 4.2.3 on 2023-08-02 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_remove_question_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
    ]
