import base64
import cv2
import numpy as np
from fer import FER

# i.e. ChatGPT
# facial recognition


class ChatGPTService:
    def __init__(self):
        pass


class FacialRecognitionService:
    def __init__(self):
        pass
    

class EmotionService:
    def __init__(self):
        """Initialize the FER detector."""
        self.detector = FER(mtcnn=True)

    def base64_to_frame(self, base64_string: str):
        """
        Convert base64-encoded string back to a frame.
        """
        frame_bytes = base64.b64decode(base64_string)

        if not isinstance(frame_bytes, np.ndarray):
            frame_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
        return frame
    
    def detect_emotions(self, base64_string: str):
        """
        Detect emotions from a base64-encoded image string.
        """
        frame = self.base64_to_frame(base64_string)
        emotions = self.detector.detect_emotions(frame)
        return emotions[0].get("emotions") if len(emotions) > 0 else {}
    

emotion_service = EmotionService()