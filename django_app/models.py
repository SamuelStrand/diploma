from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name='Автор',
        help_text='<small class="text-muted">ForeignKey</small><hr><br>',
        to=User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        validators=[MinLengthValidator(0), MaxLengthValidator(300), ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default='',
        verbose_name='Заголовок',
        help_text='<small class="text-muted">CharField [0, 300]</small><hr><br>',
        max_length=300,
    )

    description = models.TextField(
        validators=[MinLengthValidator(0), MaxLengthValidator(3000), ],
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name='Описание',
        help_text='<small class="text-muted">TextField [0, 3000]</small><hr><br>',

        max_length=3000,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name='Цена',
    )

    created = models.DateTimeField(
        editable=True,
        blank=True,
        null=True,
        default=timezone.now,
        verbose_name='Дата и время создания',
        help_text='<small class="text-muted">DateTimeField</small><hr><br>',
        auto_now=False,
        auto_now_add=False,
    )
    updated = models.DateTimeField(
        editable=True,
        blank=True,
        null=True,
        default=timezone.now,
        verbose_name='Дата и время обновления',
        help_text='<small class="text-muted">DateTimeField</small><hr><br>',

        auto_now=False,
        auto_now_add=False,
    )
    image = models.ImageField(
        upload_to='ads/%Y/%m/%d/',
        blank=True)
    is_liked = models.BooleanField(
        editable=True,
        blank=True,
        null=True,
        default=False,
        verbose_name='Избранное',
        help_text='<small class="text-muted">BooleanField</small><hr><br>',
    )

    class Meta:
        app_label = 'django_app'
        ordering = ('-updated', 'title')
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        db_table = 'django_app_post_model_table'

    def __str__(self):
        return f"{self.title}({self.id}) | {self.description[0:30]}... | {self.updated}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profiles/%Y/%m/%d/',
        blank=True)
    first_name = models.CharField(
        validators=[MinLengthValidator(0), MaxLengthValidator(300), ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default='',
        verbose_name='Имя',
        help_text='<small class="text-muted">CharField [0, 300]</small><hr><br>',
        max_length=300,
    )
    last_name = models.CharField(
        validators=[MinLengthValidator(0), MaxLengthValidator(300), ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default='',
        verbose_name='Фамилия',
        help_text='<small class="text-muted">CharField [0, 300]</small><hr><br>',
        max_length=300,
    )
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=20, default='')

    class Meta:
        app_label = 'django_app'
        ordering = ('id', 'user')
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'django_app_profile_model_table'

    def __str__(self):
        return f"{self.user}({self.id})"
