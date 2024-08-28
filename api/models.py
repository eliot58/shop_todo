from django.db import models

class Order(models.Model):
    payment_id = models.UUIDField(primary_key=True)
    paid = models.BooleanField(default=False)

class Offer(models.Model):
    file = models.FileField(upload_to="offers")
    params = models.JSONField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)