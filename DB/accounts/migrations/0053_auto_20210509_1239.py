# Generated by Django 3.1.7 on 2021-05-09 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_auto_20210509_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.country', verbose_name='Страна'),
        ),
    ]
