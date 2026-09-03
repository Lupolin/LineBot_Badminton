local-env:
	docker-compose -f docker/docker-compose-dev.yml -p dev up --build -d

local-env-rm:
	docker-compose -f docker/docker-compose-dev.yml -p dev down -v

test-env:
	docker-compose -f docker/docker-compose-test.yml -p test up --build -d

test-env-rm:
	docker-compose -f docker/docker-compose-test.yml -p test down -v

format:
	source .venv/bin/activate && ruff format .

lint:
	source .venv/bin/activate && ruff check . && mypy .

unit-test:
	source .venv/bin/activate && pytest tests/unit --log-cli-level=INFO -s

integration-test:
	make test-env
	ENV=test pytest tests/integration/
	make test-env-rm
