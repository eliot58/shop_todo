from django.db import models

class Offer(models.Model):
    file = models.FileField(upload_to="offers")
    params = models.JSONField()
