# Generated by Django 3.1.4 on 2021-02-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Macy', '0003_auto_20210212_0539'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='direct_link',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
