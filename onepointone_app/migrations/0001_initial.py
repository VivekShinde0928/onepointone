# Generated by Django 2.1.15 on 2022-12-09 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.CharField(max_length=50)),
                ('doj', models.DateTimeField()),
                ('gender', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=50)),
                ('manager', models.CharField(max_length=50)),
                ('picture', models.FileField(blank=True, null=True, upload_to='pic/')),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'employee_data',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LoginDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'login',
                'managed': True,
            },
        ),
    ]