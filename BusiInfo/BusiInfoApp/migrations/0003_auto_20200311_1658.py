# Generated by Django 3.0.1 on 2020-03-11 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusiInfoApp', '0002_auto_20200311_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='Email',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
