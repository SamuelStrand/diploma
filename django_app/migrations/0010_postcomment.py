# Generated by Django 4.2.2 on 2023-06-27 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_app', '0009_delete_postcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='', max_length=300, verbose_name='Текст комментария')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='<small class="text-muted">DateTimeField</small><hr><br>', null=True, verbose_name='Дата и время создания')),
                ('article', models.ForeignKey(blank=True, default=None, help_text='<small class="text-muted">ForeignKey</small><hr><br>', null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_app.post', verbose_name='Статья')),
                ('user', models.ForeignKey(blank=True, default=None, help_text='<small class="text-muted">ForeignKey</small><hr><br>', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий к публикации',
                'verbose_name_plural': 'Комментарии к публикациям',
                'db_table': 'django_app_postcomment_model_table',
                'ordering': ('-created',),
            },
        ),
    ]
