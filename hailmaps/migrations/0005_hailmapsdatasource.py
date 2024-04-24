# Generated by Django 5.0.4 on 2024-04-24 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hailmaps', '0004_hailevents_city_hailevents_state_hailevents_timezone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HailmapsDataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('source_type', models.CharField(choices=[('csv_file', 'CSV File'), ('api', 'API'), ('webpage', 'Webpage')], max_length=50)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('file_path', models.CharField(blank=True, max_length=255)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Hail Map Data Source',
                'verbose_name_plural': 'Hail Map Data Sources',
                'ordering': ['name'],
                'permissions': [('can_manage_data_sources', 'Can manage hail map data sources')],
                'unique_together': {('name', 'source_type')},
            },
        ),
    ]