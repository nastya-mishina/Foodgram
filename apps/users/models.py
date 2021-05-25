from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'USR', 'User'
    ADMIN = 'ADM', 'Admin'


class User(AbstractUser):

    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(
        'Логин',
        blank=False,
        unique=True,
        max_length=50,
        error_messages={
            'unique': "Пользователь с таким username уже существует.",
        },
    )
    role = models.CharField(
        default=Role.USER, choices=Role.choices, max_length=8)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser


class Follow(models.Model):
    author = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='follow', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'user'), name='unique_following')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'user: {self.user.username}, author: {self.author.username}'
