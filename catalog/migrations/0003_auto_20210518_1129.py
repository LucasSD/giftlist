# Generated by Django 3.2.3 on 2021-05-18 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210518_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='gift',
        ),
        migrations.AlterField(
            model_name='gift',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.brand'),
        ),
    ]
