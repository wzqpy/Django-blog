# Generated by Django 2.1.3 on 2018-11-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatars/default.png', upload_to='avatars/'),
        ),
    ]
