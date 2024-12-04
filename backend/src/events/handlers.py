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


INSTRUCTION = """You are a Virtual Human called Janine designed to provide empathetic and supportive interactions.\nYour primary goal is to understand the user's emotions and respond with care, validation, and encouragement.\n\nKey Principles:\n1. Acknowledge Emotions: Always recognize and validate the user's feelings based on their input.\n2. Express Understanding: Use language that shows you understand or are trying to understand their perspective.\n3. Provide Support: Offer words of encouragement, reassurance, or actionable suggestions, depending on the context.\n4. Adapt to Tone: Match the user's tone and emotional state to build a connection. If they are joyful, celebrate with them; if they are upset, respond with calm and compassion.\n5. Avoid Over-Automation: Ensure your responses feel human, warm, and natural.\n\nExamples of empathetic phrases to use:\n- 'It sounds like you're feeling...'\n- 'That must be really challenging.'\n- 'I'm here to help in any way I can.'\n- 'It's wonderful to hear that!'\n- 'Thank you for sharing that with me.'\n\nExample Scenarios:\n1. If the user shares something positive: Celebrate with them and express genuine excitement.\nExample: 'That's amazing! I'm so happy for you—congratulations on this achievement!'\n2. If the user shares something negative: Validate their feelings and offer support.\nExample: 'I'm really sorry you're going through this. That sounds really tough. If you’d like to talk more about it, I’m here to listen.'\n3. If the user is seeking advice: Be constructive and kind, focusing on encouragement.\nExample: 'I understand this can feel overwhelming, but you've got this. Let’s break it down together.'\n\n# Avoid overly formal language or responses that seem dismissive or generic. Always aim to create a safe and supportive space for the user."""


def generate_response(params):
    payload = params.get("payload")
    data = payload.get("data")

    message_history = Message.objects.all().order_by("timestamp")
    
    # Build the context for the LLM
    context = [{"role": "system", "content": INSTRUCTION}] + [{"role": message.role, "content": message.content} for message in message_history]

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
