# Generated by Django 3.1.7 on 2021-04-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20210421_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditinfo',
            name='deadline_mounth',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Срок кредита, мес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditinfo',
            name='interest_charges',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Начисленные проценты'),
        ),
        migrations.AlterField(
            model_name='creditinfo',
            name='total_debt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Долг + проценты'),
        ),
    ]