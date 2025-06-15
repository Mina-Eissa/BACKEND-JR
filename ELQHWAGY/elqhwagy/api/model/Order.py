import uuid
from django.db import models
from .User import User
from .Product import Product
from .Client import Client


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        COMPLETED = 'COMPLETED','COMPLETED'
        PENDING = 'PENDING','PENDING'
        CANCELED = 'CANCELED','CANCELED'
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4 ,editable=False)
    employee = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Employee')
    client = models.ForeignKey(Client,on_delete=models.CASCADE,verbose_name='Client')
    order_items = models.ManyToManyField('Product',through='OrderItem')
    status = models.TextField(choices=OrderStatus.choices,default=OrderStatus.PENDING)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def totalCost(self):
        return sum(item.total for item in self.orderitem_set.all())
    
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,verbose_name=f'qantity for {product.name}')
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.product.price
