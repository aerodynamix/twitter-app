# Generated by Django 3.1.6 on 2021-02-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersx', '0009_auto_20210211_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_time',
            field=models.CharField(default='02/11/2021 07:41:50 PM', max_length=40),
        ),
    ]
