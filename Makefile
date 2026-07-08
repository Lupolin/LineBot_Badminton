local-env:
	docker-compose -f docker/docker-compose-dev.yml -p dev up --build -d

local-env-rm:
	docker-compose -f docker/docker-compose-dev.yml -p dev down -v

lint:
	source .venv/bin/activate && ruff check . && mypy .

unit-test:
	pytest tests/unit --log-cli-level=INFO -s

format:
	source .venv/bin/activate && ruff format .