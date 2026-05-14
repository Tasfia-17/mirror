.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest test_mirror.py -v

run:
	python mirror.py

api:
	uvicorn api.app:app --reload

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t mirror .

docker-run:
	docker-compose up
