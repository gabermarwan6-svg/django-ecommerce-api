# Django E-Commerce REST API

A portfolio-ready backend API built with Python, Django, Django REST Framework, and JWT authentication.

## Features

- JWT authentication (access + refresh tokens)
- User registration
- Product and category management
- Search-ready product API
- User-specific shopping cart
- Stock validation
- Checkout flow
- Order history
- Django admin panel
- Automated API tests
- SQLite for simple local development

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite

## Project Structure

```text
config/             # Django project configuration
store/              # E-commerce application
  models.py         # Database models
  serializers.py    # API serialization and validation
  views.py          # API endpoints
  permissions.py    # Custom permissions
  urls.py           # API routes
  tests.py          # API tests
manage.py
requirements.txt
```

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd django-ecommerce-api
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and change the secret key for a real deployment.

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## Main Endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register/` | No | Register a user |
| POST | `/api/token/` | No | Get JWT tokens |
| POST | `/api/token/refresh/` | No | Refresh access token |
| GET | `/api/categories/` | No | List categories |
| GET | `/api/products/` | No | List products |
| POST | `/api/products/` | Admin | Create product |
| GET | `/api/cart/` | Yes | View current cart |
| POST | `/api/cart/` | Yes | Add product to cart |
| GET | `/api/cart/summary/` | Yes | Cart total and item count |
| GET | `/api/orders/` | Yes | View own orders |
| POST | `/api/orders/checkout/` | Yes | Create order from cart |

## Example Authentication

Get tokens with:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Then send the access token on protected endpoints:

```text
Authorization: Bearer <access_token>
```

## Notes

This project is designed as a learning and portfolio project. Before production use, add PostgreSQL, proper secret management, CORS configuration, rate limiting, API documentation, logging, and a deployment setup.
