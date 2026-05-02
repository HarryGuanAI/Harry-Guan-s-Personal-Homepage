# Frontend API Contract

This website is currently a static personal portfolio. There are no live backend requests in the frontend yet.

This document defines the future API surface so backend integration can be added without changing the product model later.

## Conventions

- Base URL placeholder: `https://api.your-domain.com`
- Request body format: JSON unless otherwise noted.
- Response body format: JSON.
- Authentication: not required for public read endpoints. Admin endpoints should use server-side authentication and are not exposed from the public website.
- Error format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable error message"
  }
}
```

## Endpoints

### Submit Contact Message

`POST /v1/contact/messages`

Purpose: collect a visitor message from a future contact form.

Request:

```json
{
  "name": "Visitor name",
  "email": "visitor@example.com",
  "message": "Message content",
  "source": "personal-website"
}
```

Response:

```json
{
  "id": "msg_123",
  "status": "received"
}
```

Security notes:

- Add CAPTCHA or turnstile before enabling this endpoint.
- Rate limit by IP and user agent.
- Validate email and message length server-side.
- Do not expose mailbox credentials to the frontend.

### List Projects

`GET /v1/projects`

Purpose: make project cards CMS-driven later.

Response:

```json
{
  "items": [
    {
      "slug": "vibecode-agent",
      "name": "VibeCode Agent",
      "type": "AI Agent",
      "summary": "Project summary",
      "cover": "https://your-domain.com/Images/generate/example.png",
      "tags": ["AI Agent", "Workflow"],
      "locale": "zh-CN",
      "updatedAt": "2026-05-02T00:00:00Z"
    }
  ]
}
```

### Get Project Detail

`GET /v1/projects/{slug}`

Purpose: power future independent project detail pages.

Response:

```json
{
  "slug": "vibecode-agent",
  "name": "VibeCode Agent",
  "summary": "Project summary",
  "body": "Markdown or structured rich-text content",
  "links": [
    {
      "label": "Demo",
      "url": "https://your-domain.com/projects/vibecode-agent"
    }
  ],
  "seo": {
    "title": "VibeCode Agent",
    "description": "AI Agent coding workflow project"
  },
  "updatedAt": "2026-05-02T00:00:00Z"
}
```

### Track Resume Download

`POST /v1/analytics/resume-downloads`

Purpose: record resume downloads without collecting unnecessary personal data.

Request:

```json
{
  "source": "contact-page",
  "locale": "zh-CN"
}
```

Response:

```json
{
  "status": "ok"
}
```

Privacy notes:

- Prefer aggregated analytics.
- Avoid storing IP addresses unless legally required.
- Publish a privacy note before enabling analytics.

### Client Error Report

`POST /v1/observability/client-errors`

Purpose: capture frontend runtime errors after production deployment.

Request:

```json
{
  "message": "Error message",
  "page": "https://your-domain.com/",
  "userAgent": "Browser user agent",
  "timestamp": "2026-05-02T00:00:00Z"
}
```

Response:

```json
{
  "status": "received"
}
```

Security notes:

- Scrub personal data before storing logs.
- Rate limit heavily.
- Never include secrets in client-side error payloads.

## Current Frontend Readiness

- The current frontend has no backend dependency and can deploy as a static site.
- Future backend integration should be added behind feature flags.
- Before adding API calls, define timeout, retry, loading, empty, and error states in the UI.
