# Contributing to MedAI

Thank you for your interest in contributing to MedAI! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Documentation](#documentation)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git
- API access to Hugging Face or RunPod

### Local Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd medai

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r api/requirements.txt

# Set up environment
cp infra/.env.example infra/.env
# Edit .env with your API keys

# Run the application
cd api && python main.py
```

### Docker Development
```bash
# Build and run with Docker
cd infra
docker compose up --build

# Access at http://localhost:8080
```

## Development Workflow

### 1. Choose an Issue
- Check the [Issues](../../issues) page for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
# Create and switch to a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-number-description
```

### 3. Make Changes
- Write clear, focused commits
- Test your changes thoroughly
- Update documentation as needed
- Follow the code style guidelines

### 4. Test Your Changes
```bash
# Run health check
curl http://localhost:8000/healthz

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Test message"}]}'
```

### 5. Submit a Pull Request
- Push your branch to GitHub
- Create a Pull Request with a clear description
- Reference any related issues
- Wait for review and address feedback

## Code Style

### Python Style
- Follow [PEP 8](https://pep8.org/) guidelines
- Use type hints for all function parameters and return values
- Write descriptive variable and function names
- Keep functions under 50 lines when possible
- Use docstrings for all public functions

### Example Code Style
```python
from typing import List, Dict, Optional
from fastapi import HTTPException

async def process_chat_request(
    messages: List[Dict[str, str]],
    provider: str,
    api_key: str
) -> Dict[str, str]:
    """
    Process a chat request through the specified LLM provider.

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        provider: The LLM provider to use ('HF_TGI' or 'RUNPOD_OPENAI')
        api_key: API key for the provider

    Returns:
        Dictionary containing the response

    Raises:
        HTTPException: If the request fails
    """
    if not messages:
        raise HTTPException(400, "Messages are required")

    # Implementation here
    pass
```

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

**Examples:**
```
feat: add provider switching capability
fix: handle API timeout errors gracefully
docs: update API endpoint documentation
refactor: simplify CORS middleware setup
```

## Testing

### Current Testing Status
The project currently has minimal automated testing. Future contributions should include:

### Unit Tests (Future Implementation)
```python
# tests/test_api.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/healthz")
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert "provider" in data
```

### Manual Testing Checklist
- [ ] Health endpoint returns correct status
- [ ] Chat endpoint accepts valid requests
- [ ] Error handling for invalid requests
- [ ] CORS headers are properly set
- [ ] Both HF_TGI and RunPod providers work
- [ ] Docker build completes successfully

## Submitting Changes

### Pull Request Process
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Update** documentation
6. **Commit** with clear messages
7. **Push** to your fork
8. **Create** a Pull Request

### Pull Request Template
```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please specify)

## Testing
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Commit messages are clear
- [ ] Documentation is updated
- [ ] No breaking changes
```

### Review Process
- At least one maintainer must review the PR
- All CI checks must pass
- Reviewers may request changes
- Once approved, a maintainer will merge the PR

## Documentation

### Updating Documentation
- Keep README.md current with new features
- Update API.md for endpoint changes
- Update CONFIG.md for configuration changes
- Add entries to JOURNAL.md for significant changes

### Documentation Standards
- Use clear, concise language
- Include code examples where helpful
- Keep screenshots updated
- Test all instructions on a clean environment

## Areas for Contribution

### High Priority
- [ ] Add comprehensive test suite
- [ ] Implement rate limiting
- [ ] Add request/response logging
- [ ] Improve error messages
- [ ] Add API documentation generation

### Medium Priority
- [ ] Add user session management
- [ ] Implement response caching
- [ ] Add metrics and monitoring
- [ ] Create admin interface
- [ ] Add support for more LLM providers

### Low Priority
- [ ] Add WebSocket support
- [ ] Create mobile app
- [ ] Add voice input/output
- [ ] Implement conversation history
- [ ] Add multi-language support

## Getting Help

### Communication Channels
- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Asking for Help
When asking for help:
- Provide clear description of the issue
- Include error messages and stack traces
- Describe steps to reproduce
- Mention your environment (OS, Python version, etc.)

## Recognition

Contributors will be recognized in:
- The repository's contributor list
- Release notes for significant contributions
- Special mentions in documentation updates

Thank you for contributing to MedAI! 🎉

## Keywords <!-- #keywords -->
- contributing
- development
- guidelines
- pull request
- testing
- code style
- documentation