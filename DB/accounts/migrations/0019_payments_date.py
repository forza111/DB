# Generated by Django 3.1.7 on 2021-04-01 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210401_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Дата платежа'),
        ),
    ]
