# Generated by Django 4.2.3 on 2023-07-12 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_alter_newrequestmodel_email_alter_ordermodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newrequestmodel',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
