from channels.generic.websocket import WebsocketConsumer

import json
import cv2
import base64
import numpy as np

from events.event_bus import event_bus


def on_event(data):
    print(data)

event_bus.subscribe("event.image", on_event)
event_bus.start_listener("event.image")


def on_event_hoi(data):
    print("hoi")

event_bus.subscribe("event.hoi", on_event_hoi)
event_bus.start_listener("event.hoi")

class VirtualHumanConsumer(WebsocketConsumer):
    def connect(self):
        """
        Called when a client connects
        """
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

        data = json.loads(text_data)
        type = data.get("type")

        if type == "image":
            # event_bus.publish("event.image", {**data, "timestamp": datetime.utcnow().isoformat() + "Z" })
            event_bus.publish("event.image", {**data})

        if type == "hoi":
            event_bus.publish("event.hoi", {})
        # elif type == "audio":
        #     pass

