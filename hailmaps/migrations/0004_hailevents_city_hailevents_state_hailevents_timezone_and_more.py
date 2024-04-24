# Generated by Django 5.0.4 on 2024-04-24 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hailmaps', '0003_alter_hailevents_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='hailevents',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='hailevents',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AddField(
            model_name='hailevents',
            name='timezone',
            field=models.CharField(default='UTC', max_length=50),
        ),
        migrations.AddField(
            model_name='hailevents',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]