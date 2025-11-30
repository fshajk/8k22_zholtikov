from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    product_id = models.AutoField("ID", primary_key=True)
    name = models.CharField("Name", max_length=256)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Quantity", default=0)
    description = models.TextField("Description")
    img_path = models.TextField("ImgPath", default="static/img/noimg.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Товар {self.name}'


class Order(models.Model):
    order_id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField("Order Date")
    address = models.TextField("Address")
    status = models.TextField("Status", default="in progress")
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Заказ № {self.order_id}'


class OrderItem(models.Model):
    order_item_id = models.AutoField("ID", primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Quantity", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Товар № {self.order_item_id}'


class CartItem(models.Model):
   cart_item_id = models.AutoField("ID", primary_key=True)
   user = models.ForeignKey(User, on_delete=models.PROTECT)
   product = models.ForeignKey(Product, on_delete=models.PROTECT)
   cost = models.DecimalField("Cost", max_digits=10, decimal_places=2, default=0)
   quantity = models.PositiveIntegerField("Quantity", default=1)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f'Товар в корзине № {self.cart_item_id}'
