up:
	docker compose up -d
down:
	docker compose down
bash:
	docker exec -it fastapi bash
build:
	docker compose build