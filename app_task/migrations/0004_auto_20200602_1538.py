# Generated by Django 2.1.5 on 2020-06-02 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_task', '0003_test_report'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test_Report',
            new_name='TestReport',
        ),
    ]