# QRKot 🐱

QRKot is a REST API for a charity fund that collects donations for various projects.

The service allows administrators to create and manage charity projects, while registered users can make donations. Donations are automatically distributed among open projects in the order they were created.

## Features

- User registration and authentication
- Charity project management
- Creating donations
- Automatic distribution of donations among open projects
- Tracking invested and remaining amounts
- Automatic project closing when the required amount is reached
- Role-based access for users and superusers
- API documentation via Swagger and ReDoc

## How investment works

Donations are distributed among open charity projects using a FIFO approach.

When a new donation is created:

1. The oldest open charity project is selected.
2. The available donation amount is invested into the project.
3. If the project reaches its target amount, it is automatically closed.
4. Any remaining donation amount is transferred to the next open project.

The same logic is applied when a new charity project is created and there are uninvested donations available.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- FastAPI Users
- Uvicorn
- Pytest

## Project Structure

```text
app/
├── api/          # API endpoints and validators
├── core/         # Application configuration, database and authentication
├── crud/         # Database CRUD operations
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
├── services/     # Business logic
└── main.py       # Application entry point

alembic/          # Database migrations
tests/            # Automated tests
```

## Installation

Clone the repository:

```bash
git clone https://github.com/P-Kulakova/cat-charity-2.git
cd cat-charity-2
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

You can use `.env.example` as a template:

```env
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=your_secret_key
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=your_password
```

Do not commit your actual `.env` file to the repository.

## Database Migrations

Apply the migrations:

```bash
alembic upgrade head
```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## Testing

Run the automated tests with:

```bash
pytest
```

## API Overview

The API provides endpoints for:

- authentication and user management;
- creating, viewing, updating and deleting charity projects;
- creating donations;
- viewing donation history;
- automatic investment of available funds.

Some project management operations are available only to superusers.

## Author

**Polina Kulakova**

Python Backend Developer

GitHub: [P-Kulakova](https://github.com/P-Kulakova)
