# Generated by Django 4.2.5 on 2023-09-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_doctor',
            field=models.BooleanField(null=True),
        ),
    ]
