from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User ,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self) :
        return  self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    info = models.TextField(null= True)
    price = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    complete = models.BooleanField(default=False,null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def calculate_cart_total(self):
        total =0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total += item.calculate_total
        return total
    
    @property
    def calculate_cart_items(self):
        total=0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total += item.quantity
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)

    @property
    def calculate_total(self):
        total = self.quantity * self.product.price
        return total