from email.mime import image
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст объявления")
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    created_ad = models.DateTimeField(auto_now_add="True", verbose_name="Дата создания")
    updated_ad = models.DateTimeField(auto_now="True", verbose_name="Дата обновления")
    photo = models.ImageField(blank=True, null=True, verbose_name="Фото",default='default.jpg')
    price = models.PositiveIntegerField(verbose_name="Цена", default=0)
    is_published = models.BooleanField(default=True, verbose_name="Активное?")
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name="Категории",
        default=1
    )

    def get_absolute_url(self):
        return reverse("views_post", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявления"
        verbose_name_plural = "Объявление"
        ordering = ["-updated_ad"]

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to="photos", verbose_name='Фото', blank=True)

    # def __str__(self):
    #     return self.post.title
    class Meta:
        verbose_name = "Фото"

class Category(models.Model):
    icon = models.ImageField(upload_to="icons/",blank=True, null=True, verbose_name="Иконка")
    title = models.CharField(
        max_length=150, db_index=True, verbose_name="Название категории")
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"
        ordering = ["id"]


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete = models.CASCADE)
    name = models.CharField('Ваше имя', max_length=80)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    body = models.TextField('Комментарий')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ('-created',)

    def __str__(self):
        return 'Комментарий {} от {}'.format(self.name, self.post)


class Help(models.Model):
    name = models.CharField('Ваше имя', max_length=80)
    body = models.TextField('Текст обращения')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Телефон должнен быть похож на: '+999999999'. ")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Телефон") 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Обращение в техподдежку"
        verbose_name_plural = "Техподдержка"
        ordering = ('-created',)

    def __str__(self):
        return '{} Обращение от {}: {}'.format(self.created, self.name, self.body)
