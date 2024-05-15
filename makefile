install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

docker-build:
	docker build -t ta-infra-manager .

docker-run:
	docker run -dp 8000:8000 ta-infra-manager