# Generated by Django 4.1.1 on 2022-11-27 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_help_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='help',
            options={'ordering': ('-created',), 'verbose_name': 'Обращение в техподдежку', 'verbose_name_plural': 'Обращения в техподдежку'},
        ),
    ]
