## HajjUmrahFlow — Starter Repo

This repository provides a production-ready structure for an **Integrated Web-Based System for Hajj and Umrah Trips Management**
 built with Django, Django REST Framework, PostgreSQL, Bootstrap/HTMX and n8n.

### Features
- Centralized booking and payment tracking
- Customer relationship management (CRM)
- Trip and package lifecycle management
- Role-based access (`manager`, `agent`, `accountant`)
- Token-authenticated REST API with OpenAPI documentation
- Webhook-first automation templates for n8n
- Seat availability enforcement and automatic booking status updates
- Trip manifest endpoint for exporting traveler lists

### Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Apps

`users` – custom user model with roles

`crm` – customers, documents, communication logs

`trips` – trip/package definitions

`bookings` – bookings and payments

### API

Versioned under `/api/v1/` with token authentication. OpenAPI schema is auto-generated via drf-spectacular at `/api/schema/` and `/api/docs/` (Swagger UI). A manifest of booked customers for any trip is available via `GET /api/v1/trips/<id>/manifest/`.

### Automation (n8n)

Webhook-first design. See `scripts/n8n/New_Booking_Onboarding.json` and `scripts/n8n/Reminder_Payment_Daily.json` for sample workflows. Configure your secrets in `.env`.

### Deploy

Docker and docker-compose files live in `infra/`. CI via GitHub Actions runs lint & tests and builds container images.