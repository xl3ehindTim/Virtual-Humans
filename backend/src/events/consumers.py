from events.models import Event
from events.event_bus import event_bus
from events.services import emotion_service

from django.utils import timezone


def process_emotions(params):
    payload = params.get("payload")
    raw_data = payload.get("data")

    emotions = emotion_service.detect_emotions(raw_data)

    payload = {
        'type': 'emotion.analysis', 
        'payload': {
            'data': emotions,
            'timestamp': timezone.now().isoformat()
        }
    }

    event_bus.publish("emotion.analysis", payload)


event_bus.subscribe("event.image", process_emotions)
event_bus.start_listener("event.image")



def save_event(params):
    """ Save event to database """
    Event.objects.create(
        event_type=params.get("type"),
        timestamp=params.get("timestamp"),
        data=params.get("payload"),
    )

event_bus.subscribe("event.save", save_event)
event_bus.start_listener("event.save")