# Deploying MIRROR

## Local Development

```bash
uvicorn api.app:app --reload
```

## Production Deployment

### Option 1: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 2: Railway

1. Connect your GitHub repo
2. Add environment variables in Railway dashboard
3. Deploy

### Option 3: Fly.io

```bash
fly launch
fly secrets set HEYGEN_API_KEY=...
fly deploy
```

## Environment Variables

All API keys must be set as environment variables in production.
Never commit .env to git.

## Monitoring

Use PostHog dashboards to monitor:
- Pipeline success rate
- Average duration
- Cost per generation
- Quality scores
