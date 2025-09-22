# Makefile for ai-workforce-scheduler

.PHONY: generate-all generate-workers generate-drivers generate-workplaces generate-shifts clean

generate-all:
	docker compose run --rm ml python generate_all.py

generate-workers:
	docker compose run --rm ml python generate_workers.py

generate-drivers:
	docker compose run --rm ml python generate_drivers.py

generate-workplaces:
	docker compose run --rm ml python generate_workplaces.py

generate-shifts:
	docker compose run --rm ml python generate_shifts.py

clean:
	rm -f data/*.csv

eda:
	docker compose run --rm ml python eda.py

predict-absences:
	docker compose run --rm ml python predict_absences.py

# ej. make generate-all   or   make generate-shifts
