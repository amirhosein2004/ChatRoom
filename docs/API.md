# API Documentation

Complete API reference for the Django Chat Application.

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication)
- [REST API Endpoints](#rest-api-endpoints)
  - [Room Management](#room-management-apis)
  - [Message APIs](#message-apis)
  - [Template Views](#template-views)
- [WebSocket API](#websocket-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Overview

The application provides both REST API and WebSocket endpoints:

- **REST API**: For CRUD operations, file uploads, and fetching data
- **WebSocket API**: For real-time messaging
- **Base URL**: `http://localhost:8000` (development)
- **API Version**: v1
- **API Prefix**: `/api/room/v1/`

### API Architecture

```
REST API (HTTP)
├── Room Management
├── Message History
└── Image Upload

WebSocket API (WS)
└── Real-time Messaging
```

---

## Authentication

Currently, the API uses **AllowAny** permission for all endpoints, suitable for development. Guest users are automatically created based on username.

### Future Authentication

For production, implement:
- Token-based authentication (JWT)
- Session authentication
- OAuth2

---

## REST API Endpoints

### Room Management APIs

#### 1. List All Public Rooms

**Endpoint**: `GET /api/room/v1/rooms/`

**Description**: Retrieves a list of all public chat rooms.

**Request**:
```http
GET /api/room/v1/rooms/
```

**Response**: `200 OK`
```json
[
    {
        "id": 1,
        "name": "General Discussion",
        "slug": "general-discussion",
        "description": "A place for general conversations",
        "creator": {
            "id": 1,
            "username": "admin"
        },
        "member_count": 5,
        "is_public": true,
        "created_at": "2025-11-08T12:00:00Z",
        "updated_at": "2025-11-08T12:00:00Z"
    },
    {
        "id": 2,
        "name": "Tech Talk",
        "slug": "tech-talk",
        "description": "Discuss technology and programming",
        "creator": {
            "id": 2,
            "username": "user1"
        },
        "member_count": 3,
        "is_public": true,
        "created_at": "2025-11-08T13:00:00Z",
        "updated_at": "2025-11-08T13:00:00Z"
    }
]
```

#### 2. Get Room Details

**Endpoint**: `GET /api/room/v1/rooms/{slug}/`

**Description**: Retrieves details of a specific room.

**Request**:
```http
GET /api/room/v1/rooms/general-discussion/
```

**Response**: `200 OK`
```json
{
    "id": 1,
    "name": "General Discussion",
    "slug": "general-discussion",
    "description": "A place for general conversations",
    "creator": {
        "id": 1,
        "username": "admin"
    },
    "member_count": 5,
    "is_public": true,
    "created_at": "2025-11-08T12:00:00Z",
    "updated_at": "2025-11-08T12:00:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
    "detail": "Not found."
}
```

#### 3. Create New Room

**Endpoint**: `POST /api/room/v1/rooms/create/`

**Description**: Creates a new chat room.

**Request**:
```http
POST /api/room/v1/rooms/create/
Content-Type: application/json

{
    "name": "New Room",
    "description": "A new chat room for discussions",
    "is_public": true,
    "username": "creator_user"
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Room name (max 100 chars, unique) |
| description | string | No | Room description |
| is_public | boolean | No | Public/Private flag (default: true) |
| username | string | No | Creator username (default: 'guest') |

**Response**: `201 Created`
```json
{
    "id": 3,
    "name": "New Room",
    "slug": "new-room",
    "description": "A new chat room for discussions",
    "creator": {
        "id": 3,
        "username": "creator_user"
    },
    "member_count": 0,
    "is_public": true,
    "created_at": "2025-11-08T14:00:00Z",
    "updated_at": "2025-11-08T14:00:00Z"
}
```

**Error Response**: `400 Bad Request`
```json
{
    "name": ["room with this name already exists."]
}
```

#### 4. Join Room

**Endpoint**: `POST /api/room/v1/rooms/{slug}/join/`

**Description**: Join a chat room as a member.

**Request**:
```http
POST /api/room/v1/rooms/general-discussion/join/
Content-Type: application/json

{
    "username": "user123"
}
```

**Response**: `200 OK`
```json
{
    "id": 1,
    "name": "General Discussion",
    "slug": "general-discussion",
    "description": "A place for general conversations",
    "creator": {
        "id": 1,
        "username": "admin"
    },
    "member_count": 6,
    "is_public": true,
    "created_at": "2025-11-08T12:00:00Z",
    "updated_at": "2025-11-08T12:00:00Z"
}
```

**Error Response**: `400 Bad Request`
```json
{
    "error": "نام کاربری الزامی است"
}
```

#### 5. Leave Room

**Endpoint**: `POST /api/room/v1/rooms/{slug}/leave/`

**Description**: Leave a chat room.

**Request**:
```http
POST /api/room/v1/rooms/general-discussion/leave/
Content-Type: application/json

{
    "username": "user123"
}
```

**Response**: `200 OK`
```json
{
    "message": "با موفقیت از اتاق خارج شدید"
}
```

**Error Response**: `404 Not Found`
```json
{
    "error": "کاربر یافت نشد"
}
```

---

### Message APIs

#### 1. Get Message History

**Endpoint**: `GET /api/room/v1/messages/{slug}/?offset={offset}`

**Description**: Retrieves message history for a room with pagination.

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| offset | integer | No | Starting offset for pagination (default: 0) |

**Request**:
```http
GET /api/room/v1/messages/general-discussion/?offset=0
```

**Response**: `200 OK`
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "admin"
        },
        "content": "Hello everyone!",
        "image_url": null,
        "message_type": "text",
        "timestamp": "2025-11-08T12:30:00Z"
    },
    {
        "id": 2,
        "user": {
            "id": 2,
            "username": "user1"
        },
        "content": "Hi admin!",
        "image_url": null,
        "message_type": "text",
        "timestamp": "2025-11-08T12:31:00Z"
    },
    {
        "id": 3,
        "user": {
            "id": 1,
            "username": "admin"
        },
        "content": "",
        "image_url": "http://localhost:8000/media/chat_images/image.jpg",
        "message_type": "image",
        "timestamp": "2025-11-08T12:32:00Z"
    }
]
```

**Notes**:
- Returns 50 messages per request
- Messages are ordered by timestamp (newest first in API, but reversed in frontend)
- For public chat, use slug `public_chat` or omit slug

**Public Chat Request**:
```http
GET /api/room/v1/messages/?offset=0
```

#### 2. Upload Image

**Endpoint**: `POST /api/room/v1/upload-image/`

**Description**: Upload an image message.

**Request**:
```http
POST /api/room/v1/upload-image/
Content-Type: multipart/form-data

{
    "image": [binary file],
    "username": "user123",
    "room_slug": "general-discussion"
}
```

**Form Data**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| image | file | Yes | Image file (JPEG, PNG, etc.) |
| username | string | Yes | Sender username |
| room_slug | string | No | Room slug (omit for public chat) |

**Response**: `201 Created`
```json
{
    "id": 10,
    "user": {
        "id": 3,
        "username": "user123"
    },
    "content": "",
    "image_url": "http://localhost:8000/media/chat_images/image_abc123.jpg",
    "message_type": "image",
    "timestamp": "2025-11-08T14:30:00Z"
}
```

**Error Response**: `400 Bad Request`
```json
{
    "image": ["This field is required."]
}
```

**Notes**:
- Images are uploaded via HTTP (not WebSocket) for better handling of large files
- After upload, a notification is sent to all room members via WebSocket
- Maximum file size should be configured in Django settings

---

### Template Views

#### 1. Room List Page

**Endpoint**: `GET /api/room/v1/rooms/list/`

**Description**: Renders the HTML page showing all rooms.

**Response**: HTML page with room list

#### 2. Chat Room Page

**Endpoint**: `GET /api/room/v1/chat/{slug}/`

**Description**: Renders the chat interface for a specific room.

**Request**:
```http
GET /api/room/v1/chat/general-discussion/
```

**Response**: HTML page with chat interface

#### 3. Public Chat Page

**Endpoint**: `GET /api/room/v1/`

**Description**: Renders the public chat interface.

**Response**: HTML page with public chat

---

## WebSocket API

### Connection

**Endpoint**: `ws://localhost:8000/ws/chat/{room_slug}/`

**Description**: Establishes WebSocket connection for real-time messaging.

**Example**:
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/chat/general-discussion/');
```

For public chat:
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/chat/public_chat/');
```

### Connection Events

#### 1. Connect
```javascript
socket.onopen = function(e) {
    console.log('Connected to chat server');
};
```

#### 2. Disconnect
```javascript
socket.onclose = function(e) {
    console.log('Disconnected from chat server');
};
```

#### 3. Error
```javascript
socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

### Sending Messages

#### Text Message

**Client → Server**:
```json
{
    "message_type": "text",
    "username": "user123",
    "message": "Hello everyone!"
}
```

**JavaScript Example**:
```javascript
socket.send(JSON.stringify({
    'message_type': 'text',
    'username': 'user123',
    'message': 'Hello everyone!'
}));
```

#### Image Message Notification

**Note**: Images are uploaded via HTTP POST. After upload, the server sends a notification through WebSocket.

### Receiving Messages

#### Message Format

**Server → Client**:
```json
{
    "message_id": 123,
    "username": "user123",
    "message_type": "text",
    "message": "Hello everyone!",
    "timestamp": "2025-11-08T12:30:00Z"
}
```

**JavaScript Example**:
```javascript
socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Message received:', data);
    
    if (data.message_type === 'text') {
        displayTextMessage(data);
    } else if (data.message_type === 'image') {
        displayImageMessage(data);
    }
};
```

#### Image Message Format

```json
{
    "message_id": 124,
    "username": "user123",
    "message_type": "image",
    "message": "",
    "image_url": "http://localhost:8000/media/chat_images/image.jpg",
    "timestamp": "2025-11-08T12:31:00Z"
}
```

### WebSocket Flow Diagram

```
Client                          Server                      Database
  |                                |                             |
  |------ WebSocket Connect ------>|                             |
  |<----- Connection Accepted -----|                             |
  |                                |                             |
  |------ Send Text Message ------->|                             |
  |                                |------ Save Message -------->|
  |                                |<----- Message Saved --------|
  |<----- Broadcast Message -------|                             |
  |                                |                             |
  |------ HTTP Upload Image ------->|                             |
  |                                |------ Save Image ---------->|
  |                                |<----- Image Saved ----------|
  |<----- HTTP Response -----------|                             |
  |<----- WebSocket Broadcast -----|                             |
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

### Error Response Format

```json
{
    "error": "Error message here",
    "detail": "Detailed error information"
}
```

### Field Validation Errors

```json
{
    "field_name": [
        "Error message 1",
        "Error message 2"
    ]
}
```

### Common Errors

#### 1. Room Not Found
```json
{
    "detail": "Not found."
}
```

#### 2. Validation Error
```json
{
    "name": ["This field is required."]
}
```

#### 3. Duplicate Room Name
```json
{
    "name": ["room with this name already exists."]
}
```

---

**Note**: Rate Limiting and CORS settings are not currently implemented as the frontend is rendered on the same server.

---

## Testing the API

### Using cURL

#### List Rooms
```bash
curl -X GET http://localhost:8000/api/room/v1/rooms/
```

#### Create Room
```bash
curl -X POST http://localhost:8000/api/room/v1/rooms/create/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Room","description":"Testing","is_public":true}'
```

#### Get Messages
```bash
curl -X GET "http://localhost:8000/api/room/v1/messages/test-room/?offset=0"
```

#### Upload Image
```bash
curl -X POST http://localhost:8000/api/room/v1/upload-image/ \
  -F "image=@/path/to/image.jpg" \
  -F "username=testuser" \
  -F "room_slug=test-room"
```

### Using Python Requests

```python
import requests

# List rooms
response = requests.get('http://localhost:8000/api/room/v1/rooms/')
rooms = response.json()

# Create room
data = {
    'name': 'Python Room',
    'description': 'Created from Python',
    'is_public': True
}
response = requests.post(
    'http://localhost:8000/api/room/v1/rooms/create/',
    json=data
)
room = response.json()

# Upload image
files = {'image': open('image.jpg', 'rb')}
data = {'username': 'pythonuser', 'room_slug': 'python-room'}
response = requests.post(
    'http://localhost:8000/api/room/v1/upload-image/',
    files=files,
    data=data
)
```

### Using WebSocket (JavaScript)

```javascript
// Connect
const socket = new WebSocket('ws://localhost:8000/ws/chat/python-room/');

// Send message
socket.onopen = () => {
    socket.send(JSON.stringify({
        message_type: 'text',
        username: 'pythonuser',
        message: 'Hello from JavaScript!'
    }));
};

// Receive messages
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

---

## API Versioning

Current version: **v1**

Future versions will use URL prefix:
- `/api/room/v1/` - Version 1 (current)
- `/api/room/v2/` - Version 2 (future)

---

## Best Practices

### 1. Always Handle Errors
```javascript
fetch('/api/room/v1/rooms/')
    .then(response => {
        if (!response.ok) {
            throw new Error('API request failed');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

### 2. Use Pagination
```javascript
let offset = 0;
const limit = 50;

async function loadMore() {
    const response = await fetch(
        `/api/room/v1/messages/room-slug/?offset=${offset}`
    );
    const messages = await response.json();
    offset += messages.length;
}
```

### 3. Reconnect WebSocket
```javascript
function connectWebSocket() {
    const socket = new WebSocket('ws://localhost:8000/ws/chat/room/');
    
    socket.onclose = () => {
        console.log('Disconnected. Reconnecting...');
        setTimeout(connectWebSocket, 3000);
    };
    
    return socket;
}
```

---

## Related Documentation

- [Models Documentation](MODELS.md) - Database schema
- [Templates Documentation](TEMPLATES.md) - Frontend integration
- [User Guide](USER_GUIDE.md) - End-user features

---

[← Back to Documentation Index](README.md)
