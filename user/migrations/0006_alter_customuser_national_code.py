# Generated by Django 5.0.2 on 2024-02-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_customuser_user_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
