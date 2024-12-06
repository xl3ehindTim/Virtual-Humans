from django.conf import settings

import redis
import threading
import json


class EventBus:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        self.subscribers = {}
        self.lock = threading.Lock()

    def publish(self, event_name, data):
        """Publish an event with data."""
        try:
            self.redis.publish(event_name, json.dumps(data))

            # Create save event to log everything
            self.redis.publish("event.save", json.dumps({
                **data,
                "type": event_name,
            }))
        except Exception as e:
            print(f"Failed to publish event {event_name}: {e}")

    def subscribe(self, event_name, handler):
        """Subscribe a handler function to an event."""
        with self.lock:
            if event_name not in self.subscribers:
                self.subscribers[event_name] = []
            self.subscribers[event_name].append(handler)

    def _event_listener(self, event_name):
        """Internal listener for Redis pub/sub."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(event_name)

        try:
            for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        with self.lock:
                            for handler in self.subscribers.get(event_name, []):
                                try:
                                    handler(data)
                                except Exception as handler_error:
                                    print(f"Error in handler for {event_name}: {handler_error}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode message: {e}")
        except Exception as e:
            print(f"Listener error for {event_name}: {e}")
        finally:
            pubsub.close()

    def start_listener(self, event_name):
        """Start a listener thread for an event."""
        thread = threading.Thread(target=self._event_listener, args=(event_name,))
        thread.daemon = True
        thread.start()

# Singleton instance of the EventBus
event_bus = EventBus()
