# Generated by Django 4.2.4 on 2023-08-17 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230807_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
