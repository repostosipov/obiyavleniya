# Generated by Django 4.1.1 on 2022-12-04 11:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_help_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='help',
            name='phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Телефон должнен быть похож на: '+999999999'. ", regex='^\\+?1?\\d{9,15}$')], verbose_name='Телефон'),
        ),
    ]
