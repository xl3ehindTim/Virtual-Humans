from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self) -> None:
        """
        Override app configuration to initialize consumers
        """
        from backend.src.events.subscribers import initialize_listeners
        initialize_listeners()