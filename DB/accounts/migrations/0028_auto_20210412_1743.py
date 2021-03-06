# Generated by Django 3.1.7 on 2021-04-12 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20210408_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='score_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='score123', to='accounts.score', verbose_name='Счет'),
        ),
        migrations.AlterField(
            model_name='score',
            name='bank_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.bankname', verbose_name='Банк'),
        ),
    ]
