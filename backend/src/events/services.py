from .utils import base64_to_frame

from fer import FER
import face_recognition

import cv2


# LLMService? More generic as it doesn't have to necessarily be ChatGPT?
class ChatGPTService:
    def __init__(self):
        pass


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