# Generated by Django 2.0.3 on 2020-03-27 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200327_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_record',
            name='state',
            field=models.CharField(choices=[('1', '已通过审核'), ('2', '暂未审核'), ('3', '拒绝')], default='2', max_length=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='Auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='审核人'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='sum_price',
            field=models.FloatField(default=0, verbose_name='总价格'),
        ),
    ]
