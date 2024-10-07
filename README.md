# Superheroes API

## Overview
This is a simple Flask API that manages superheroes, their powers, and their strengths.

## Features
- Retrieve all heroes and their details.
- Retrieve all powers and their descriptions.
- Add a new hero's power and update powers.

## Technologies Used
- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite (for the database)
  
## Installation and Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/superheroes-api.git
    cd superheroes-api
    ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
5. Run the app:
    ```bash
    flask run
    ```

## API Endpoints
### Get All Heroes
- **Endpoint**: `/heroes`
- **Method**: `GET`

### Get Single Hero
- **Endpoint**: `/heroes/<id>`
- **Method**: `GET`

### Add Hero Power
- **Endpoint**: `/hero_powers`
- **Method**: `POST`
- **Body** (JSON):
  ```json
  {
      "strength": "Strong",
      "hero_id": 1,
      "power_id": 3
  }
