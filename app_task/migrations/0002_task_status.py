# Generated by Django 2.1.5 on 2020-05-07 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.SmallIntegerField(choices=[('0', '未执行'), ('1', '执行中'), ('2', '已完成')], default='0', verbose_name='状态'),
        ),
    ]
