from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse


# Create your models here.
class User(AbstractUser):
    user_adress = models.CharField(max_length=255,verbose_name="Адресс")
    user_birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Product(models.Model):
    product_name = models.CharField(max_length=255,verbose_name="Название продукта")
    product_description = models.TextField(verbose_name="Описание", blank=True)
    product_price = models.DecimalField(decimal_places=0, max_digits=10,  verbose_name="Цена", default=0)
    product_image = models.ImageField(upload_to="Img/",verbose_name="Изображение продукта")
    product_slug = models.SlugField(max_length=255, unique=True,db_index=True,verbose_name="URL")
    product_physico_chemical_characteristics = models.TextField(verbose_name="Физико-химические свойства", blank=True)
    cat = models.ForeignKey('Category',on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'product_slug': self.product_slug})

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Category(models.Model):
    cat = models.CharField(verbose_name="Категория", max_length=255,unique=True)
    cat_slug = models.SlugField(max_length=255, verbose_name="Category URL")

    def get_absolute_url(self):
        return reverse('category_product', kwargs={'cat_slug': self.cat_slug})

    def __str__(self):
        return self.cat

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['-id']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10,  verbose_name="Итоговая сумма", default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    @staticmethod
    def get_cart_length(user):
        return Cart.objects.filter(user=user).count()

    class Meta:
        unique_together = ['user', 'product']