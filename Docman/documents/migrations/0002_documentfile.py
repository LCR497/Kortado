# Generated by Django 5.1 on 2024-08-21 02:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='documents.document')),
            ],
        ),
    ]
