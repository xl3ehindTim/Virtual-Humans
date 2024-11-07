from django.db import models


class Event(models.Model):
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()  

    def __str__(self):
        return self.type