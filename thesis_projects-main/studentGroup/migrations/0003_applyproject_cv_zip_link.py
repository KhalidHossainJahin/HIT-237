# Generated by Django 5.0.6 on 2024-05-29 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentGroup', '0002_applyproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyproject',
            name='cv_zip_link',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]