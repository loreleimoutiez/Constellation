# Constellation
[![Status](https://img.shields.io/badge/status-in%20development-orange)]()

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Constellation** is a modern Configuration Management Database (CMDB) that uses graph technology to track and visualize all your organization's assets - from infrastructure and applications to people, processes, and policies.

## Quick Start

**New to Constellation? Get everything running in 3 steps:**

```bash
# 1. Clone the repository
git clone https://github.com/loreleimoutiez/Constellation.git
cd Constellation

# 2. First time setup
make setup

# 3. Start development environment  
make start-bg
```

**That's it!** Everything is now running:
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs  
- **Neo4j Browser:** http://localhost:7474 (neo4j/constellation123)

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Node.js 18+** for frontend development
- 4GB+ RAM available
- Ports 5173, 7474, 7687, 8000 available

## Development Commands

Tip: run `make help` anytime to see all available commands.

<details>
<summary>Click to expand commands</summary>
  
| Command | Description |
|---------|-------------|
| `make setup` | **First-time setup** (new developers) |
| `make start` | **Start development** (shows frontend logs) |
| `make start-bg` | **Start in background** (frees terminal) |
| `make stop` | **Stop everything** |
| `make restart` | **Restart all services** |
| `make check` | **Check status** of all services |
| `make logs` | **View logs** from all services |

</details>
<details>
<summary>Click to expand advanced options</summary>

| Command | Description |
|---------|-------------|
| `make build` | Rebuild Docker containers |
| `make clean` | Clean up containers and volumes |
| `make reset` | Complete reset (clean + build + setup) |
| `make shell-api` | Shell access to API container |
| `make test` | Run API tests |
| `make test-frontend` | Run frontend tests |
| `make sample-data` | Load sample CMDB data |
| `make db-reset` | Reset database (DELETES ALL DATA) |
| `make demo` | Start everything in containers (demo mode) |

</details>

## Use Cases

- **"What breaks if this server fails?"** → Impact Analysis
- **"Who has access to this system?"** → Dependency tracking  
- **"Which services have no backup maintainer?"** → Bus factor analysis
- **"What policies cover this data?"** → Compliance mapping
- **"What's the blast radius of this change?"** → Change impact assessment

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js 3      │    │   FastAPI       │    │   Neo4j 5       │
│   Frontend      │────│   Backend       │────│   Database      │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • CRUD APIs     │    │ • Assets        │
│ • Asset Mgmt    │    │ • Impact Query  │    │ • Relationships │
│ • Impact Views  │    │ • Search        │    │ • Change Log    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Key Features

### Current Features
- **Graph Database**: Neo4j for powerful relationship modeling
- **Modern Frontend**: Vue.js 3 + TypeScript + Tailwind CSS responsive interface
- **RESTful API**: Complete CRUD operations with FastAPI
- **Asset Management**: Track hardware, software, people, processes, policies
- **Impact Analysis**: Understand dependencies and blast radius of changes
- **Search & Filtering**: Text search and advanced filtering capabilities
- **Health Monitoring**: Service health checks and monitoring

## Development Workflow

### Daily Development
```bash
# Start your development session
make start-bg      # Everything runs in background

# Check status anytime
make check         # See what's running

# View logs when needed
make logs          # Backend logs
make logs-api      # API logs only

# End your session
make stop          # Stop everything cleanly
```

## API Endpoints

The API provides comprehensive Configuration Item management:

### Core Operations
- `GET /api/v1/cis` - List all CIs with filtering
- `POST /api/v1/cis` - Create new CI
- `GET /api/v1/cis/{id}` - Get specific CI details
- `PUT /api/v1/cis/{id}` - Update CI
- `DELETE /api/v1/cis/{id}` - Delete CI

### Impact Analysis
- `GET /api/v1/impact/{id}` - Analyze impact of CI failure
- `GET /api/v1/dependencies/{id}` - Get CI dependencies
- `GET /api/v1/busfactor` - Identify critical single points of failure

### System
- `GET /health` - Health check with database status
- `GET /docs` - Interactive API documentation

**Full API documentation:** http://localhost:8000/docs (when running)

## Data Model

Constellation models your infrastructure as interconnected nodes:

- **Configuration Items**: Hardware, Software, Services, Applications
- **Human Assets**: People, Teams, Roles, Skills  
- **Governance**: Processes, Policies, Controls, Risks
- **External**: Vendors, Partners, Contracts
- **Digital Assets**: Datasets, Identities, Credentials

## Testing

```bash
make test           # Run API tests
make test-frontend  # Run frontend tests
```

## Configuration

Key environment variables (configured automatically by `make setup`):

```bash
# Database
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=constellation123

# API
PROJECT_NAME=Constellation
API_V1_STR=/api/v1

# Development
ENVIRONMENT=development
```

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Links

- [Issues](https://github.com/loreleimoutiez/Constellation/issues)
- [API Documentation](http://localhost:8000/docs) (when running)

---

**Ready to start?** Clone the repo, then run `make setup` and `make start-bg` - you're good to go!
