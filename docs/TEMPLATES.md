# Templates Documentation

This document describes the HTML templates used in the Django Chat Application frontend.

## Table of Contents
- [Overview](#overview)
- [Room List Template](#room-list-template)
- [Chat Room Template](#chat-room-template)
- [Create Room Template](#create-room-template)
- [Common Features](#common-features)
- [Customization](#customization)

---

## Overview

The application uses Django templates with embedded JavaScript for dynamic functionality. All templates follow a modern, responsive design with RTL (Right-to-Left) support for Persian/Farsi language.

### Template Location
```
templates/
└── chat/
    ├── room_list.html
    ├── room.html
    └── create_room.html
```

### Key Technologies
- **Pure HTML/CSS**: No external CSS frameworks
- **Vanilla JavaScript**: No frontend framework dependencies
- **WebSocket API**: Real-time communication
- **Fetch API**: RESTful API calls
- **Modern CSS**: Flexbox, Grid, Gradients, Animations

---

## Room List Template

**File**: `templates/chat/room_list.html`

### Purpose
Displays a list of all public chat rooms and provides a modal to create new rooms.

### Features
- **Dynamic Room Loading**: Fetches rooms from REST API
- **Room Cards**: Grid layout with room information
- **Create Room Modal**: In-page form for room creation
- **Real-time Updates**: Automatic room list refresh

### Structure

#### 1. Header Section
```html
<div class="header">
    <h1>اتاق‌های چت</h1>
    <p>به اتاق‌های مختلف بپیوندید و با دیگران گفتگو کنید</p>
    <button onclick="showCreateRoomModal()">ایجاد اتاق جدید</button>
</div>
```

#### 2. Room Grid
```html
<div class="rooms-grid" id="roomsGrid">
    <!-- Dynamically loaded room cards -->
</div>
```

Each room card displays:
- Room name
- Description
- Member count
- Creator username
- Join button

#### 3. Create Room Modal
```html
<div id="createRoomModal" class="modal">
    <form id="createRoomForm">
        <!-- Room name input -->
        <!-- Description textarea -->
        <!-- Public/Private checkbox -->
    </form>
</div>
```

### JavaScript Functions

#### `loadRooms()`
Fetches room list from API endpoint `/api/room/v1/rooms/`

```javascript
async function loadRooms() {
    const response = await fetch('/api/room/v1/rooms/');
    const rooms = await response.json();
    // Display rooms in grid
}
```

#### `createRoomCard(room)`
Generates HTML for individual room card

#### `showCreateRoomModal()` / `hideCreateRoomModal()`
Controls modal visibility

#### Form Submission
Posts new room data to `/api/room/v1/rooms/create/`

### Styling Highlights
- **Color Scheme**: Green gradient (#075e54, #128c7e)
- **Layout**: CSS Grid with auto-fill
- **Responsive**: Mobile-friendly with media queries
- **Animations**: Hover effects and smooth transitions

---

## Chat Room Template

**File**: `templates/chat/room.html`

### Purpose
Main chat interface for sending/receiving messages, images, and viewing history.

### Features
- **Real-time Messaging**: WebSocket-based instant messaging
- **Image Upload**: Send and receive images
- **Infinite Scroll**: Load previous messages on scroll
- **Message Types**: Text and image messages
- **Username Management**: Local storage for username
- **Auto-reconnect**: WebSocket reconnection on disconnect

### Structure

#### 1. Chat Header
```html
<div class="chat-header">
    <h2>💬 {{ room_name }}</h2>
    <div class="user-info">
        <span id="current-user-display">مهمان</span>
    </div>
</div>
```

#### 2. Message Container
```html
<div id="chat-messages">
    <!-- Messages loaded via API and WebSocket -->
    <div class="history-loading">⏳ Loading older messages...</div>
</div>
```

#### 3. Input Area
```html
<div class="chat-input-container">
    <!-- Username setup (if needed) -->
    <!-- Image preview -->
    <!-- Message textarea -->
    <!-- Attach button -->
    <!-- Send button -->
</div>
```

### JavaScript Components

#### WebSocket Connection
```javascript
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomSlug + '/'
);
```

#### Message Loading

**Initial Messages**
```javascript
async function loadInitialMessages() {
    const url = `/api/room/v1/messages/${roomSlug}/?offset=0`;
    const response = await fetch(url);
    const messages = await response.json();
    // Display messages
}
```

**Infinite Scroll**
```javascript
async function loadMoreMessages() {
    const url = `/api/room/v1/messages/${roomSlug}/?offset=${messageOffset}`;
    // Fetch and prepend older messages
}
```

#### Sending Messages

**Text Message**
```javascript
function sendMessage() {
    chatSocket.send(JSON.stringify({
        'message_type': 'text',
        'username': currentUsername,
        'message': message
    }));
}
```

**Image Upload**
```javascript
async function uploadImage() {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('username', currentUsername);
    formData.append('room_slug', roomSlug);
    
    const response = await fetch('/api/room/v1/upload-image/', {
        method: 'POST',
        body: formData
    });
}
```

#### Message Display
```javascript
function displayMessage(data, insertAtTop = false) {
    // Creates message bubble with:
    // - Username
    // - Content/Image
    // - Timestamp
    // Applies 'own' or 'other' class based on sender
}
```

### Message Types

#### Text Message
```html
<div class="message own/other">
    <div class="message-bubble">
        <div class="message-username">Username</div>
        <div class="message-content">Message text</div>
        <div class="message-time">12:30</div>
    </div>
</div>
```

#### Image Message
```html
<div class="message own/other">
    <div class="message-bubble">
        <div class="message-username">Username</div>
        <img class="message-image" src="..." alt="Image">
        <div class="message-time">12:30</div>
    </div>
</div>
```

### State Management

#### Local Storage
```javascript
// Username persistence
localStorage.setItem('chatUsername', username);
const currentUsername = localStorage.getItem('chatUsername');
```

#### Pagination State
```javascript
let messageOffset = 0;       // Current offset for pagination
let isLoadingHistory = false; // Loading state
let hasMoreMessages = true;   // More messages available
```

### Styling Highlights
- **Color Scheme**: Purple gradient (#667eea, #764ba2)
- **Message Bubbles**: Different styling for own/other messages
- **Animations**: Slide-in effect for new messages
- **Scrollbar**: Custom styled scrollbar
- **Responsive**: Mobile-optimized layout

---

## Create Room Template

**File**: `templates/chat/create_room.html`

### Purpose
Standalone page for creating new chat rooms (if separate from modal).

### Features
Similar to the modal in room_list.html, but as a dedicated page:
- Room name input
- Description textarea
- Public/Private toggle
- Form validation
- Success/Error messages

---

## Common Features

### 1. RTL Support
All templates support Right-to-Left layout for Persian/Farsi:
```html
<html lang="fa" dir="rtl">
```

### 2. Responsive Design
Media queries for mobile devices:
```css
@media (max-width: 768px) {
    .chat-container {
        height: 100vh;
        border-radius: 0;
    }
}
```

### 3. Loading States
Visual feedback during async operations:
- Loading spinners
- Skeleton screens
- Status messages

### 4. Error Handling
User-friendly error messages:
- Connection errors
- API failures
- Upload failures

### 5. Animations
Smooth transitions and effects:
```css
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

---

## Customization

### Changing Colors

**Room List** (Green theme):
```css
.header {
    background: #075e54; /* WhatsApp green */
}
```

**Chat Room** (Purple theme):
```css
.chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Modifying Layout

**Grid Columns**:
```css
.rooms-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
```

**Chat Container Size**:
```css
.chat-container {
    max-width: 900px;
    max-height: 700px;
}
```

### Adding New Features

#### Example: Add "Typing..." Indicator

1. **HTML**:
```html
<div id="typing-indicator" style="display: none;">
    Someone is typing...
</div>
```

2. **JavaScript**:
```javascript
// Listen for typing events
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'typing') {
        showTypingIndicator(data.username);
    }
};
```

3. **Send typing event**:
```javascript
messageInput.addEventListener('input', function() {
    chatSocket.send(JSON.stringify({
        'type': 'typing',
        'username': currentUsername
    }));
});
```

---

## API Integration

### REST API Endpoints Used

| Endpoint | Method | Purpose | Template |
|----------|--------|---------|----------|
| `/api/room/v1/rooms/` | GET | List all rooms | room_list.html |
| `/api/room/v1/rooms/create/` | POST | Create new room | room_list.html |
| `/api/room/v1/messages/${slug}/` | GET | Get room messages | room.html |
| `/api/room/v1/upload-image/` | POST | Upload image | room.html |

### WebSocket Endpoint

```
ws://localhost:8000/ws/chat/{room_slug}/
```

**Message Format**:
```json
{
    "message_type": "text",
    "username": "user123",
    "message": "Hello world",
    "timestamp": "2025-11-08T12:00:00Z"
}
```

---

## Best Practices

### 1. Progressive Enhancement
Core functionality works without JavaScript, enhanced with JS

### 2. Accessibility
- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support

### 3. Performance
- Lazy loading of messages
- Image optimization
- Debounced scroll events

### 4. Security
- No inline event handlers in production
- CSP-compliant code
- Input sanitization

### 5. Error Handling
```javascript
try {
    const response = await fetch('/api/...');
    if (!response.ok) throw new Error('API Error');
    // Handle response
} catch (error) {
    console.error('Error:', error);
    showErrorMessage('Something went wrong');
}
```

---

## Template Variables

### Django Context Variables

**room_list.html**:
```python
context = {
    'rooms': Room.objects.filter(is_public=True)
}
```

**room.html**:
```python
context = {
    'room_name': room.name,
    'room_slug': room.slug,
}
```

### Accessing in Templates
```html
<h2>{{ room_name }}</h2>
<script>
    const roomSlug = '{{ room_slug }}';
</script>
```

---

## Troubleshooting

### Issue: Messages not loading

**Check**:
1. API endpoint is accessible
2. CORS settings are correct
3. Browser console for errors

### Issue: WebSocket connection fails

**Check**:
1. Redis is running
2. Channels configuration is correct
3. WebSocket URL is correct (ws:// not http://)

### Issue: Images not displaying

**Check**:
1. MEDIA_URL is configured
2. Image upload permissions
3. File size limits

---

## Future Enhancements

Potential template improvements:

1. **Dark Mode**: Add theme switcher
2. **Emoji Picker**: Integrate emoji selector
3. **File Attachments**: Support PDFs, documents
4. **Voice Messages**: Audio recording
5. **Read Receipts**: Message read status
6. **Reactions**: Emoji reactions to messages
7. **Message Editing**: Edit sent messages
8. **Search**: Search messages in room

---

[← Back to Documentation Index](README.md)
