# Generated by Django 3.2.4 on 2021-07-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='est',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
