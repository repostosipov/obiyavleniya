# Generated by Django 4.1.1 on 2022-10-29 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Цена'),
        ),
    ]
