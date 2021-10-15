from django.db import models

# Create your models here.
class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    affiliations = models.CharField(max_length=256)
    pubcount = models.IntegerField()
    citecount = models.IntegerField()
    hindex = models.IntegerField()
    interests = models.CharField(max_length=512)