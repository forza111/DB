# Generated by Django 3.1.7 on 2021-03-28 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.country'),
        ),
    ]
