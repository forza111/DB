# Generated by Django 3.1.7 on 2021-04-01 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0022_auto_20210401_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cr', to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
    ]
