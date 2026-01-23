# Python Todo API with Keploy Mocking

A Flask-based Todo REST API with MySQL database integration, comprehensive pytest tests, and Keploy mocking for database calls.

## Features

- ✅ RESTful API with Flask
- ✅ MySQL database integration
- ✅ Full CRUD operations for todos
- ✅ Comprehensive pytest test suite
- ✅ Keploy integration for mocking database calls
- ✅ Docker Compose for easy MySQL setup

## Project Structure

```
python-todo-app/
├── app.py              # Flask application with API routes
├── models.py           # Todo data model
├── database.py         # MySQL database connection
├── repository.py       # Todo repository (CRUD operations)
├── test_app.py         # Pytest test suite
├── conftest.py         # Pytest configuration
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # MySQL Docker setup
├── .env               # Environment variables
└── README.md          # This file
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for MySQL)
- Keploy CLI (for mocking)

## Installation

### 1. Install Python Dependencies

```bash
cd python-todo-app
pip install -r requirements.txt
```

### 2. Start MySQL Database

```bash
docker-compose up -d
```

Wait for MySQL to be ready (about 10-20 seconds).

### 3. Install Keploy

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://get.keploy.io" -OutFile "install.ps1"; .\install.ps1
```

**macOS/Linux:**
```bash
curl -sSL https://get.keploy.io | bash
```

## Usage

### Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### Health Check
```bash
curl.exe http://localhost:5000/health
```

#### Create Todo
```bash
curl.exe http://localhost:5000/todos
Content-Type: application/json

{
  "title": "My Todo",
  "description": "Todo description",
  "completed": false
}
```

#### Get All Todos
```bash
GET /todos
```

#### Get Todo by ID
```bash
GET /todos/{id}
```

#### Update Todo
```bash
PUT /todos/{id}
Content-Type: application/json

{
  "title": "Updated Todo",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Todo
```bash
DELETE /todos/{id}
```

## Testing

### Running Tests WITHOUT Keploy (Real Database)

```bash
python -m pytest test_app.py -v
```

### Using Keploy to Record Database Calls

First, record the database interactions:

```bash
keploy mock-record -c "python -m pytest test_app.py -v" --path ./keploy
```

This will:
1. Run your tests
2. Record all MySQL database calls
3. Save them as mocks in the `./keploy` folder

### Using Keploy to Replay Mocks (No Real Database Needed)

Once mocks are recorded, you can run tests without a real database:

```bash
keploy mock-test -c "python -m pytest test_app.py -v" --path ./keploy
```

This will:
1. Run your tests
2. Intercept MySQL database calls
3. Return recorded responses instead of hitting the real database

### List Available Mock Sets

```bash
keploy list-mocks --path ./keploy
```

### Use Specific Mock Set

```bash
keploy mock-test -c "python -m pytest test_app.py -v" --mockName "mock-1234567890" --path ./keploy
```

## Benefits of Using Keploy

1. **No Database Required**: Run tests without MySQL running
2. **Faster Tests**: Mocked responses are instant
3. **Consistent Results**: Same responses every time
4. **Isolation**: Tests don't affect your database
5. **CI/CD Friendly**: No need to spin up databases in CI pipelines

## Environment Variables

Edit `.env` file to configure database connection:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=todo_db
```

## Development Workflow

### 1. Development with Real Database
```bash
# Start MySQL
docker-compose up -d

# Run app
python app.py

# Test with real database
python -m pytest test_app.py -v
```

### 2. Record Mocks for CI/CD
```bash
# Record all database interactions
keploy mock-record -c "python -m pytest test_app.py -v" --path ./keploy
```

### 3. Fast Testing with Mocks
```bash
# No database needed!
keploy mock-test -c "python -m pytest test_app.py -v" --path ./keploy
```

## Test Coverage

The test suite includes:

- ✅ Health check endpoint
- ✅ Create todo (success and validation)
- ✅ Get all todos
- ✅ Get todo by ID (success and not found)
- ✅ Update todo (success and not found)
- ✅ Delete todo (success and not found)
- ✅ Model serialization/deserialization

## Troubleshooting

### Database Connection Issues

If you get connection errors, ensure:
1. MySQL container is running: `docker ps`
2. MySQL is healthy: `docker-compose ps`
3. Environment variables are correct in `.env`

### Keploy Issues

If Keploy doesn't work:
1. Check Keploy is installed: `keploy --version`
2. Ensure you're in the correct directory
3. Make sure the application runs normally first

### Windows-Specific Issues

On Windows, you may need to:
1. Run PowerShell as Administrator for Docker commands
2. Enable WSL2 for Docker Desktop
3. Check Windows Defender isn't blocking Keploy

## Example Test Run

```bash
# Record mocks
$ keploy mock-record -c "pytest test_app.py -v" --path ./keploy
Recording outgoing calls...
test_app.py::TestHealthEndpoint::test_health_check PASSED
test_app.py::TestTodoEndpoints::test_create_todo PASSED
test_app.py::TestTodoEndpoints::test_get_all_todos PASSED
...
Mocks recorded successfully!

# Run with mocks (no database needed)
$ keploy mock-test -c "pytest test_app.py -v" --path ./keploy
Replaying mocks...
test_app.py::TestHealthEndpoint::test_health_check PASSED
test_app.py::TestTodoEndpoints::test_create_todo PASSED
test_app.py::TestTodoEndpoints::test_get_all_todos PASSED
...
All tests passed with mocks!
```

## License

MIT License
