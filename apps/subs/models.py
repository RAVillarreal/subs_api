from django.db import models

# Create your models here.
class Subtitle(models.Model):
    name = models.CharField(max_length=100)
    downloads = models.IntegerField(default=0)
    uploaded = models.DateField(auto_now_add=True)
    link = models.TextField()

    def __str__(self):
        return self.name