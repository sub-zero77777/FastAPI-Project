# Service Request Management API

A secure and scalable Service Request Management API built with FastAPI and Supabase. The application provides user authentication, service request management, and dashboard analytics through RESTful APIs. It follows a clean, modular architecture to ensure maintainability, scalability, and ease of development.

## Features

- User Registration and Authentication
- JWT-Based Authorization
- Secure Password Hashing with Bcrypt
- Create, Read, Update, and Manage Service Requests
- Dashboard Analytics and Reporting
- Data Validation with Pydantic
- Supabase Database Integration
- Environment-Based Configuration
- Modular and Scalable Project Structure

## Tech Stack

- **Backend:** FastAPI
- **Database:** Supabase
- **Authentication:** JWT (JSON Web Tokens)
- **Password Security:** Passlib & Bcrypt
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Configuration:** Python Dotenv

## Project Structure

```text
app/
├── core/
│   ├── config.py
│   ├── security.py
│   └── supabase_client.py
├── routers/
│   ├── auth.py
│   ├── service_requests.py
│   └── dashboard.py
├── schemas/
│   ├── auth.py
│   └── service_request.py
├── services/
│   ├── auth_service.py
│   └── service_request_service.py
├── utils/
│   └── enums.py
└── main.py

requirements.txt
README.md
