.PHONY: demo up down logs backup restore check migrate migrate-status migrate-rollback gitops-validate test test-demo test-production

demo: up check backup
	@echo "Demo complete. Try: make logs"

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

check:
	bash scripts/check_replication.sh

backup:
	bash scripts/backup.sh

restore:
	bash scripts/restore.sh

migrate:
	bash scripts/migrate.sh

migrate-status:
	bash scripts/migrate_status.sh

migrate-rollback:
	bash scripts/migrate_rollback.sh

gitops-validate:
	@python3 scripts/gitops_validate.py

test: test-demo

test-demo:
	@TEST_MODE=demo python3 tests/run_tests.py

test-production:
	@TEST_MODE=production python3 tests/run_tests.py
