from events.models import Event
from events.event_bus import event_bus

def on_event(data):
    print('test2')

event_bus.subscribe("event.image", on_event)
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