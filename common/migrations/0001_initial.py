# Generated by Django 3.2.19 on 2024-04-23 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInterfaceSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_header', models.CharField(default='IntelICH Administration', max_length=255)),
                ('site_title', models.CharField(default='IntelICH site admin', max_length=255)),
                ('index_title', models.CharField(default='Site administration', max_length=255)),
            ],
        ),
    ]
