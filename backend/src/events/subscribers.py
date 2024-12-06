from events.handlers import *
from events.event_bus import event_bus


def initialize_listeners():
    """
    Subscribes event handlers to the event bus.
    """

    event_bus.subscribe("video.frame", process_emotions)
    event_bus.subscribe("video.frame", face_recognition)
    
    event_bus.subscribe("audio.raw", process_raw_audio)
    event_bus.subscribe("audio.transcription", generate_response)
    
    event_bus.subscribe("event.save", save_event)

    # Listeners
    event_bus.start_listener("video.frame") 

    event_bus.start_listener("audio.raw")
    event_bus.start_listener("audio.transcription") 

    event_bus.start_listener("assistant.response")

    event_bus.start_listener("event.save")
