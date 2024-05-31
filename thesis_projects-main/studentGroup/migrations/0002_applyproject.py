# Generated by Django 5.0.6 on 2024-05-29 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_projectitem_supervisor'),
        ('studentGroup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='applyProject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentGroup.studentgroup')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.projectitem')),
            ],
        ),
    ]