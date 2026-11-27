# Assistant Core — Foundation v0.2

## Implemented
- Chat request/response contracts.
- Session IDs for conversations.
- In-memory conversation history.
- Chat API endpoint.
- History read and conversation deletion endpoints.
- Explicit provider status so the UI cannot misrepresent stub replies as AI-generated.

## API
- `GET /api/health` — service health
- `POST /api/chat` — accept a message and return a session ID/reply
- `GET /api/conversations/{id}/history` — read session history
- `DELETE /api/conversations/{id}` — clear session

## Current limitation
The response is a clearly labeled foundation placeholder. No LLM/provider is configured. Session data is in-memory and resets when the backend restarts. The next milestone is provider abstraction/configuration and persistence, with secrets supplied through local environment variables rather than committed files.
