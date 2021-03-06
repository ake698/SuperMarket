# Generated by Django 2.2.8 on 2020-04-17 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20200417_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-id'], 'verbose_name': '销售管理', 'verbose_name_plural': '销售管理'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='vip',
        ),
        migrations.AddField(
            model_name='purchase_record',
            name='good_count',
            field=models.IntegerField(default=0, verbose_name='订单商品数量'),
        ),
    ]
