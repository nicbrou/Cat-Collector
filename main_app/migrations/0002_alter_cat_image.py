# Generated by Django 4.0.2 on 2022-03-28 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='image',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]
