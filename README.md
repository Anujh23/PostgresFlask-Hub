---

# Flask Application with PostgreSQL

## Overview

This project consists of a Flask application that interacts with a PostgreSQL database. The application provides APIs to manage users, products, and orders. It is containerized using Docker for easy deployment.

## Project Structure

- `app.py`: Main Flask application with endpoints for managing users, products, and orders.
- `flask.dockerfile`: Dockerfile for building the Flask application image.
- `docker-compose.yml`: Docker Compose file for setting up Flask and PostgreSQL services.
- `requirements.txt`: Python dependencies for the Flask application.

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Build and Run the Docker Containers

Make sure Docker and Docker Compose are installed on your machine.

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers for both the Flask application and PostgreSQL database.

### 3. Access the Application

- **Flask Application**: Available at `http://localhost:4000`
- **PostgreSQL Database**: Accessible at `localhost:5432`

## API Endpoints

### User Routes

- **Create User**: `POST /api/flask/users`
- **Get All Users**: `GET /api/flask/users`
- **Get User by ID**: `GET /api/flask/users/<id>`
- **Update User**: `PUT /api/flask/users/<id>`
- **Delete User**: `DELETE /api/flask/users/<id>`

### Product Routes

- **Create Product**: `POST /api/flask/products`
- **Get All Products**: `GET /api/flask/products`
- **Get Product by ID**: `GET /api/flask/products/<id>`
- **Update Product**: `PUT /api/flask/products/<id>`
- **Delete Product**: `DELETE /api/flask/products/<id>`

### Order Routes

- **Create Order**: `POST /api/flask/orders`
- **Get All Orders**: `GET /api/flask/orders`
- **Get Order by ID**: `GET /api/flask/orders/<id>`
- **Update Order**: `PUT /api/flask/orders/<id>`
- **Delete Order**: `DELETE /api/flask/orders/<id>`

## Docker Configuration

### Flask Dockerfile

```Dockerfile
FROM python:3.10.0

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
```

### Docker Compose Configuration

```yaml
version: '3'

services:
  flaskapp:
    container_name: flaskapp
    image: flaskapp:1.0.0
    build:
      context: ./backend
      dockerfile: flask.dockerfile
    ports:
      - 4000:4000
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
    depends_on:
      - db

  db:
    container_name: db
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata: {}
```

## Docker Commands

- **Start Container Images**
  - For database: `docker start db`
  - For Flask app: `docker start flaskapp`

- **To Apply Changes in Container**
  ```bash
  docker-compose up --build
  ```

- **To Start All Containers at Once**
  ```bash
  docker-compose up -d
  ```

- **Check Status of Containers**
  ```bash
  docker-compose ps
  ```

- **To Stop Containers**
  - All containers: `docker-compose stop`
  - Individually:
    ```bash
    docker stop flaskapp
    docker stop db
    ```

- **To Check Database**
  ```bash
  docker exec -it db psql -U postgres
  ```

## Requirements

- Flask
- Flask-SQLAlchemy
- Flask-CORS
- psycopg2-binary

You can install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Notes

- Ensure PostgreSQL is running before starting the Flask application.
- The Flask app is configured to run in debug mode. Change `debug=True` to `debug=False` for production.
---
