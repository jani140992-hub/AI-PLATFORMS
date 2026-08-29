.PHONY: help install-backend install-frontend build test lint clean docker-up docker-down seed migrate

help:
	@echo "OmniFlow AI Platform - Available Commands:"
	@echo "  install-backend   Install Python backend dependencies"
	@echo "  install-frontend  Install Next.js frontend dependencies"
	@echo "  build             Build backend and frontend artifacts"
	@echo "  test              Run full test suites"
	@echo "  lint              Run linter and code formatters"
	@echo "  docker-up         Launch complete environment via Docker Compose"
	@echo "  docker-down       Tear down docker environment"
	@echo "  migrate           Run database migrations via Alembic"
	@echo "  seed              Seed database with demo workflows and knowledge bases"

install-backend:
	cd backend && pip install -e ".[dev]"

install-frontend:
	cd frontend && npm install

build:
	cd backend && python -m build
	cd frontend && npm run build

test:
	cd backend && pytest tests/ -v
	cd frontend && npm test

lint:
	ruff check backend/
	black --check backend/
	cd frontend && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf backend/build backend/dist backend/*.egg-info

docker-up:
	docker-compose -f deployments/docker/docker-compose.yml up -d

docker-down:
	docker-compose -f deployments/docker/docker-compose.yml down -v

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python scripts/seed_database.py
