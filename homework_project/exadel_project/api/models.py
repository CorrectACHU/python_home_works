from django.db import models
from django.db.migrations import operations

# Create your models here.


class TestModel(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()