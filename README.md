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

Event name | Description | Input | Triggered by
--- | --- | --- | --- |
`audio.raw` | Raw audio bytes captured from a source | `{ "payload": { "bytes": "<base64-encoded-audio>" }}` | |
`audio.transcription` | Transcribed text from audio | `{ "payload": { "transcription": "<transcription>" }}` | `audio.raw` |
`video.frame` | Video feed frames | `{ "payload": { "data": "<base64-encoded-image>" }}` |  |
`face.detected` | Detects faces from a video frame | `{ "payload": { "data": "<base64-encoded-image>" }}` | `video.frame` |
`face.emotion` | Detects emotions from faces in a video frame | `{ "payload": { "data": "<base64-encoded-image>" }}` | `face.detected` |
`assistant.response`  | AI agent response message | `{ "payload": { "transcription": "<transcription>" }}` | `audio.transcription` | 
`event.save`  | Event to trigger event storage into the database | `{ "type": "<domain.action>", "payload": { <event data> }, "timestamp": "<iso-8601-timestamp>", "metadata": { <metadata> } }` |  |

<!-- `face.unrecognized` | Faces detected but not recognized | `{ "payload": { "faces": [ { "encoding": "<face-encoding>" "} ] }}` |
`face.emotion` | Analyzed emotions of detected faces | `{ "payload": { "faces": [ { "id": "<face-id>", "emotions": { "happy": 0.8, "sad": 0.1, "neutral": 0.1 } } ] } }` | -->

<!--
`face.recognized` | Recognized faces from a video frame | `{ "payload": { "faces": [ { "id": "<user-id>", "encoding": "<face-encoding>" "} ] }}` |
`face.unrecognized` | Faces detected but not recognized | `{ "payload": { "faces": [ { "encoding": "<face-encoding>" "} ] }}` |
`face.emotion` | Analyzed emotions of detected faces | `{ "payload": { "faces": [ { "id": "<face-id>", "emotions": { "happy": 0.8, "sad": 0.1, "neutral": 0.1 } } ] } }` |
-->
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