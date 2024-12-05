from events.models import Event, Message
from events.event_bus import event_bus
from events.services import emotion_service, face_recognition_service, llm_service

from django.utils import timezone


def face_recognition(params):
    payload = params.get("payload")
    data = payload.get("data")

    recognized_faces, unrecognized_faces = face_recognition_service.detect_and_recognize_faces(data)

    # Serialize each numpy array in the list to a Python list to prevent 'Object of type ndarray is not JSON serializable'
    serialized_recognized_faces = [face.tolist() for face in recognized_faces] 
    serialized_unrecognized_faces = [face.tolist() for face in unrecognized_faces]

    message = {
        "type": "face_recognition.detect",
        "payload": {
            "recognized_faces": serialized_recognized_faces,
            "unrecognized_faces": serialized_unrecognized_faces,
        },
        "timestamp": timezone.now().isoformat(),
        "metadata": None,
    }

    event_bus.publish(message["type"], message)


def generate_response(params):
    payload = params.get("payload")
    data = payload.get("data")

    messages = Message.objects.all().order_by("timestamp")
    
    # Build the context for the LLM
    context = llm_service.build_context(messages=messages)

    # Add the new user message to the context
    context.append({"role": "user", "content": data})

    # Generate language using LLMService
    response = llm_service.generate_text(context=context)

    # Save messages to the database
    Message.objects.bulk_create([
        Message(role="user", content=data),
        Message(role="assistant", content=response)
    ])

    # Build event message
    message = {
        "type": "response.text",
        "payload": {
            "response": response,
        },
        "timestamp": timezone.now().isoformat(),
        "metadata": None,
    }

    event_bus.publish(message["type"], message)
    

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

    message = {
        "type": "emotion.analysis",
        "payload": {
            "emotions": emotions,
        },
        "timestamp": timezone.now().isoformat(),
        "metadata": None,
    }

    event_bus.publish("emotion.analysis", message)


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
            - metadata (dict): Contains metadata of the event.
    """
    Event.objects.create(
        event_type=params.get("type"),
        timestamp=params.get("timestamp"),
        data=params.get("payload"),
        metadata=params.get("metadata"),
    )
