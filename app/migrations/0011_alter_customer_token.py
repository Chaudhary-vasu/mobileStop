# Generated by Django 4.2 on 2023-05-02 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_customer_city_alter_customer_locality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='token',
            field=models.CharField(default='', max_length=200),
        ),
    ]
