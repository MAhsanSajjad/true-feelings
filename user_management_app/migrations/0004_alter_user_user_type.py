# Generated by Django 5.1.6 on 2025-02-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_app', '0003_alter_user_city_alter_user_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('representative', 'Representative')], default='admin', max_length=255),
        ),
    ]
