# Generated by Django 3.2.7 on 2021-10-27 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211027_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='answer',
            new_name='answer_link',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='question_link',
        ),
    ]