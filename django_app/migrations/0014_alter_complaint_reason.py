# Generated by Django 4.2.2 on 2023-06-28 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0013_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='reason',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Причина жалобы'),
        ),
    ]
