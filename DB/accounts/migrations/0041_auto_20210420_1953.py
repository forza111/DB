# Generated by Django 3.1.7 on 2021-04-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0040_auto_20210419_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditinfo',
            name='total_rate',
            field=models.DecimalField(blank=True, decimal_places=18, max_digits=20, null=True, verbose_name='Общая ставка'),
        ),
        migrations.AlterField(
            model_name='creditinfo',
            name='interest_rate_mounth',
            field=models.DecimalField(blank=True, decimal_places=18, max_digits=20, null=True, verbose_name='Процентная ставка за месяц'),
        ),
    ]
