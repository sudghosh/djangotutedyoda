from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)
    

class Purchase(models.Model):
    name = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(blank=True)
    salesman = models.ForeignKey(User,on_delete=models.CASCADE)

    # changes required everytime updated
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args,**kwargs)

    def __str__(self):
        return f'Sold {self.name} - {self.quantity} items for {self.total_price}'