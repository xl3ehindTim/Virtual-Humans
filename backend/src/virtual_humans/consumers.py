from channels.generic.websocket import WebsocketConsumer
from fer import FER

import json
import cv2
import base64
import numpy as np


class VirtualHumanConsumer(WebsocketConsumer):
    def connect(self):
        """
        Called when a client connects
        """
        self.accept()
        self.__init_processor()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'success',
        }))

    def __init_processor(self) -> None:
        self.detector = FER(mtcnn=True)

    def __base64_to_frame(self, base64_string: str):
        """
        Convert base64-encoded string back to a frame.
        """
        frame_bytes = base64.b64decode(base64_string)

        if not isinstance(frame_bytes, np.ndarray):
            frame_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
        return frame

    def __process_frame(self, frame):
        return self.detector.detect_emotions(frame)

    def receive(self, text_data=None, bytes_data=None) -> None:
        """
        Called when data is received from a client
        """
        if not text_data:
            return

        data = json.loads(text_data)
        
        type = data.get("type")

        if type == "image":
            frame = self.__base64_to_frame(data.get("data"))
            emotions = self.__process_frame(frame=frame)

            self.send(text_data=json.dumps({
                'type': 'emotions',
                'emotions': emotions[0].get("emotions") if len(emotions) > 0 else {}
            }))

        elif type == "audio":
            pass

    def disconnect(self, close_code):
        """
        Called when the socket closes
        """
        pass
