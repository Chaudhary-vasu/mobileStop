# Generated by Django 4.2 on 2023-05-02 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_customer_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='token',
            field=models.CharField(max_length=200),
        ),
    ]
