# Generated by Django 2.0.3 on 2020-04-15 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20200415_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_record',
            name='supplier',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Supplier', verbose_name='进货厂商'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='cost_price',
            field=models.FloatField(default=0, verbose_name='进货单价'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='margin',
            field=models.FloatField(default=20, max_length=4, verbose_name='利润率%'),
        ),
    ]
