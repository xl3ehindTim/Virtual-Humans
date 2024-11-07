from channels.generic.websocket import WebsocketConsumer

from rest_framework import serializers

from analytics.models import Event
from analytics.serializers import ImageSerializer
from analytics.utils import decode_base64_frame
from analytics.event_handler import EventHandler

# from fer import FER

import face_recognition

import json
import cv2
import numpy as np


# TODO: Move to database after recognition is validated
known_face_encodings = []

# TODO: Implement Django alike 'MIDDLEWARE' for event handling and scalability

class VirtualHumanConsumer(WebsocketConsumer):
    def connect(self):
        """
        Called when a client connects
        """
        self.accept()
        # self.__init_processor()
        self.event_handler = EventHandler()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'success',
        }))

    # def __init_processor(self) -> None:
    #     self.detector = FER(mtcnn=True)

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
            serializer = ImageSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.validated_data['payload']

            self.event_handler.handle_event(event_type=type, payload=payload)

            frame = decode_base64_frame(payload['data'])

            # self.send(text_data=json.dumps({
            #     'type': 'message',
            # }))

            # Convert BGR image from OpenCV to RGB for face_recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # frame[:, :, ::-1]

            # Find all the faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, model="small")

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.5)

                if True in matches:
                    # Get the index of the first True match
                    first_match_index = matches.index(True)

                    # Retrieve the matched face encoding from the known_face_encodings list
                    matched_face_encoding = known_face_encodings[first_match_index]

                    self.event_handler.handle_event(event_type="face_recognition", payload={"face_encoding": matched_face_encoding.tolist()})
                else:
                    # TODO: Add new user
                    known_face_encodings.append(face_encoding)

            # emotions = self.__process_frame(frame=frame)
            # self.send(text_data=json.dumps({
            #     'type': 'emotions',
            #     'emotions': emotions[0].get("emotions") if len(emotions) > 0 else {}
            # }))

        elif type == "audio":
            pass

    def disconnect(self, close_code):
        """
        Called when the socket closes
        """
        pass
