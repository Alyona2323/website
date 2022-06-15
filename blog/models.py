from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Назва категорії"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категорія")
        verbose_name_plural = _("Категорії")


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name=_("Назва"))
    content = models.TextField(verbose_name=_("Опис"))
    published_date = models.DateTimeField(auto_created=True, verbose_name=_("Дата опублікування"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Категорія"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    img = models.ImageField(upload_to="posts", verbose_name=_("Зображення"))
    likes = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name=_("Вподобання"))

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = _("Публікація")
        verbose_name_plural = _("Публікації")


class Comment(models.Model):
    text = models.TextField(verbose_name=_("Текст"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Створено"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, verbose_name=_("Публікація"))

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = _("Коментар")
        verbose_name_plural = _("Коментарі")

