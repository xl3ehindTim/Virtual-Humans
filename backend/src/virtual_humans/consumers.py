from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from events.event_bus import event_bus
import json


class VirtualHumanConsumer(WebsocketConsumer):
    def connect(self):
        """ Handles WebSocket connection """

        event_bus.subscribe("event.virtual_human", self.virtual_human_event_handler)

        self.accept()

        # Send connection confirmation
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'success',
        }))

    def disconnect(self, close_code):
        """ Unsubscribe on disconnect to avoid memory leaks """
        if "event.virtual_human" in event_bus.subscribers:
            event_bus.subscribers["event.virtual_human"].remove(self.virtual_human_event_handler)

    def receive(self, text_data=None, bytes_data=None) -> None:
        """
        Called when data is received from a client
        """
        if not text_data:
            return

        # Parse text_data to JSON
        data = json.loads(text_data)
        type = data.get("type")
        
        # TODO: Validation

        # Build event payload
        message = {
            **data,
            "timestamp": timezone.now().isoformat(),
        }
        
        if type == "image":
            event_bus.publish("event.image", message)

        if type == "text":
            event_bus.publish("event.text", message)
            
    def virtual_human_event_handler(self, data):
        """ Send actionable behaviour and responses to Virtual Human """
        self.send(text_data=json.dumps({
            "type": data.get("type"),
            "payload": data.get("payload"),
            "timestamp": data.get("timestamp"),
            "metadata": data.get("metadata") or {}
        }))