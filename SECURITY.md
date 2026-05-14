# Security

## API Keys

Never commit .env to git. Use environment variables in production.

## Input Validation

MIRROR accepts audio files. Validate file types and sizes before processing.

## Rate Limiting

Implement rate limiting on the /generate endpoint to prevent abuse.

## PostHog Data

PostHog events may contain transcript text. Ensure compliance with
privacy regulations if processing sensitive content.

## Reporting Vulnerabilities

Email security issues to rifatasfiachowdhury@gmail.com
