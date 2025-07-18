# Generated by Django 5.1.6 on 2025-04-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management_app', '0007_transactionhistroy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='representatives/documents/'),
        ),
        migrations.AddField(
            model_name='user',
            name='fixed_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='per_call_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='salary_type',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')], default='monthly', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='services',
            field=models.CharField(blank=True, choices=[('standard', 'Standard'), ('advance', 'Advance')], default='standard', max_length=255, null=True),
        ),
    ]
