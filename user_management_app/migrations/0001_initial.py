# Generated by Django 5.1.6 on 2025-02-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(blank=True, max_length=60, null=True, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('full_name', models.CharField(blank=True, max_length=128, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('whatsapp_no', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=30, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='Logo/User_logo')),
                ('social_platform', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('google', 'Google'), ('apple', 'Apple')], max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('user_type', models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('representative', 'Representative')], default='user', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
