# Generated by Django 3.1.7 on 2021-03-29 20:37

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_delete_residenceaddres'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='area', chained_model_field='area_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.city'),
            preserve_default=False,
        ),
    ]
