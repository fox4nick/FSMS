# Generated by Django 4.2.3 on 2023-07-12 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_newrequestmodel_status_alter_ordermodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newrequestmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='email',
            field=models.EmailField(blank=True, max_length=50),
        ),
    ]
