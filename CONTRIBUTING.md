# Contributing to MIRROR

## Development Setup

1. Fork the repo
2. Clone your fork
3. Install dependencies: pip install -r requirements.txt
4. Copy .env.example to .env and add your API keys
5. Run tests: pytest test_mirror.py -v

## Code Style

- Use type hints where possible
- Follow PEP 8
- Keep functions under 50 lines
- Add docstrings to all public functions

## Testing

Add tests for new features in test_mirror.py.
Run pytest before submitting a PR.

## Pull Request Process

1. Update README.md if you add features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description
