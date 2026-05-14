# MIRROR Quickstart

Get MIRROR running in 5 minutes.

## 1. Clone and install

```bash
git clone https://github.com/Tasfia-17/mirror.git
cd mirror
pip install -r requirements.txt
```

## 2. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```
ELEVENLABS_API_KEY=   # https://elevenlabs.io/app/settings/api-keys
HEYGEN_API_KEY=       # https://app.heygen.com/settings/api
FAL_KEY=              # https://fal.ai/dashboard/keys
POSTHOG_API_KEY=      # https://app.posthog.com/project/settings
OPENAI_API_KEY=       # https://platform.openai.com/api-keys
```

## 3. Run the CLI

```bash
python mirror.py your_voice_memo.mp3
```

The pipeline takes 15-90 seconds depending on API latency.

## 4. Run the web API

```bash
uvicorn api.app:app --reload
```

Open http://localhost:8000/static/index.html in your browser.

## 5. Run tests

```bash
pip install pytest
pytest test_mirror.py -v
```

## Troubleshooting

**EnvironmentError: Missing required environment variable**
Copy `.env.example` to `.env` and add your API keys.

**ModuleNotFoundError**
Run `pip install -r requirements.txt` again.

**HeyGen API error**
Check your API key at https://app.heygen.com/settings/api.
Make sure you have credits available.

**Fal API error**
Check your key at https://fal.ai/dashboard/keys.
Kling 2.1 Pro requires a paid Fal account.
