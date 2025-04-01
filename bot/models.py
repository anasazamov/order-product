from django.db import models

# Create your models here.


class BotAdmin(models.Model):
    fullname = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=True)
    chat_id = models.BigIntegerField(null=False)
    is_active = models.BooleanField(default=False)


