# Generated by Django 3.0.3 on 2020-02-14 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialektor', '0005_auto_20200210_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metadata',
            name='id',
        ),
        migrations.AlterField(
            model_name='metadata',
            name='fileID',
            field=models.CharField(default='defaultID', max_length=100, primary_key=True, serialize=False),
        ),
    ]