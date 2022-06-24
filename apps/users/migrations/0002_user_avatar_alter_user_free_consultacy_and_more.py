# Generated by Django 4.0.4 on 2022-06-21 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='users/avatars/default.jpg', upload_to='users/avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='free_consultacy',
            field=models.BooleanField(default=False, verbose_name='Free Consultacy?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_lawyer',
            field=models.BooleanField(default=False, verbose_name='Is Lawyer?'),
        ),
    ]
