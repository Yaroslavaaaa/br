from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from bookrev import settings


# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Автор")
    genre = models.ForeignKey("Genres", on_delete=models.PROTECT, verbose_name="Жанр")
    description = models.TextField(verbose_name="Описание")
    pub_date = models.IntegerField(verbose_name="Год выпуска")
    image = models.ImageField(upload_to="photos/bookphoto/%Y/%m/%d/", verbose_name="Изображение")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    user = models.ForeignKey("CustomUser", verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['title']


class Genres(models.Model):
    genre_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


    def __str__(self):
        return self.genre_name


    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})


    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class CustomUser(AbstractUser):
    # Добавляем новые поля в модель пользователя
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='photos/avatars/%Y/%m/%d/', default='photos/avatars/no_avatar.jpg')
    role = models.ForeignKey("Roles", on_delete=models.PROTECT, default=1)


    def __str__(self):
        return self.username


    def get_absolute_url(self):
        return reverse('user', kwargs={'user_username': self.username})



class Roles(models.Model):
    role_name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.role_name



    class Meta:
        verbose_name = 'Роли'
        verbose_name_plural = 'Роли'
        ordering = ['role_name']

class Comments(models.Model):
    com_text = models.TextField(db_index=True)
    book = models.ForeignKey("Books", on_delete=models.PROTECT, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.com_text

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.book.pk})


    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['create_time', 'com_text']




class CommentsAns(models.Model):
    ans_com_text = models.TextField(db_index=True)
    user_com_ans = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    comments = models.ForeignKey("Comments", on_delete=models.CASCADE, related_name="comments_ans")

    def __str__(self):
        return self.ans_com_text

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.comments.pk})

    class Meta:
        verbose_name = 'Ответы на комментарии'
        verbose_name_plural = 'Ответв на комментарии'
        ordering = ['create_time', 'ans_com_text']
