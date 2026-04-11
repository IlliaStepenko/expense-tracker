## Expense tracking

### 1. Clone the repository
```bash
git clone git@github.com:IlliaStepenko/expense-tracker.git
```

### 2. .env

```bash
cp .env.example .env
```

### 3. Run docker-compose
1. For local development
```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
```
2. For deployment on test server
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
### 4. Linting and Code Formatting
```bash
flake8 backend

isort --check-only --diff backend

black --check backend
```