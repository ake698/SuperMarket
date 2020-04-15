# Generated by Django 2.0.3 on 2020-03-27 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200325_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='in_money',
            field=models.FloatField(verbose_name='收钱'),
        ),
        migrations.AlterField(
            model_name='order',
            name='out_money',
            field=models.FloatField(verbose_name='找零'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='purchases',
            field=models.ManyToManyField(blank=True, null=True, to='app.Purchase', verbose_name='进货记录'),
        ),
    ]
