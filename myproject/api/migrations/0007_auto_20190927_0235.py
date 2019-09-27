# Generated by Django 2.2.5 on 2019-09-26 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190927_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='accepted_user',
        ),
        migrations.RemoveField(
            model_name='question',
            name='num_of_answers',
        ),
        migrations.AddField(
            model_name='primaryimage',
            name='num_of_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='secondaryimage',
            name='is_a_match',
            field=models.BooleanField(default=False),
        ),
    ]
