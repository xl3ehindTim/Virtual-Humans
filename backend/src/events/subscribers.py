from events.handlers import *
from events.event_bus import event_bus


def initialize_listeners():
    """
    Subscribes event handlers to the event bus.
    """

    # Subscribe handlers
    event_bus.subscribe("event.image", process_emotions)
    event_bus.subscribe("event.image", face_recognition)
    
    event_bus.subscribe("event.text", generate_response)
    event_bus.subscribe("event.save", save_event)

    # Start listeners for each event type 
    event_bus.start_listener("event.image") # rename: video.frame?
    event_bus.start_listener("event.text") # rename: audio.transcription?
    event_bus.start_listener("event.save")
    event_bus.start_listener("event.virtual_human")