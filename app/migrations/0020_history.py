# Generated by Django 2.0.3 on 2020-03-28 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20200328_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(max_length=100, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(default='-', max_length=200, verbose_name='操作记录')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Users', verbose_name='操作人')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'ordering': ['-id'],
            },
        ),
    ]
