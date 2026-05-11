from django.db import models
from order.models import Order

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at= models.DateTimeField(auto_now_add=True)
    class Status(models.TextChoices):
        PENDING = 'pending','Pending'
        PROCESSING = 'processing','Processing'
        PAID = 'paid','Paid'

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)