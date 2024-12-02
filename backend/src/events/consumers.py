from events.models import Event
from events.event_bus import event_bus
from events.services import emotion_service

from django.utils import timezone


def process_emotions(params):
    """
    Process an image event to analyze emotions.

    This function is triggered by the "event.image" event published to the event bus. 
    It extracts image data from the event payload, performs emotion analysis using the 
    EmotionService, and publishes a new "emotion.analysis" event with the results.

    Parameters:
        params (dict): The event payload passed to the function.
            - payload (dict): Contains the data for the event.
                - data (str): Base64-encoded image data to be processed.

    Returns:
        None

    Published Event:
        Event Name: "emotion.analysis"
        Payload:
            - type (str): Type of the event ("emotion.analysis").
            - payload (dict): Contains the analysis results.
                - data (dict): A dictionary of detected emotions and their intensities.
            - timestamp (str): ISO 8601 timestamp of when the event was processed.
    """     
    payload = params.get("payload")
    data = payload.get("data")

    emotions = emotion_service.detect_emotions(data)
    
    # TODO: Formatting?
    payload = {
        'type': 'emotion.analysis', 
        'payload': {
            'data': emotions,
        },
        'timestamp': timezone.now().isoformat()
    }

    event_bus.publish("emotion.analysis", payload)


def save_event(params):
    """
    Save an event to the database.

    This function is triggered by the "event.save" event published to the event bus. 
    It extracts event details from the provided parameters and saves them to the database.

    Parameters:
        params (dict): The event payload passed to the function.
            - type (str): The type of the event.
            - timestamp (str): ISO 8601 timestamp of the event.
            - payload (dict): Contains the actual data of the event.

    Returns:
        None
    """
    Event.objects.create(
        event_type=params.get("type"),
        timestamp=params.get("timestamp"),
        data=params.get("payload"),
    )


def initialize_listeners():
    # Subscribe handlers
    event_bus.subscribe("event.image", process_emotions)
    event_bus.subscribe("event.save", save_event)

    # Start listeners
    event_bus.start_listener("event.image")
    event_bus.start_listener("event.save")

    event_bus.start_listener("event.virtual_human")
