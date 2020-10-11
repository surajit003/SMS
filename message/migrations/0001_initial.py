# Generated by Django 3.1.2 on 2020-10-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('account_number', models.CharField(help_text='accountnumber,username,accountid,apikey', max_length=100)),
                ('api_url', models.URLField(blank=True, null=True)),
                ('password', models.CharField(max_length=100)),
                ('configured_sender', models.CharField(max_length=120)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Gateway Detail',
                'verbose_name_plural': 'Gateway Details',
            },
        ),
    ]
