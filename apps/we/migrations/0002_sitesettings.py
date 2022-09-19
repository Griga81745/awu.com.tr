# Generated by Django 4.0.6 on 2022-08-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('we', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support_email', models.EmailField(default='support@example.com', max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
