# Generated by Django 3.1.6 on 2021-02-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersx', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='modified_time',
            field=models.CharField(default='02/10/2021 05:54:30 PM', max_length=50),
        ),
    ]
