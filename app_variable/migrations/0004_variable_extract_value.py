# Generated by Django 2.1.5 on 2020-06-10 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_variable', '0003_variable_api'),
    ]

    operations = [
        migrations.AddField(
            model_name='variable',
            name='extract_value',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='提取值'),
        ),
    ]