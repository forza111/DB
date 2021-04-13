# Generated by Django 3.1.7 on 2021-04-13 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_card_type_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='score',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='score_card', to='accounts.score', verbose_name='банковская карта'),
        ),
    ]
