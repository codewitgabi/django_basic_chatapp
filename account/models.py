from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    message = models.TextField()
    date_sent = models.TimeField(auto_now_add= True)

    def __str__(self):
        return self.message