# Generated by Django 5.1.1 on 2024-10-03 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_alter_apirequest_request_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequest',
            name='request_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
