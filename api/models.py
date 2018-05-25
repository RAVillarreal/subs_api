from django.db import models

# Create your models here.
class Subtitle(models.Model):
    name = models.CharField(max_length=100)
    link = models.TextField()
    downloads = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
