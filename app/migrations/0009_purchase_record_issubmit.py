# Generated by Django 2.0.3 on 2020-03-27 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200327_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_record',
            name='isSubmit',
            field=models.BooleanField(default=False, verbose_name='是否提交'),
        ),
    ]
