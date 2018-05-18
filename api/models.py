from django.db import models

# Create your models here.
class SubtitleModel(models.Model):
    name = models.CharField(max_length=100)
    link = models.TextField()
    downloads = models.IntegerField()
    date = models.DateField()

    def save(self):
        pass
