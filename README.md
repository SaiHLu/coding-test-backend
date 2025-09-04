# Coding Test AI

A FastAPI application with AI capabilities, database integration, and waste/company management features.

## Features

- **FastAPI** web framework with async support
- **PostgreSQL** database with SQLModel ORM
- **Alembic** for database migrations
- **AI Integration** with LangChain and OpenAI
- **Company and Waste Management** APIs
- **Pytest** for testing

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for database)
- Git

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd coding-test-ai
```

### 2. Virtual Environment Setup

#### Option A: Using Python venv (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
which python
```

#### Option B: Using conda

```bash
# Create conda environment
conda create -n coding-test-ai python=3.11

# Activate environment
conda activate coding-test-ai
```

### 3. Install Dependencies

After activating your virtual environment:

```bash
# Install Python dependencies
make install

# Or manually:
pip install -r requirements.txt
```

### 4. Database Setup

Start the PostgreSQL database using Docker:

```bash
# Start the database
docker compose up -d

# Verify database is running
docker compose ps
```

### 5. Environment Variables

Create a `.env` file in the project root (if needed for API keys):

```bash
# Example .env file
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://postgres@localhost:5432/postgres
```

### 6. Database Migrations

Run database migrations to set up the schema:

```bash
# Run migrations to latest
make migration-up

# Or manually:
alembic upgrade head
```

## Running the Project

### Development Server

```bash
# Start the FastAPI development server
make start

# Or manually:
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health-check


## Available Commands

The project uses a Makefile for common tasks:

```bash
# Install dependencies
make install

# Start development server
make start

# Run tests
make test

# Create a new migration
make create-migration MSG="Your migration message"

# Run migrations
make migration-up

# Rollback migrations
make migration-down

# Rollback specific number of steps
make migration-down STEPS=2

# Migrate to specific revision
make migration-up TARGET=revision_id
```

## Testing

Run the test suite:

```bash
# Run all tests
make test

# Or manually:
pytest . -s -v

# Run specific test file
pytest src/ai/tests/test_llm.py -v
```

## API Endpoints

The application provides the following main endpoints:

- **Companies**: `/companies` - Company management APIs
- **Wastes**: `/wastes` - Waste management APIs  
- **AI**: `/ai` - AI-powered features
- **Health Check**: `/health-check` - Application health status

Visit http://localhost:8000/docs for interactive API documentation.

## Project Structure

```
coding-test-ai/
├── alembic/                 # Database migrations
├── src/
│   ├── ai/                  # AI-related functionality
│   ├── dto/                 # Data Transfer Objects
│   ├── models/              # Database models
│   ├── repositories/        # Data access layer
│   ├── routers/             # API endpoints
│   ├── utils/               # Utility functions
│   ├── database.py          # Database configuration
│   ├── dependencies.py      # FastAPI dependencies
│   └── main.py              # Application entry point
├── requirements.txt         # Python dependencies
├── Makefile                 # Common commands
├── docker-compose.yml       # Database setup
└── alembic.ini             # Alembic configuration
```

## Development Workflow

1. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Start database**:
   ```bash
   docker compose up -d
   ```

3. **Run migrations** (if needed):
   ```bash
   make migration-up
   ```

4. **Start development server**:
   ```bash
   make start
   ```

5. **Run tests** (in another terminal):
   ```bash
   make test
   ```

6. **Run streamlit** (to interact with ai)
   ```base
   make gui
   ```

## Troubleshooting

### Virtual Environment Issues

- **Environment not activating**: Ensure you're using the correct activation command for your shell
- **Command not found**: Make sure Python 3.11+ is installed and accessible
- **Permission errors**: Use `python3 -m venv venv` instead of `python -m venv venv`

### Database Issues

- **Connection refused**: Ensure Docker is running and PostgreSQL container is started
- **Migration errors**: Check database connection and ensure container is healthy

### Dependencies Issues

- **Install failures**: Upgrade pip with `pip install --upgrade pip`
- **Conflicting packages**: Consider creating a fresh virtual environment
