from django.db import models

# Create your models here.
class payment_details_cus(models.Model):
    customer_name=models.CharField(max_length=100)
    customer_id=models.CharField(max_length=200)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    product_id = models.CharField(max_length=200)
    checkout_id=models.CharField(max_length=200)
    amount_paid=models.BooleanField(default=False)
    quantity=models.IntegerField()

