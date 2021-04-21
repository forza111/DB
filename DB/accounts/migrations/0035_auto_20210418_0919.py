# Generated by Django 3.1.7 on 2021-04-18 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_credittarget'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='name',
        ),
        migrations.AddField(
            model_name='credit',
            name='target',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='cr', to='accounts.credittarget', verbose_name='Назначение кредита'),
            preserve_default=False,
        ),
    ]