from django.db import models
import uuid

class Event(models.Model):
    """
    Stores event messages
    """
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True) 
    data = models.JSONField() 
    metadata = models.JSONField(null=True, blank=True) # TODO: Future proofing for versioning and user_id?

    def __str__(self):
        return f"{self.event_type} - {self.event_id}"


class Message(models.Model):
    """
    Stores conversation messages
    """
    ROLE_CHOICES = (
        ('system', 'System'),
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 