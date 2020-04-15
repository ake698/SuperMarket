# Generated by Django 2.0.3 on 2020-03-28 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200328_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='saler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Users', verbose_name='售货员'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='Auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Users', verbose_name='审核人'),
        ),
        migrations.AlterField(
            model_name='purchase_record',
            name='purchaser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='purchaser', to='app.Users', verbose_name='进货人'),
        ),
    ]
