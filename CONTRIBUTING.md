# Contributing to Constellation

We love your input! We want to make contributing to Constellation as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This leads to **more readable messages** that are easy to follow when looking through the **project history**.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Scopes

Common scopes for this project:
- **api**: Backend API changes
- **ui**: Frontend UI changes
- **db**: Database related changes
- **auth**: Authentication and authorization
- **graph**: Graph visualization components
- **model**: Data models and schemas
- **config**: Configuration changes
- **docker**: Docker and infrastructure changes

### Examples

```bash
feat(api): add endpoint for CI impact analysis
fix(ui): resolve graph rendering issue with large datasets
docs(readme): update installation instructions
refactor(model): simplify relationship mapping logic
test(api): add unit tests for authentication service
```

## Code Style

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://github.com/PyCQA/isort) for import sorting
- Use type hints where applicable

### JavaScript/Vue.js (Frontend)
- Follow [Vue.js Style Guide](https://vuejs.org/style-guide/)
- Use [ESLint](https://eslint.org/) with Vue.js configuration
- Use [Prettier](https://prettier.io/) for code formatting

### General
- Write meaningful commit messages
- Keep functions small and focused
- Add comments for complex logic
- Write tests for new features

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/loreleimouttez/Constellation.git
   cd Constellation
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Backend development** (Optional, for API development)
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. **Frontend development** (Optional, for UI development)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/loreleimouttez/Constellation/issues).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We use GitHub issues to track feature requests. Request a feature by [opening a new issue](https://github.com/loreleimouttez/Constellation/issues) with the `enhancement` label.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Questions?

Feel free to contact the maintainers if you have any questions. We're here to help!

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

---

Thank you for contributing to Constellation! 🌟