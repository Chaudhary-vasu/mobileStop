# Generated by Django 4.2 on 2023-05-01 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_customer_city_alter_customer_locality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
    ]
