# Generated by Django 2.2.8 on 2020-04-17 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20200417_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_record',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Supplier', verbose_name='进货厂商'),
        ),
    ]