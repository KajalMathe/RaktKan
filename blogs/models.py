# blogs/models.py

from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(unique=True)
    published_date = models.DateTimeField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return self.title
