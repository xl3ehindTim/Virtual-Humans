from django.db import models
import uuid

class Event(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True) 
    data = models.JSONField() 
    metadata = models.JSONField(null=True, blank=True) # TODO: Future proofing for versioning

    def __str__(self):
        return f"{self.event_type} - {self.event_id}"
