# Generated by Django 3.1.6 on 2021-02-10 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersx', '0003_auto_20210210_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='modified_time',
            field=models.CharField(default='02/10/2021 06:59:20 PM', max_length=50),
        ),
    ]