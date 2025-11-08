# Models Documentation

Database models structure for the chat application.

---

## Room Model

The `Room` model represents a chat room where users can communicate.

### Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `name` | CharField | Room name | max_length=100, unique=True |
| `slug` | SlugField | URL-friendly room identifier | max_length=100, unique=True, auto-generated |
| `description` | TextField | Room description | blank=True, null=True |
| `creator` | ForeignKey | User who created the room | User model, SET_NULL on delete |
| `members` | ManyToManyField | Users who are members | User model, blank=True |
| `is_public` | BooleanField | Public/Private room flag | default=True |
| `created_at` | DateTimeField | Room creation timestamp | auto_now_add=True |
| `updated_at` | DateTimeField | Last update timestamp | auto_now=True |


## Message Model

The `Message` model represents individual messages sent in chat rooms.

### Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `room` | ForeignKey | Room where message was sent | Room model, CASCADE on delete |
| `user` | ForeignKey | User who sent the message | User model, CASCADE on delete |
| `content` | TextField | Text content of the message | blank=True, null=True |
| `image` | ImageField | Image attachment | upload_to='chat_images/', blank=True, null=True |
| `message_type` | CharField | Type of message (text/image) | max_length=10, choices=['text', 'image'], default='text' |
| `timestamp` | DateTimeField | Message timestamp | auto_now_add=True |

**Message Types**: text, image

---

[← Back to Documentation Index](README.md)
