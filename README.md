# EMBASA - Engine Multi-domain for Business and Scientific Analysis

## Overview
EMBASA is an AI orchestration system specialized in multi-domain content analysis and validation.

## Setup
1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configurations
```

## Development
- Follow git workflow in docs/Padrões/boas praticas git.md
- Run tests: `pytest`
- Format code: `black .` and `isort .`

## License
Proprietary software. All rights reserved.
