# Constellation

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Constellation is an open-source Configuration Management Database (CMDB) built for modern infrastructure management. It provides a graph-based approach to track and visualize all your organization's assets - from hardware and software to people, processes, and policies.

## 🎯 Vision

Create a comprehensive, visual, and intuitive CMDB that goes beyond traditional infrastructure tracking to include intangible assets like datasets, human resources, processes, and governance elements.

## ✨ Key Features

- **Graph Database Foundation**: Built on Neo4j for powerful relationship modeling
- **Full Stack Architecture**: FastAPI backend + Vue.js frontend
- **Asset Diversity**: Track tangible (hardware, software) and intangible (people, processes, policies) assets
- **Impact Analysis**: Understand dependencies and blast radius of changes
- **RACI Management**: Track responsibilities and accountabilities
- **Compliance Tracking**: Monitor policy coverage and compliance status
- **Audit Trail**: Complete change history with who/when/what tracking

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js        │    │   FastAPI       │    │   Neo4j         │
│   Frontend      │────│   Backend       │────│   Database      │
│                 │    │                 │    │                 │
│ • Graph View    │    │ • CRUD APIs     │    │ • Assets        │
│ • Asset Mgmt    │    │ • Impact Query  │    │ • Relationships │
│ • Query Builder │    │ • Auth & RBAC   │    │ • Change Log    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- At least 4GB RAM available for containers
- Ports 7474, 7687, and 8000 available

### Development Setup

1. **Clone and setup**:
   ```bash
   git clone https://github.com/loreleimoutiez/Constellation.git
   cd Constellation
   ./dev-setup.sh
   ```

2. **Or manual setup**:
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Build and start services
   make dev
   
   # View logs
   make logs
   ```

3. **Access the services**:
   - 📊 **Neo4j Browser**: http://localhost:7474
     - Username: `neo4j`
     - Password: `constellation123`
   - 📚 **API Documentation**: http://localhost:8000/docs
   - 🔍 **API Health Check**: http://localhost:8000/health

### Available API Endpoints

The API provides comprehensive Configuration Item management:

- **CRUD Operations**:
  - `POST /api/v1/cis` - Create new CI
  - `GET /api/v1/cis` - List CIs with filtering
  - `GET /api/v1/cis/{id}` - Get specific CI
  - `PUT /api/v1/cis/{id}` - Update CI
  - `DELETE /api/v1/cis/{id}` - Delete CI

- **Search & Analytics**:
  - `GET /api/v1/cis/search?q=term` - Search CIs by text
  - `GET /api/v1/cis/count` - Get total CI count
  - `GET /api/v1/database/test` - Test database connectivity

- **System Endpoints**:
  - `GET /health` - Health check with DB status
  - `GET /docs` - Interactive API documentation

### Development Commands

| Command | Description |
|---------|-------------|
| `make dev` | Quick development setup (build + start) |
| `make build` | Build all Docker containers |
| `make up` | Start Neo4j and API services |
| `make down` | Stop all services |
| `make logs` | View all logs |
| `make shell-api` | Shell access to API container |
| `make clean` | Stop and clean up volumes |
| `make test` | Run API tests |
| `make status` | Show services status |

### Project Status

| Component | Status | Description |
|-----------|--------|-------------|
| 🗄️ **Data Models** | ✅ Complete | Pydantic models for CI, Human, Governance assets |
| 🐳 **Docker Infrastructure** | ✅ Complete | Neo4j + FastAPI + development environment |
| 🔌 **Neo4j Integration** | ✅ Complete | Database connection with pooling and lifecycle management |
| � **CRUD API** | ✅ Complete | Full Configuration Items endpoints with validation |
| 🔍 **Search & Filtering** | ✅ Complete | Text search and advanced filtering capabilities |
| 📈 **Impact Analysis** | 🚧 In Progress | Dependencies and impact query endpoints |
| 🎨 **Frontend** | 📋 Planned | Vue.js application with graph visualization |
| 🔒 **Authentication** | 📋 Planned | JWT-based RBAC system |

## 📊 Data Model

Constellation models your infrastructure as interconnected nodes:

- **Configuration Items (CIs)**: Hardware, Software, Services, Applications, Endpoints
- **Human Assets**: People, Teams, Roles, Skills
- **Governance**: Processes, Policies, Controls, Risks, Contracts
- **External**: Vendors, Partners
- **Digital**: Datasets, Identities, Credentials

## 🎯 Use Cases

- **Impact Analysis**: "If this server fails, what services are affected?"
- **Bus Factor Analysis**: "Which critical services depend on a single person?"
- **Compliance Tracking**: "Which assets are covered by our data protection policy?"
- **Change Management**: "What's the full dependency chain for this deployment?"
- **Risk Assessment**: "Where are our single points of failure?"

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](docs/) (Coming soon)
- [API Documentation](http://localhost:8000/docs) (When running)
- [Issues](https://github.com/loreleimouttez/Constellation/issues)

---

**Status**: 🚧 Early Development - Infrastructure Complete, API Development in Progress

### 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Format code
make format

# Lint code
make lint
```

### 🔧 Configuration

Key environment variables in `.env`:

```bash
# Database
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=constellation123

# API
PROJECT_NAME=Constellation
API_V1_STR=/api/v1
SECRET_KEY=your-secret-key-here

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```