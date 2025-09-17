# Constellation CMDB - Development Makefile
# Simplifies Docker Compose operations for development

.PHONY: help build up down logs shell shell-api shell-neo4j clean restart status

# Default target
help: ## Show this help message
	@echo "Constellation CMDB - Development Commands"
	@echo "======================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Quick Start:"
	@echo "  1. cp .env.example .env"
	@echo "  2. make build"
	@echo "  3. make up"
	@echo "  4. Open http://localhost:7474 (Neo4j Browser)"
	@echo "  5. Open http://localhost:8000/docs (API Documentation)"

# Build all services
build: ## Build all Docker containers
	@echo "🔧 Building Constellation containers..."
	docker compose build

# Start all services (backend only by default)
up: ## Start Neo4j and API services
	@echo "🚀 Starting Constellation services..."
	docker compose up -d neo4j api
	@echo "✅ Services started!"
	@echo "   Neo4j Browser: http://localhost:7474"
	@echo "   API Docs: http://localhost:8000/docs"

# Start all services including frontend
up-all: ## Start all services including frontend
	@echo "🚀 Starting all Constellation services..."
	docker compose --profile frontend up -d
	@echo "✅ All services started!"
	@echo "   Neo4j Browser: http://localhost:7474"
	@echo "   API Docs: http://localhost:8000/docs"
	@echo "   Frontend: http://localhost:3000"

# Stop all services
down: ## Stop all services
	@echo "🛑 Stopping Constellation services..."
	docker compose down

# Stop and remove all containers, networks, and volumes
clean: ## Stop services and clean up volumes
	@echo "🧹 Cleaning up Constellation environment..."
	docker compose down -v --remove-orphans
	docker volume prune -f

# View logs
logs: ## Show logs for all services
	docker compose logs -f

# View API logs only
logs-api: ## Show API logs only
	docker compose logs -f api

# View Neo4j logs only
logs-neo4j: ## Show Neo4j logs only
	docker compose logs -f neo4j

# Restart all services
restart: ## Restart all services
	@echo "🔄 Restarting Constellation services..."
	docker compose restart

# Show service status
status: ## Show status of all services
	@echo "📊 Constellation Services Status:"
	docker compose ps

# Shell access to API container
shell-api: ## Open shell in API container
	docker compose exec api bash

# Shell access to Neo4j container
shell-neo4j: ## Open shell in Neo4j container
	docker compose exec neo4j bash

# Run API tests
test: ## Run API tests
	docker compose exec api python -m pytest tests/ -v

# Run API tests with coverage
test-coverage: ## Run API tests with coverage report
	docker compose exec api python -m pytest tests/ --cov=app --cov-report=html --cov-report=term

# Format code
format: ## Format code with black and isort
	docker compose exec api black app tests
	docker compose exec api isort app tests

# Lint code
lint: ## Lint code with flake8
	docker compose exec api flake8 app tests

# Install new dependencies
install: ## Install new dependencies (run after updating requirements.txt)
	docker compose build api
	docker compose up -d api

# Database operations
db-reset: ## Reset Neo4j database (WARNING: deletes all data)
	@echo "⚠️  This will delete ALL data in Neo4j database!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo ""; \
		echo "🗑️  Resetting database..."; \
		docker compose exec neo4j cypher-shell -u neo4j -p constellation123 "MATCH (n) DETACH DELETE n"; \
		echo "✅ Database reset complete"; \
	else \
		echo ""; \
		echo "❌ Database reset cancelled"; \
	fi

# Backup database
db-backup: ## Backup Neo4j database
	@echo "💾 Creating database backup..."
	mkdir -p backups
	docker compose exec neo4j neo4j-admin dump --database=neo4j --to=/var/lib/neo4j/backups/constellation-$(shell date +%Y%m%d_%H%M%S).dump
	docker cp constellation-neo4j:/var/lib/neo4j/backups/. ./backups/
	@echo "✅ Backup created in ./backups/"

# Load sample data
sample-data: ## Load sample CMDB data
	@echo "📊 Loading sample data..."
	docker compose exec api python scripts/load_sample_data.py
	@echo "✅ Sample data loaded"

# Development workflow
dev: build up ## Quick development setup (build + up)

# Frontend development
frontend-dev: ## Start development with frontend
	@echo "🚀 Starting full stack development (including frontend)..."
	docker compose --profile frontend up -d

frontend-build: ## Build frontend container only
	@echo "🔧 Building frontend container..."
	docker compose build frontend

frontend-logs: ## Show frontend logs
	docker compose logs -f frontend

# Production-like setup (without development volumes)
prod-test: ## Test production-like setup
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Update all containers
update: ## Pull latest images and rebuild
	@echo "🔄 Updating Constellation containers..."
	docker compose pull
	docker compose build --pull
	@echo "✅ Update complete"