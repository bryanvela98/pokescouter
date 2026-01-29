# PokeScouter

## Features

- Fetch Pokemon data from PokeAPI on-demand
- Store Pokemon information locally for fast access
- Retrieve Pokemon by ID, name, or list all
- Batch fetch multiple Pokemon in a single request
- Comprehensive Pokemon data including:
  - Basic information (name, height, weight)
  - Types (with primary/secondary slot)
  - Base stats (HP, Attack, Defense, etc.)
  - Abilities (normal and hidden)
  - Sprite images (default and shiny)
- Input validation and sanitization
- RESTful API design
- SQLite database with SQLAlchemy ORM
- Environment-based configuration

## Technology Stack

- **Python 3.x**
- **Flask 3.1.2** - Web framework
- **SQLAlchemy 2.0.46** - ORM for database operations
- **Flask-SQLAlchemy 3.1.1** - Flask integration for SQLAlchemy
- **Requests 2.32.5** - HTTP library for API calls
- **python-dotenv 1.2.1** - Environment variable management
- **SQLite** - Database

## Project Structure

```
PokeScouter/
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore rules
├── config/
│   ├── __init__.py
│   └── config.py          # Configuration management
├── models/
│   ├── __init__.py
│   ├── base_model.py      # Base model with CRUD operations
│   ├── pokemon.py         # Pokemon model
│   ├── pokemonType.py     # Pokemon Type model
│   ├── pokemonStat.py     # Pokemon Stats model
│   ├── pokemonAbility.py  # Pokemon Abilities model
│   └── pokemontypes.py    # Junction table for Pokemon-Type relationship
├── routes/
│   ├── __init__.py
│   └── pokemon_routes.py  # Pokemon API endpoints
├── services/
│   ├── __init__.py
│   ├── pokemon_service.py # Pokemon business logic
│   ├── pokeapi_service.py # PokeAPI client and data transformer
│   └── validators.py      # Input validation and sanitization
└── utils/
    ├── __init__.py
    └── db.py              # Database initialization

```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Steps

1. Clone the repository:

```bash
git clone https://github.com/bryanvela98/pokescouter.git
cd pokescouter
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```bash
touch .env
```

5. Configure environment variables (see [Configuration](#configuration))

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///poke_scouting.db

# PokeAPI Configuration
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
POKEAPI_TIMEOUT=10
```

### Configuration Variables

| Variable           | Description                             | Default                      | Required |
| ------------------ | --------------------------------------- | ---------------------------- | -------- |
| `SECRET_KEY`       | Flask secret key for session management | -                            | Yes      |
| `DATABASE_URL`     | Database connection string              | `sqlite:///poke_scouting.db` | Yes      |
| `POKEAPI_BASE_URL` | Base URL for PokeAPI                    | `https://pokeapi.co/api/v2`  | Yes      |
| `POKEAPI_TIMEOUT`  | API request timeout in seconds          | `10`                         | No       |

## Usage

### Starting the Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the application
python app.py
```

The server will start on `http://localhost:5050`

### Basic Workflow

1. **Check server health:**

```bash
curl http://localhost:5050/health
```

2. **Fetch a Pokemon from PokeAPI:**

```bash
curl -X POST http://localhost:5050/api/pokemon/fetch/pikachu
```

3. **Retrieve Pokemon from database:**

```bash
curl http://localhost:5050/api/pokemon/name/pikachu
```

4. **Fetch multiple Pokemon:**

```bash
curl -X POST http://localhost:5050/api/pokemon/fetch/batch \
  -H "Content-Type: application/json" \
  -d '{"pokemon": ["charizard", "bulbasaur", "squirtle"]}'
```

For detailed API documentation including request/response schemas and all parameters, see [API Resume](docs/API_Resume.md).

For detailed information about architecture decisions and implementation patterns, see [RelevantKnowledge](docs/RelevantKnowledgeAPPLIED.md).

##
