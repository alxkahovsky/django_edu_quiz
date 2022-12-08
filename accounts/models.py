from django.db import models
from django.utils import timezone
from django.conf import settings


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    slug = models.SlugField(max_length=200, unique=False, verbose_name='User')
    available = models.BooleanField(default=True, verbose_name='Актуальность')
    created = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')
    updated = models.DateField(blank=True, null=True, default=timezone.now, verbose_name='Дата ред-ия записи')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Зарегистрированный пользователь'
        verbose_name_plural = 'Зарегистрированные пользователи'

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)
