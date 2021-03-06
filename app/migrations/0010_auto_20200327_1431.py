# Generated by Django 2.0.3 on 2020-03-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_purchase_record_issubmit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='in_money',
            field=models.FloatField(default=0, verbose_name='收钱'),
        ),
        migrations.AlterField(
            model_name='order',
            name='out_money',
            field=models.FloatField(default=0, verbose_name='找零'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sales',
            field=models.ManyToManyField(null=True, to='app.Sale', verbose_name='销售记录'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sum_price',
            field=models.FloatField(default=0, verbose_name='总价格'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_num',
            field=models.IntegerField(default=0, verbose_name='销售数量'),
        ),
    ]
