# Generated by Django 2.1.5 on 2019-02-03 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0004_auto_20190203_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='name',
        ),
    ]
