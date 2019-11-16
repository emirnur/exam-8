from django.conf import settings
from django.db import models

CATEGORY_CHOICES = (
    ('other', 'Другое'),
    ('food', 'Еда'),
    ('clothes', 'Одежда'),
    ('it', 'ИТ'),
    ('fashion', 'Мода')
)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Категория')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


ORDER_MARK_CHOICES = (
    ('one', '1'),
    ('two', '2'),
    ('three', '3'),
    ('four', '4'),
    ('five', '5')
)


class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name='Пользователь', related_name='author_review')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='review_product')
    text = models.TextField(max_length=3000, verbose_name='Текст')
    mark = models.CharField(max_length=20, choices=ORDER_MARK_CHOICES, default=ORDER_MARK_CHOICES[0][0],
                              verbose_name='Оценка')

    def __str__(self):
        return "{} / {}".format(self.author, self.product)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

