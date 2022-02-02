up:
	docker compose up -d
down:
	docker compose down
rebuild:
	docker compose up -d --build 
bash:
	docker exec -it fastapi bash
build:
	docker compose build
test_utils:
	docker compose exec fastapi pytest . -sv -m "utils"
test_put:
	docker compose exec fastapi pytest . -sv -m "put"

# https://qavalidation.com/2021/01/pytest-options-how-to-skip-or-run-specific-tests.html/
# https://pawamoy.github.io/posts/pass-makefile-args-as-typed-in-command-line/