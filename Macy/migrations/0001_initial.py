# Generated by Django 3.1.4 on 2021-03-02 00:05

import Macy.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('intro', models.TextField(blank=True, null=True)),
                ('profile', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('header', models.ImageField(blank=True, null=True, upload_to='header/')),
                ('direct_link', models.URLField(blank=True, max_length=255, null=True)),
                ('is_direct', models.BooleanField(default=False)),
                ('username', models.CharField(help_text='150 characters or fewer.', max_length=150)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', Macy.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(blank=True, max_length=150)),
                ('media_choice', models.CharField(choices=[('TWT', 'Twitter'), ('INS', 'Instagram'), ('TIK', 'TikTok'), ('FBK', 'Facebook'), ('YTB', 'Youtube'), ('LNE', 'LINE'), ('MIS', 'Other')], default='MIS', max_length=3)),
                ('link', models.URLField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
