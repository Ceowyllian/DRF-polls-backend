# Generated by Django 4.1 on 2022-11-07 13:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('polls', '0002_alter_question_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=60, validators=[django.core.validators.MaxLengthValidator(limit_value=60,
                                                                                                        message='Choice text must less than 60 characters long.')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(limit_value=20,
                                                                                                         message='Question text must be at least 20 characters long.'),
                                                               django.core.validators.MaxLengthValidator(
                                                                   limit_value=200,
                                                                   message='Question title must less than 200 characters long.')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_title',
            field=models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(limit_value=40,
                                                                                                        message='Question title must be at least 40 characters long.'),
                                                              django.core.validators.MaxLengthValidator(limit_value=40,
                                                                                                        message='Question title must less than 40 characters long.')]),
        ),
    ]
