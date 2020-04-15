# Generated by Django 2.0.3 on 2020-04-15 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20200415_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='操作人'),
        ),
        migrations.AlterField(
            model_name='order',
            name='saler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='售货员'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='Auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='审核人'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='purchaser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaser', to='app.Users', verbose_name='进货人'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='supplier',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='app.Supplier', verbose_name='进货厂商'),
        ),
        migrations.AlterField(
            model_name='return_record',
            name='Auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Users', verbose_name='审核人'),
        ),
        migrations.AlterField(
            model_name='return_record',
            name='returner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returner', to='app.Users', verbose_name='退货人'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goods', verbose_name='商品'),
        ),
    ]