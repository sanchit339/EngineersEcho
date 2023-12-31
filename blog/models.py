from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200 , default='')
    content = models.TextField(default='')
    stripped_content = models.TextField(default='.')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE , default=1)

    def __str__(self):
        return self.title
