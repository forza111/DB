# Generated by Django 3.1.7 on 2021-04-08 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_card_paymentsystem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='paymentsystem',
        ),
        migrations.AddField(
            model_name='card',
            name='paymentsystem',
            field=models.ManyToManyField(related_name='paymentsystem_card', to='accounts.PaymentSystem', verbose_name='тип платежной системы'),
        ),
    ]