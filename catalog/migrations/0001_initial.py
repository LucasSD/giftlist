# Generated by Django 3.1.7 on 2021-05-18 09:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('est', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a gift category (e.g. electronics or clothes)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the country the gift was made in', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Enter a brief description of the gift', max_length=1000)),
                ('ref', models.CharField(help_text='Enter a product code or similar as a reference', max_length=20, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('url', models.URLField()),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='gifts', to='catalog.brand')),
                ('category', models.ManyToManyField(help_text='Select a category for this gift', to='catalog.Category')),
                ('made_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.country')),
            ],
        ),
        migrations.CreateModel(
            name='GiftInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this specific gift requested by a single user', primary_key=True, serialize=False)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('a', 'Available'), ('t', 'Taken')], default='a', help_text='Gift availability', max_length=1)),
                ('gift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.gift')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='gift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='brands', to='catalog.gift'),
        ),
    ]
