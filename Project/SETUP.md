# Setup Guide for Background Job Scheduler

This guide will help you set up and run the Background Job Scheduler project.

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```cmd
   cd d:\Code\Python\py-scripts\Project
   ```

2. **Start with Docker Compose:**
   ```cmd
   docker-compose up -d
   ```

3. **Check logs:**
   ```cmd
   docker-compose logs -f scheduler
   ```

### Option 2: Local Development Setup

1. **Prerequisites:**
   - Python 3.13+
   - MySQL 8.0+
   - Git

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Set up database:**
   - Create MySQL database: `job_scheduler`
   - Copy `.env.example` to `.env` and configure database credentials

4. **Run migrations:**
   ```cmd
   python -m background_job_scheduler.cli migrate
   ```

5. **Start the scheduler:**
   ```cmd
   python run_scheduler.py
   ```

## Development Commands

### Using Make (if available):
```cmd
make help           # Show available commands
make install-dev    # Install development dependencies
make test           # Run tests
make lint          # Run code linting
make format        # Format code
make run           # Run the scheduler
```

### Manual Commands:
```cmd
# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/background_job_scheduler --cov-report=html

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Run the application
python run_scheduler.py

# Use CLI commands
python -m background_job_scheduler.cli --help
python -m background_job_scheduler.cli list-jobs
python -m background_job_scheduler.cli add-job "Test Job" "0 * * * *" example_job.py
```

## Project Structure

```
Project/
├── src/background_job_scheduler/    # Main application package
│   ├── domain/                      # Business logic
│   │   ├── entities/               # Domain entities (Job, JobExecution)
│   │   ├── interfaces/             # Repository and service interfaces
│   │   └── services/               # Domain services
│   ├── infrastructure/             # External integrations
│   │   ├── database/              # Database connections and migrations
│   │   └── repositories/          # Repository implementations
│   ├── config/                    # Configuration management
│   └── cli.py                     # Command-line interface
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── example_job.py                 # Example job implementation
├── run_scheduler.py               # Main application entry point
├── requirements.txt               # Dependencies
├── pyproject.toml                 # Project configuration
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── Makefile                       # Development commands
└── README.md                      # Project documentation
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=job_scheduler
DB_USER=scheduler
DB_PASSWORD=scheduler_pass

# Application Configuration
LOG_LEVEL=INFO
MAX_WORKERS=4
SCHEDULER_TIMEZONE=UTC
```

### Database Setup

1. **Create MySQL database:**
   ```sql
   CREATE DATABASE job_scheduler;
   CREATE USER 'scheduler'@'localhost' IDENTIFIED BY 'scheduler_pass';
   GRANT ALL PRIVILEGES ON job_scheduler.* TO 'scheduler'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Run migrations:**
   The migration script is located at `src/background_job_scheduler/infrastructure/database/migrations/001_initial_schema.sql`

## Usage Examples

### Adding a Job via CLI

```cmd
python -m background_job_scheduler.cli add-job "Daily Report" "0 9 * * *" example_job.py
```

### Creating Custom Jobs

Create a Python file with your job logic:

```python
# my_job.py
import time
from datetime import datetime

def execute_job() -> dict:
    """Your job implementation"""
    print(f"Executing job at {datetime.now()}")
    
    # Your business logic here
    time.sleep(2)
    
    return {"status": "completed", "message": "Job executed successfully"}

if __name__ == "__main__":
    result = execute_job()
    print(f"Result: {result}")
```

### Cron Expression Examples

- `"0 9 * * *"` - Daily at 9:00 AM
- `"0 */6 * * *"` - Every 6 hours
- `"0 9 * * 1-5"` - Weekdays at 9:00 AM
- `"0 0 1 * *"` - First day of every month at midnight

## Monitoring and Logs

### View Logs
- **Docker:** `docker-compose logs -f scheduler`
- **Local:** Check console output or configure file logging

### Check Job Status
```cmd
python -m background_job_scheduler.cli list-jobs
python -m background_job_scheduler.cli job-history <job_id>
```

## Architecture

This project follows Clean Architecture principles:

- **Domain Layer:** Contains business logic and rules
- **Application Layer:** Orchestrates use cases
- **Infrastructure Layer:** Handles external concerns (database, file system)
- **Configuration Layer:** Manages application settings

### SOLID Principles Applied:

- **Single Responsibility:** Each class has one reason to change
- **Open/Closed:** Extensible through interfaces
- **Liskov Substitution:** Implementations are substitutable
- **Interface Segregation:** Focused interfaces
- **Dependency Inversion:** Depends on abstractions, not concretions

## Troubleshooting

### Common Issues:

1. **Database Connection Errors:**
   - Verify MySQL is running
   - Check credentials in `.env` file
   - Ensure database exists

2. **Import Errors:**
   - Run `pip install -e .` to install package in development mode
   - Check Python path and virtual environment

3. **Permission Errors:**
   - Ensure job scripts are executable
   - Check file paths are accessible

4. **Port Conflicts:**
   - MySQL default port 3306
   - Change ports in `docker-compose.yml` if needed

### Getting Help:

1. Check logs for error messages
2. Verify configuration settings
3. Test database connectivity
4. Ensure all dependencies are installed

## Next Steps

1. **Add More Job Types:** Extend the system with different job types
2. **Web Interface:** Add a web dashboard for job management
3. **Notifications:** Implement email/Slack notifications for job failures
4. **Metrics:** Add monitoring and metrics collection
5. **Clustering:** Scale with multiple scheduler instances

Enjoy using the Background Job Scheduler! 🚀