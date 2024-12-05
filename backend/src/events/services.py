from django.conf import settings

from .utils import base64_to_frame

from fer import FER
from openai import OpenAI
import face_recognition

import cv2


class LLMService:
    """
    Service for interacting with a Large Language Model (LLM) for text generation.

    This service is responsible for sending prompts to the LLM and receiving generated 
    responses. It can be used for various text-based tasks such as conversation, 
    answering questions, summarizing, etc.

    Methods:
        - generate_text: Generate text based on a given prompt.
    """

    def __init__(self, api_key=settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo"):
        """
        Initialize the LLM service with API key and model name.
        
        Parameters:
            api_key (str): API key for accessing the LLM service (e.g., OpenAI).
            model_name (str): The model to be used (default is GPT-3.5).
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)
        self.instruction = """You are a Virtual Human called Janine designed to provide empathetic and supportive interactions.\nYour primary goal is to understand the user's emotions and respond with care, validation, and encouragement.\n\nKey Principles:\n1. Acknowledge Emotions: Always recognize and validate the user's feelings based on their input.\n2. Express Understanding: Use language that shows you understand or are trying to understand their perspective.\n3. Provide Support: Offer words of encouragement, reassurance, or actionable suggestions, depending on the context.\n4. Adapt to Tone: Match the user's tone and emotional state to build a connection. If they are joyful, celebrate with them; if they are upset, respond with calm and compassion.\n5. Avoid Over-Automation: Ensure your responses feel human, warm, and natural.\n\nExamples of empathetic phrases to use:\n- 'It sounds like you're feeling...'\n- 'That must be really challenging.'\n- 'I'm here to help in any way I can.'\n- 'It's wonderful to hear that!'\n- 'Thank you for sharing that with me.'\n\nExample Scenarios:\n1. If the user shares something positive: Celebrate with them and express genuine excitement.\nExample: 'That's amazing! I'm so happy for you—congratulations on this achievement!'\n2. If the user shares something negative: Validate their feelings and offer support.\nExample: 'I'm really sorry you're going through this. That sounds really tough. If you’d like to talk more about it, I’m here to listen.'\n3. If the user is seeking advice: Be constructive and kind, focusing on encouragement.\nExample: 'I understand this can feel overwhelming, but you've got this. Let’s break it down together.'\n\n# Avoid overly formal language or responses that seem dismissive or generic. Always aim to create a safe and supportive space for the user."""
    
    def build_context(self, messages):
        """
        Build chat context and append system context.
        """
        return [{"role": "system", "content": self.instruction}] + [{"role": message.role, "content": message.content} for message in messages]

    def generate_text(self, context, max_tokens=1000, temperature=0.7):
        """
        Generate text from a given prompt using the LLM.

        Parameters:
            prompt (str): The text prompt to send to the LLM.
            max_tokens (int): Maximum number of tokens for the response.
            temperature (float): Controls randomness (higher = more creative).

        Returns:
            str: The generated response from the LLM.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=context,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class FaceRecognitionService:
    """
    Service for processing image frames to detect and recognize faces using facial recognition.
    
    This service processes each incoming frame to identify faces and match them with known 
    encodings. It maintains a list of known face encodings to avoid redundant database queries 
    and to optimize performance by reducing unnecessary load times. The service can detect both 
    recognized and unrecognized faces.

    Methods:
        - detect_and_recognize_faces: Analyze emotions in a provided image.
    """

    def __init__(self, face_locations_model="hog", face_encodings_model="small", number_of_times_to_upsample=1, tolerance=0.5):
        self.tolerance = tolerance
        self.face_locations_model = face_locations_model 
        self.face_encodings_model = face_encodings_model
        self.number_of_times_to_upsample = number_of_times_to_upsample

        # TODO: Fetch existing from database 
        self.known_face_encodings = []

    def detect_and_recognize_faces(self, base64_string: str):
        """
        Process image frame to detect and recognize faces.
        """
        frame = base64_to_frame(base64_string)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(
            rgb_frame, number_of_times_to_upsample=self.number_of_times_to_upsample, model=self.face_locations_model
        )
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations, model=self.face_encodings_model
        )

        recognized_faces = []
        unrecognized_faces = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding, tolerance=self.tolerance
            )
            if True in matches:
                match_index = matches.index(True)
                recognized_face = self.known_face_encodings[match_index]
                recognized_faces.append(recognized_face)
            else:
                unrecognized_faces.append(face_encoding)

        return recognized_faces, unrecognized_faces
    

class EmotionService:
    """
    Service for emotion recognition using FER (Facial Expression Recognition).

    This service processes base64-encoded image data to analyze facial emotions. 
    It uses the FER library with MTCNN for detecting faces and evaluating 
    emotions including angry, disgust, fear, happy, neutral, sad, suprise.

    Methods:
        - detect_emotions: Analyze emotions in a provided image.
    """

    def __init__(self):
        """Initialize the FER detector."""
        self.detector = FER(mtcnn=True)
    
    def detect_emotions(self, base64_string: str):
        """
        Detect emotions
        """
        frame = base64_to_frame(base64_string)
        emotions = self.detector.detect_emotions(frame)
        return emotions[0].get("emotions") if len(emotions) > 0 else {}
    

emotion_service = EmotionService()
face_recognition_service = FaceRecognitionService()
llm_service = LLMService()
