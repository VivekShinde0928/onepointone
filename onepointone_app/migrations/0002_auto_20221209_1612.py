# Generated by Django 2.1.15 on 2022-12-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onepointone_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeedata',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='logindetails',
            name='updated_at',
            field=models.DateTimeField(default=None),
        ),
    ]
