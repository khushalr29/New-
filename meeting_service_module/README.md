# Meeting Management Service

A professional, multi-tenant microservice for managing corporate meetings, halls, and action items.

## Architecture

This service is part of a modular ERP system. It leverages a centralized `shared` package for core data models, ensuring consistent logic across the entire ecosystem while maintaining high isolation between client companies.

### Key Features

- **Multi-Tenant Isolation:** All data access is strictly gated by the user's company affiliation.
- **Granular Control:** Built using Django REST Framework's `APIView` for precise request handling and method override.
- **Auto-Documentation:** Live OpenAPI 3.0 documentation available via Swagger/Redoc.
- **Audit Logging:** Server-side logging for critical state changes (Create/Update/Delete).

## Setup & Running

This project requires connectivity to the `shared` module and a valid PostgreSQL instance.

### Prerequisites

1. Active virtual environment.
2. `shared` package installed in editable mode (`pip install -e /path/to/shared`).
3. Correct environment variables in `.env`.

### Commands

```bash
# Apply remaining migrations
python manage.py migrate

# Start the service
python manage.py runserver 0.0.0.0:8000
```

## API Documentation

Access the following routes in your browser after starting the server:

- **Swagger UI:** `/swagger/`
- **ReDoc:** `/redoc/`

---
*Maintained by Engineering Team*
