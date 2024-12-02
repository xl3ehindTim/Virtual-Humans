from events.handlers import process_emotions, generate_response, save_event
from events.event_bus import event_bus


def initialize_listeners():
    """
    Subscribes event handlers to the event bus.
    """

    # Subscribe handlers
    event_bus.subscribe("event.image", process_emotions)
    event_bus.subscribe("event.text", generate_response)
    event_bus.subscribe("event.save", save_event)

    # Start listeners for each event type
    event_bus.start_listener("event.image")
    event_bus.start_listener("event.text")
    event_bus.start_listener("event.save")
    event_bus.start_listener("event.virtual_human")