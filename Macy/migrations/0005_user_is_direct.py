# Generated by Django 3.1.4 on 2021-02-18 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Macy', '0004_user_direct_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_direct',
            field=models.BooleanField(default=False),
        ),
    ]