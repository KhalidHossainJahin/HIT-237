# Generated by Django 5.0.6 on 2024-05-30 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
