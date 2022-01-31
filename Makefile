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