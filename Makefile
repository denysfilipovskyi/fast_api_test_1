run:
	docker compose up --build

stop:
	docker compose down

clean:
	docker compose down -v --rmi all

logs:
	docker compose logs -f app

restart:
	docker compose down && docker compose up --build

init_db:
	docker compose exec app poetry run python3 users_crm/init_db.py

test:
	PYTHONPATH=$(PWD)/users_crm poetry run pytest