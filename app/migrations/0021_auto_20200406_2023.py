# Generated by Django 2.0.3 on 2020-04-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='profile',
            field=models.FloatField(default=0, verbose_name='销售利润'),
        ),
    ]
