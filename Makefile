# Constellation CMDB - Development Makefile
# =========================================
# Simple commands for development workflow

.PHONY: help setup start start-bg stop restart check logs up-backend check-backend build clean reset db-reset sample-data shell-api shell-neo4j test test-frontend logs-api logs-neo4j logs-live kill-frontend demo

# Default target - show help
help: ## Show available commands
	@echo ""
	@echo "    ╭─────────────────────────────────────────────────────────────╮"
	@echo "    │ ✧   ★ ✦      Configuration Management Database      ✦ ★   ✧ │"
	@echo "    │                                                             │"
	@echo "    │   ______                 __       ____      __  _           │"
	@echo "    │  / ____/___  ____  _____/ /____  / / /___ _/ /_(_)___  ____ │"
	@printf "    │ / /   / __ \\\/ __ \\\/ ___/ __/ _ \\\/ / / __ \`/ __/ / __ \\\/ __ \\\│\n"
	@echo "    │/ /___/ /_/ / / / (__  ) /_/  __/ / / /_/ / /_/ / /_/ / / / /│"
	@printf "    │\\\____/\\\____/_/ /_/____/\\\__/\\\___/_/_/\\\__,_/\\\__/_/\\\____/_/ /_/ │\n"
	@echo "    │                                                             │"
	@echo "    │ ✦   ✧ ★                                             ★ ✧   ✦ │"
	@echo "    ╰─────────────────────────────────────────────────────────────╯"
	@echo ""
	@echo "ESSENTIAL COMMANDS (90% of your usage):"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / && /ESSENTIAL/ {gsub(/## ESSENTIAL /, ""); printf "  \033[32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "ADVANCED COMMANDS:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / && !/ESSENTIAL/ {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "QUICK START:"
	@echo "  1. First time:     make setup"
	@echo "  2. Daily work:     make start-bg"
	@echo "  3. Stop work:      make stop"
	@echo "  4. Check status:   make check"
	@echo ""
	@echo "TIP: Use 'make start' instead of 'start-bg' if you want to see live logs"
	@echo ""

# ============================================================================
# ESSENTIAL COMMANDS - Everything you need for daily development
# ============================================================================

setup: ## ESSENTIAL Setup project for first time (new developers)
	@echo ""
	@echo "    ╭─────────────────────────────────────────────────────────────╮"
	@echo "    │ ✧   ★ ✦          First-time Project Setup           ✦ ★   ✧ │"
	@echo "    │                                                             │"
	@echo "    │   ______                 __       ____      __  _           │"
	@echo "    │  / ____/___  ____  _____/ /____  / / /___ _/ /_(_)___  ____ │"
	@printf "    │ / /   / __ \\\/ __ \\\/ ___/ __/ _ \\\/ / / __ \`/ __/ / __ \\\/ __ \\\│\n"
	@echo "    │/ /___/ /_/ / / / (__  ) /_/  __/ / / /_/ / /_/ / /_/ / / / /│"
	@printf "    │\\\____/\\\____/_/ /_/____/\\\__/\\\___/_/_/\\\__,_/\\\__/_/\\\____/_/ /_/ │\n"
	@echo "    │                                                             │"
	@echo "    │ ✦   ✧ ★                                             ★ ✧   ✦ │"
	@echo "    ╰─────────────────────────────────────────────────────────────╯"
	@echo ""
	@echo "Setting up Constellation for the first time..."
	@echo "=============================================="
	@echo "1. Creating environment file..."
	@cp .env.example .env 2>/dev/null || echo "   ✅ .env already exists"
	@echo "2. Building Docker containers..."
	@docker compose build
	@echo "3. Installing frontend dependencies..."
	@cd frontend && npm install --legacy-peer-deps --silent
	@echo "4. Starting services for the first time..."
	@$(MAKE) up-backend
	@echo "5. Waiting for services to be ready..."
	@sleep 5
	@$(MAKE) check-backend
	@echo ""
	@echo "🎉 Setup complete! Your project is ready."
	@echo "💡 Run 'make start' to begin development"

start: ## ESSENTIAL Start development (backend + frontend)
	@echo ""
	@echo "    ╭─────────────────────────────────────────────────────────────╮"
	@echo "    │ ✧   ★ ✦      Starting Development Environment       ✦ ★   ✧ │"
	@echo "    │                                                             │"
	@echo "    │   ______                 __       ____      __  _           │"
	@echo "    │  / ____/___  ____  _____/ /____  / / /___ _/ /_(_)___  ____ │"
	@printf "    │ / /   / __ \\\/ __ \\\/ ___/ __/ _ \\\/ / / __ \`/ __/ / __ \\\/ __ \\\│\n"
	@echo "    │/ /___/ /_/ / / / (__  ) /_/  __/ / / /_/ / /_/ / /_/ / / / /│"
	@printf "    │\\\____/\\\____/_/ /_/____/\\\__/\\\___/_/_/\\\__,_/\\\__/_/\\\____/_/ /_/ │\n"
	@echo "    │                                                             │"
	@echo "    │ ✦   ✧ ★                                             ★ ✧   ✦ │"
	@echo "    ╰─────────────────────────────────────────────────────────────╯"
	@echo ""
	@echo "Starting Constellation Development Stack"
	@echo "======================================="
	@$(MAKE) up-backend
	@echo "⏳ Waiting for backend to be ready..."
	@sleep 3
	@$(MAKE) check-backend
	@echo "Starting frontend development server..."
	@echo ""
	@echo "🎯 Ready! Your URLs:"
	@echo "   Frontend:  http://localhost:5173"
	@echo "   API Docs:  http://localhost:8000/docs"
	@echo "   Neo4j:     http://localhost:7474"
	@echo ""
	@cd frontend && npm run dev

start-bg: ## ESSENTIAL Start everything in background
	@echo ""
	@echo "    ╭─────────────────────────────────────────────────────────────╮"
	@echo "    │ ✧   ★ ✦         Background Development Mode         ✦ ★   ✧ │"
	@echo "    │                                                             │"
	@echo "    │   ______                 __       ____      __  _           │"
	@echo "    │  / ____/___  ____  _____/ /____  / / /___ _/ /_(_)___  ____ │"
	@printf "    │ / /   / __ \\\/ __ \\\/ ___/ __/ _ \\\/ / / __ \`/ __/ / __ \\\/ __ \\\│\n"
	@echo "    │/ /___/ /_/ / / / (__  ) /_/  __/ / / /_/ / /_/ / /_/ / / / /│"
	@printf "    │\\\____/\\\____/_/ /_/____/\\\__/\\\___/_/_/\\\__,_/\\\__/_/\\\____/_/ /_/ │\n"
	@echo "    │                                                             │"
	@echo "    │ ✦   ✧ ★                                             ★ ✧   ✦ │"
	@echo "    ╰─────────────────────────────────────────────────────────────╯"
	@echo ""
	@echo "Starting Constellation (Background Mode)"
	@echo "======================================="
	@$(MAKE) up-backend
	@echo "⏳ Waiting for backend to be ready..."
	@sleep 3
	@$(MAKE) check-backend
	@echo "🌐 Starting frontend in background..."
	@cd frontend && npm run dev > /dev/null 2>&1 &
	@sleep 2
	@echo ""
	@echo "✅ Everything is running in background!"
	@echo "🎯 Your URLs:"
	@echo "   Frontend:  http://localhost:5173"
	@echo "   API Docs:  http://localhost:8000/docs"
	@echo "   Neo4j:     http://localhost:7474"
	@echo ""
	@echo "💡 Use 'make stop' to stop everything"
	@echo "💡 Use 'make logs' to see logs"

stop: ## ESSENTIAL Stop all services
	@echo "🛑 Stopping all Constellation services..."
	@echo "1. Stopping frontend processes..."
	@echo '#!/bin/bash' > /tmp/stop_frontend.sh
	@echo 'pkill -f "npm run dev" 2>/dev/null || true' >> /tmp/stop_frontend.sh
	@echo 'pkill -f "vite" 2>/dev/null || true' >> /tmp/stop_frontend.sh
	@chmod +x /tmp/stop_frontend.sh
	@/tmp/stop_frontend.sh
	@rm -f /tmp/stop_frontend.sh
	@sleep 1
	@echo "2. Stopping backend services..."
	@docker compose down
	@echo "✅ All services stopped"

restart: ## ESSENTIAL Restart everything
	@echo "🔄 Restarting Constellation..."
	@$(MAKE) stop
	@sleep 2
	@$(MAKE) start-bg

check: ## ESSENTIAL Check status of all services
	@echo "🔍 Constellation Status Check"
	@echo "============================"
	@$(MAKE) check-backend
	@echo ""
	@echo "Frontend Service:"
	@if ps aux | grep -v grep | grep -E "(npm run dev|vite)" > /dev/null 2>&1; then \
		echo "✅ Frontend dev server is running"; \
		if curl -s http://localhost:5173 > /dev/null 2>&1; then \
			echo "✅ Frontend responding at http://localhost:5173"; \
		else \
			echo "❌ Frontend not responding"; \
		fi; \
	else \
		echo "❌ Frontend dev server is not running"; \
	fi
	@echo ""
	@echo "🌐 Quick Access:"
	@echo "   Frontend:  http://localhost:5173"
	@echo "   API Docs:  http://localhost:8000/docs"
	@echo "   Neo4j:     http://localhost:7474"

logs: ## ESSENTIAL View logs from all services
	@echo "📋 Constellation Logs"
	@echo "===================="
	@echo "Backend logs:"
	@docker compose logs --tail=20 api neo4j
	@echo ""
	@echo "💡 For live logs: docker compose logs -f"
	@echo "💡 Frontend logs: check terminal where you ran 'make start'"

# ============================================================================
# ADVANCED COMMANDS - For specific needs and troubleshooting
# ============================================================================

up-backend: ## Start only backend services (Neo4j + API)
	@echo "🚀 Starting backend services..."
	@docker compose up -d neo4j api
	@echo "✅ Backend services started"

check-backend: ## Check backend services health
	@echo "Backend Services:"
	@docker compose ps
	@echo ""
	@echo "Health Checks:"
	@if curl -s http://localhost:8000/health > /dev/null 2>&1; then \
		echo "✅ API is healthy at http://localhost:8000"; \
	else \
		echo "❌ API is not responding"; \
	fi
	@if curl -s http://localhost:7474 > /dev/null 2>&1; then \
		echo "✅ Neo4j is healthy at http://localhost:7474"; \
	else \
		echo "❌ Neo4j is not responding"; \
	fi

build: ## Rebuild Docker containers
	@echo "🔧 Building Constellation containers..."
	@docker compose build

clean: ## Clean up containers and volumes
	@echo "🧹 Cleaning up Constellation environment..."
	@docker compose down -v --remove-orphans
	@docker system prune -f
	@echo "✅ Cleanup complete"

reset: ## Complete reset (clean + build + setup)
	@echo "🔄 Complete reset of Constellation..."
	@$(MAKE) clean
	@$(MAKE) build
	@$(MAKE) up-backend
	@echo "✅ Reset complete"

# Database operations
db-reset: ## Reset Neo4j database (⚠️ DELETES ALL DATA)
	@echo "⚠️  WARNING: This will delete ALL data in Neo4j!"
	@read -p "Are you sure? Type 'yes' to continue: " response; \
	if [ "$$response" = "yes" ]; then \
		echo "🗑️  Resetting database..."; \
		docker compose exec neo4j cypher-shell -u neo4j -p constellation123 "MATCH (n) DETACH DELETE n"; \
		echo "✅ Database reset complete"; \
	else \
		echo "❌ Database reset cancelled"; \
	fi

sample-data: ## Load sample CMDB data
	@echo "📊 Loading sample data..."
	@docker compose exec api python scripts/load_sample_data.py
	@echo "✅ Sample data loaded"

# Shell access
shell-api: ## Open shell in API container
	@docker compose exec api bash

shell-neo4j: ## Open shell in Neo4j container  
	@docker compose exec neo4j bash

# Testing
test: ## Run API tests
	@echo "🧪 Running API tests..."
	@docker compose exec api python -m pytest tests/ -v

test-frontend: ## Run frontend tests
	@echo "🧪 Running frontend tests..."
	@cd frontend && npm test

# Development utilities
logs-api: ## Show API logs only
	@docker compose logs -f api

logs-neo4j: ## Show Neo4j logs only
	@docker compose logs -f neo4j

logs-live: ## Show live logs for all services
	@docker compose logs -f

kill-frontend: ## Force kill frontend processes
	@echo "🔪 Force killing frontend processes..."
	@pkill -9 -f "npm run dev" 2>/dev/null || true
	@pkill -9 -f "vite" 2>/dev/null || true
	@echo "✅ Frontend processes killed"

# Containers-only mode (for demos/production testing)
demo: ## Start everything in containers (demo mode)
	@echo "🎬 Starting Constellation in demo mode..."
	@docker compose --profile frontend up -d
	@echo "✅ Demo mode started - all services in containers"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "📚 API Docs: http://localhost:8000/docs"