# Generated by Django 2.2.5 on 2019-09-26 14:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20190926_2006'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='UserResponse',
        ),
    ]
