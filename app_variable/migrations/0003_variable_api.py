# Generated by Django 2.1.5 on 2020-06-10 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0005_apicase_is_cookie'),
        ('app_variable', '0002_auto_20200603_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='api',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_api.ApiCase'),
            preserve_default=False,
        ),
    ]