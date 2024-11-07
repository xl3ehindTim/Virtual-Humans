from analytics.models import Event


class EventHandler:
    def __init__(self):
        pass

    def handle_event(self, event_type, payload):
        event = Event.objects.create(type=event_type, payload=payload)
        event.save()