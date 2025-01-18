from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField(null=True,blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

