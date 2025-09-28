# Background Job Scheduler

A modern Python 3.13 background job scheduler with MySQL database integration, cron expression support, and clean architecture following SOLID principles.

## Features

- 🕒 **Cron Expression Support**: Schedule jobs using familiar cron syntax
- 🗄️ **MySQL Integration**: Persistent job storage and execution tracking
- 🏗️ **Clean Architecture**: Follows SOLID principles with dependency injection
- 📊 **Job Monitoring**: Track job execution history and status
- 🔧 **Configuration Management**: Environment-based configuration
- 📝 **Comprehensive Logging**: Structured logging with rich output
- 🧪 **Test Coverage**: Unit tests with pytest framework

## Project Structure

```
Project/
├── src/
│   └── background_job_scheduler/
│       ├── __init__.py
│       ├── cli.py                    # Command-line interface
│       ├── config/                   # Configuration layer
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── database.py
│       ├── domain/                   # Domain layer (business logic)
│       │   ├── __init__.py
│       │   ├── entities/
│       │   │   ├── __init__.py
│       │   │   ├── job.py
│       │   │   └── execution.py
│       │   ├── interfaces/
│       │   │   ├── __init__.py
│       │   │   ├── job_repository.py
│       │   │   ├── scheduler.py
│       │   │   └── executor.py
│       │   └── services/
│       │       ├── __init__.py
│       │       ├── job_service.py
│       │       └── scheduler_service.py
│       ├── infrastructure/            # Infrastructure layer
│       │   ├── __init__.py
│       │   ├── database/
│       │   │   ├── __init__.py
│       │   │   ├── connection.py
│       │   │   ├── repositories/
│       │   │   │   ├── __init__.py
│       │   │   │   └── mysql_job_repository.py
│       │   │   └── migrations/
│       │   │       ├── __init__.py
│       │   │       └── 001_initial_schema.sql
│       │   ├── scheduler/
│       │   │   ├── __init__.py
│       │   │   ├── cron_scheduler.py
│       │   │   └── job_executor.py
│       │   └── logging/
│       │       ├── __init__.py
│       │       └── setup.py
│       └── application/               # Application layer
│           ├── __init__.py
│           ├── use_cases/
│           │   ├── __init__.py
│           │   ├── create_job.py
│           │   ├── schedule_job.py
│           │   └── execute_job.py
│           └── dto/
│               ├── __init__.py
│               └── job_dto.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_job_service.py
│   │   └── test_scheduler.py
│   └── integration/
│       ├── __init__.py
│       └── test_database.py
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml
```

## Quick Start

### Prerequisites

- Python 3.13+
- MySQL 8.0+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your MySQL credentials
   ```

5. **Run database migrations**:
   ```bash
   job-scheduler migrate
   ```

### Usage

#### Start the scheduler daemon
```bash
job-scheduler start
```

#### Create a new job
```bash
job-scheduler create-job \
  --name "Daily Backup" \
  --cron "0 2 * * *" \
  --command "python backup_script.py" \
  --description "Daily database backup"
```

#### List all jobs
```bash
job-scheduler list-jobs
```

#### View job execution history
```bash
job-scheduler job-history --job-id 1
```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and adjust the values:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=job_scheduler
DB_USER=your_username
DB_PASSWORD=your_password

# Application Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_JOBS=5
JOB_TIMEOUT=300
```

## Architecture

This project follows Clean Architecture principles with clear separation of concerns:

- **Domain Layer**: Contains business entities and interfaces (SOLID - D: Dependency Inversion)
- **Application Layer**: Use cases and application-specific logic
- **Infrastructure Layer**: External concerns (database, scheduler, logging)
- **Configuration Layer**: Application settings and dependency injection

### SOLID Principles Applied

- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Extensible through interfaces without modifying existing code
- **L**iskov Substitution: Implementations can be substituted without breaking functionality
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: High-level modules don't depend on low-level modules

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/ tests/
isort src/ tests/
```

### Type Checking
```bash
mypy src/
```

### Linting
```bash
ruff check src/ tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.