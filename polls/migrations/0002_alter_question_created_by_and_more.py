# Generated by Django 4.1 on 2022-10-31 07:31

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(limit_value=20,
                                                                                                         message='Question text must be at least 20 characters long.')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_title',
            field=models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(limit_value=20,
                                                                                                        message='Question title must be at least 20 characters long.')]),
        ),
    ]