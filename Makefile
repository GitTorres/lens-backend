# bash:
# 	docker exec -it fastapi bash
up:
	docker compose up --no-deps -d
up_prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
down:
	docker compose down
rebuild:
	docker compose up -d --build --force-recreate --renew-anon-volumes --no-deps
build:
	docker compose build
test_utils:
	docker compose exec fastapi pytest . -sv -m "utils"
test_put:
	docker compose exec fastapi pytest . -sv -m "put"
remove:
	docker compose down
	docker container rm lens-backend_fastapi:latest || true
	docker image rm lens-backend_fastapi:latest || true

# https://qavalidation.com/2021/01/pytest-options-how-to-skip-or-run-specific-tests.html/
# https://pawamoy.github.io/posts/pass-makefile-args-as-typed-in-command-line/
# https://stackoverflow.com/questions/34228864/docker-stop-and-delete-docker-container-if-its-running