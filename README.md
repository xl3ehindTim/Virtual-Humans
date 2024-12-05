# Virtual Humans
This repository contains the backend system for a Virtual Human experience, built with Python. The system leverages an event-driven architecture to enable parallel processing and dynamic interactions. 

## Repository structure
```bash
├── src/
│   ├── users/               # User management
│   ├── virtual_humans/      # Core project logic and configurations
│   │   ├── consumers.py     # WebSocket connection consumer
│   │   └── ...              # Other project logic and configuration files
│   ├── events/              # Event-driven components
│   │   ├── handlers.py      # Business logic for processing specific events
│   │   ├── services.py      # Core business operations
│   │   ├── subscribers.py   # Event listeners
│   │   ├── event_bus.py     # Event dispatch and routing
│   │   ├── models.py        # Database models
│   │   └── ...              # Other utilities for event handling
│   └── manage.py            # Django management script
├── Dockerfile.dev           # Development Dockerfile
├── docker-compose.yml       # Docker Compose file for setting up services
└── .env                     # Environment variables
```
### How it works
The events app contains the event-driven architecture components, including handlers, services, subscribers, and the event bus. The system communicates by routing events through the event bus, which are processed by handlers implementing services for specific functionalities (i.e. face recognition, response generation). Docker is used to run the backend and associated services like Redis and PostgreSQL.

## Event schema

Event name | Description | Input |
--- | --- | --- |
`audio.raw` | Raw audio bytes captured from a source | `{ "payload": { "bytes": "<base64-encoded-audio>" }}` |
`audio.transcription` | Transcribed text from audio | `{ "payload": { "transcription": "<transcription>" }}` |
`video.frame` | Video feed frames | `{ "payload": { "data": "<base64-encoded-image>" }}` |
`assistant.response`  | AI agent response message | `{ "payload": { "transcription": "<transcription>" }}` |
`event.save`  | Event to trigger event storage into the database | `{ "type": "<domain.action>", "payload": { <event data> }, "timestamp": "<iso-8601-timestamp>", "metadata": { <metadata> } }` |

<!--- Table row
Event name | Description | Input |  
--->

## Getting started
### Prerequisites 
- Docker

### Run

```bash
docker-compose -f docker-compose.yml up --build
```

### Usage
Interact with the backend through a WebSocket connection, either the Virtual Human, a custom client script, or online [WebSocket tester](https://piehost.com/websocket-tester).