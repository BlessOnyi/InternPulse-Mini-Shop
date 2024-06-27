from django.db import models
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    name = models.CharField(max_length=150)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.product.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.product.name} ({self.quantity})"