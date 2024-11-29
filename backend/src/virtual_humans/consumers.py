from channels.generic.websocket import WebsocketConsumer

import json
import cv2
import base64
import numpy as np

from django.utils import timezone

from events.event_bus import event_bus


class VirtualHumanConsumer(WebsocketConsumer):
    def connect(self):
        """ Handles WebSocket connection """

        event_bus.subscribe("event.virtual_human", self.virtual_human_event_handler)
        event_bus.start_listener("event.virtual_human")

        self.accept()

        # Send connection confirmation
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'success',
        }))

    def __base64_to_frame(self, base64_string: str):
        """
        Convert base64-encoded string back to a frame.
        """
        frame_bytes = base64.b64decode(base64_string)

        if not isinstance(frame_bytes, np.ndarray):
            frame_bytes = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
        return frame

    def receive(self, text_data=None, bytes_data=None) -> None:
        """
        Called when data is received from a client
        """
        if not text_data:
            return

        # Parse text_data to JSON
        data = json.loads(text_data)
        type = data.get("type")
        # data.pop("type", None)

        # TODO: Validation

        # Build event payload
        payload = {
            **data,
            "timestamp": timezone.now().isoformat()
        }

        if type == "image":
            event_bus.publish("event.image", payload)

        # if type == "text":
        #     event_bus.publish("event.text", payload)
            
        # if type == "t":
        #     event_bus.publish("event.virtual_human", { 
        #         "type": "behaviour",
        #         "data": {
        #             "a": 1
        #         }
        #     })

    def virtual_human_event_handler(self, data):
        """ Send actionable behaviour and responses to Virtual Human """
        self.send(text_data=json.dumps({
            "type": data.get("type"),
            "payload": data
        }))