# Generated by Django 5.2.1 on 2025-05-15 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourapp', '0005_remove_vendor_company_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tourstatus',
            old_name='title',
            new_name='status',
        ),
    ]
