# Generated by Django 2.1.15 on 2022-12-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onepointone_app', '0003_auto_20221209_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedata',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
