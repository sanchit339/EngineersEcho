# EngineersEcho Blog Website

## Introduction
EngineersEcho is a full-stack blog platform built with Django, deployed using Docker with PostgreSQL, Nginx, and Gunicorn. Images are stored locally on the server (no cloud storage required).

## Tech Stack
- **Backend:** Django 4.2, Python 3.11
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** PostgreSQL 16
- **Web Server:** Nginx (reverse proxy) + Gunicorn (WSGI server)
- **Containerization:** Docker & Docker Compose
- **Email:** Gmail SMTP (for password reset)

## Features

### User Authentication
- Register, Login, Logout, and Profile Management
- Password reset via email
- Profile picture upload with image compression

### Blog
- Create, Read, Update, Delete blog posts
- Pagination for better navigation
- Post search by title

### Deployment
- Dockerized with 3 services: Django (Gunicorn), PostgreSQL, Nginx
- Local file storage for media uploads
- Static files served via WhiteNoise + Nginx
- Auto-run migrations on container startup

## Project Structure
```
EngineersEcho/
├── EngineersEcho/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── blog/                   # Blog app (posts, views, templates)
├── users/                  # Auth app (register, login, profiles)
├── media/                  # User uploads (profile pics)
├── staticfiles/            # Collected static files (generated)
├── Dockerfile              # Python app container
├── docker-compose.yml      # Multi-container orchestration
├── nginx.conf              # Nginx reverse proxy config
├── gunicorn.conf.py        # Gunicorn server config
├── entrypoint.sh           # Container startup script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Actual environment variables (not in git)
└── Notes/                  # Developer documentation
```

## Quick Start (Docker)

### 1. Clone the repository
```bash
git clone https://github.com/sanchit339/EngineersEcho.git
cd EngineersEcho
```

### 2. Create environment file
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 3. Build and run
```bash
docker compose up -d --build
```

The app will be available at `http://localhost` (or your server IP).

### 4. Create a superuser
```bash
docker compose exec web python manage.py createsuperuser
```

## Environment Variables (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | Debug mode | `False` for production |
| `ALLOWED_HOSTS` | Comma-separated domains | `34.14.195.121,localhost` |
| `POSTGRES_DB` | Database name | `engineersecho` |
| `POSTGRES_USER` | Database user | `engineersecho` |
| `POSTGRES_PASSWORD` | Database password | Use a strong password |
| `EMAIL_USER` | Gmail address | `your@gmail.com` |
| `EMAIL_PASS` | Gmail app password | Generate at myaccount.google.com |

## Docker Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `db` | postgres:16-alpine | 5432 | PostgreSQL database |
| `web` | Custom (Django) | 8000 | Gunicorn + Django app |
| `nginx` | nginx:alpine | 80 | Reverse proxy + static files |

## Useful Commands

```bash
# View logs
docker compose logs -f

# Restart services
docker compose restart

# Stop everything
docker compose down

# Rebuild after code changes
docker compose up -d --build

# Run Django management commands
docker compose exec web python manage.py <command>

# Access Django shell
docker compose exec web python manage.py shell

# Run migrations manually
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Backup database
docker compose exec db pg_dump -U engineersecho engineersecho > backup.sql

# Restore database
docker compose exec -T db psql -U engineersecho engineersecho < backup.sql
```

## Development (without Docker)

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL locally (or use SQLite)
Create a `.env` file with your local database settings, or the app will fall back to defaults.

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Run development server
```bash
python manage.py runserver
```

## Deployment Notes

- Media files (profile pictures) are stored in a Docker volume (`media_data`), persisted across container restarts
- Static files are collected at build time and served by Nginx
- PostgreSQL data is persisted in a Docker volume (`postgres_data`)
- The entrypoint script waits for PostgreSQL, runs migrations, and collects static files before starting Gunicorn

## References
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Nginx + Gunicorn + Django](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)
