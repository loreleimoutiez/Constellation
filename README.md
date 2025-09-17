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

*Coming soon - Development in progress*

```bash
# Clone the repository
git clone https://github.com/loreleimouttez/Constellation.git
cd Constellation

# Start with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Neo4j Browser: http://localhost:7474
```

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

**Status**: 🚧 Early Development - MVP in Progress