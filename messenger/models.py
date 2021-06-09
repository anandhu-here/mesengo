from django.db import models
from accounts.models import User
# Create your models here.

class Conversation(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_1")
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_1.first_name) + "-" + str(self.user_2.first_name)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.sender.first_name) + "-" + str(self.reciever.first_name)

class FileMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_file = models.FileField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)