# Generated by Django 2.0.3 on 2020-03-27 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200327_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='img',
        ),
        migrations.AlterField(
            model_name='order',
            name='good_count',
            field=models.IntegerField(default=0, verbose_name='订单商品数量'),
        ),
    ]
