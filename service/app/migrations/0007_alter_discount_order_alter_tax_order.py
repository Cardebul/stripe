# Generated by Django 5.0 on 2023-12-24 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_price_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='order',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='discounts',
                to='app.order'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='order',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='taxs',
                to='app.order'),
        ),
    ]