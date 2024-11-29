from django.utils import timezone
from .models import Event

from events.event_bus import event_bus


def save_event_to_db(data):
    """Event handler that saves the event to the database."""
    event_type = data.get("type")
    if not event_type:
        print("Invalid event: Missing 'type'")
        return
    
    try:
        # Create a new Event in the database
        Event.objects.create(
            event_type=event_type,
            data=data,
            timestamp=timezone.now()
        )
        print(f"Event '{event_type}' saved to database.")
    except Exception as e:
        print(f"Failed to save event {event_type} to database: {e}")


event_bus.subscribe("event.save", save_event_to_db)

event_bus.start_listener("event.save")