# Generated by Django 4.2.2 on 2023-08-19 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_session_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='property_img',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]