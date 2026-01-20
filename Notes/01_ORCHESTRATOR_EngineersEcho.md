# 01: The Orchestrator - EngineersEcho (Main Project)

## what is the orchestrator?

the **EngineersEcho** directory is NOT an app - it's the **main Django project**.  
it's the container that holds all your apps together and manages global settings.

think of it as the **application.properties + main class** in Spring Boot.

---

## directory structure

```
EngineersEcho/          # the project root (orchestrator)
├── __init__.py         # makes this a Python package
├── settings.py         # GLOBAL configuration
├── urls.py             # MAIN URL router (entry point)
├── wsgi.py             # production server interface
└── asgi.py             # async server interface
```

---

## file-by-file breakdown

### 1. `__init__.py`

**what it is:**
- empty file (usually)
- makes the directory a Python package
- allows imports like `from EngineersEcho import settings`

**why it exists:**
- Python requirement for package imports
- without it, Python won't recognize this as a module

**other things you can do:**
```python
# can add package-level initialization
from .celery import app as celery_app
__all__ = ('celery_app',)

# or version info
__version__ = '1.0.0'
```

**in similar apps:**
- usually left empty
- only add stuff if you need package-level initialization
- common use: Celery configuration for async tasks

---

### 2. `settings.py` - THE BRAIN

**what it is:**
- **global configuration file** for the entire project
- every Django setting lives here
- equivalent to `application.properties` in Spring Boot

**current settings explained:**

#### a) SECRET_KEY
```python
SECRET_KEY = 'django-insecure-w4umm)1e=jf5j&8f&hc@sjv&=2r68&ij992b*tp=c_4sn$1k^r'
```
- **what:** cryptographic key for security features
- **why:** signs sessions, CSRF tokens, password resets
- **issue:** yours is hardcoded (bad for production)
- **better approach:**
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-for-dev')
```

#### b) DEBUG
```python
DEBUG = True
```
- **what:** enables detailed error pages
- **why:** useful for development
- **issue:** shows sensitive info in production
- **production:**
```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

#### c) ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['*']
```
- **what:** which domains can access your app
- **why:** security - prevents host header attacks
- **issue:** `['*']` allows anyone (bad for production)
- **production:**
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

#### d) INSTALLED_APPS
```python
INSTALLED_APPS = [
    'django.contrib.admin',        # admin panel
    'django.contrib.auth',         # authentication
    'django.contrib.contenttypes', # content type framework
    'django.contrib.sessions',     # session framework
    'django.contrib.messages',     # messaging framework
    'django.contrib.staticfiles',  # static files (CSS/JS)
    
    # your apps
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    
    # third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
]
```
- **what:** list of all Django apps/plugins to use
- **why:** Django needs to know what's included
- **order matters:** Django loads them in order
- **adding new apps:** append to this list + run migrations

**other apps you might add:**
```python
'rest_framework',           # for APIs
'corsheaders',              # CORS for frontend
'django_filters',           # filtering querysets
'django_extensions',        # dev utilities
'debug_toolbar',            # debugging in dev
'channels',                 # WebSockets
'celery',                   # async tasks
```

#### e) MIDDLEWARE
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
```
- **what:** request/response processors (like Spring interceptors)
- **why:** each one modifies requests/responses
- **execution:** runs top-to-bottom for requests, bottom-to-top for responses

**middleware breakdown:**
- `SecurityMiddleware` - security enhancements
- `SessionMiddleware` - handles sessions
- `CsrfViewMiddleware` - prevents CSRF attacks
- `AuthenticationMiddleware` - adds `request.user`
- `WhiteNoiseMiddleware` - serves static files in production

**custom middleware example:**
```python
# in middleware.py
class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        response['X-Custom-Header'] = 'value'
        return response

# in settings.py
MIDDLEWARE = [
    # ...
    'yourapp.middleware.CustomHeaderMiddleware',
]
```

#### f) DATABASES
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
- **what:** database configuration
- **why:** Django ORM needs to know where to store data

**PostgreSQL example:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'engineersecho_db',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**MySQL example:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'engineersecho',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**multiple databases:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'main_db',
    },
    'analytics': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics_db',
    }
}
```

#### g) STATIC FILES
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
- **STATIC_URL:** URL prefix for static files (CSS/JS)
- **STATIC_ROOT:** where `collectstatic` puts files for production
- **MEDIA_URL:** URL prefix for user uploads
- **MEDIA_ROOT:** where user uploads are stored

**production with S3:**
```python
# already in your settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = "engineersecho"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

#### h) EMAIL
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
```

**other email backends:**
```python
# development - prints to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# production - SendGrid
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# production - AWS SES
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
```

#### i) authentication
```python
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'
```
- **LOGIN_REDIRECT_URL:** where to go after login
- **LOGIN_URL:** where to redirect if login required

**other auth settings:**
```python
# session expiry
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# password validators (already in your settings)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# custom user model (for advanced apps)
AUTH_USER_MODEL = 'users.CustomUser'
```

---

### 3. `urls.py` - THE ROUTER

**what it is:**
- **main URL dispatcher** (entry point for all requests)
- delegates to app-specific URL configs
- like Spring Boot's `@RequestMapping` at the application level

**current configuration:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),           # root → blog app
    path('users/', include('users.urls')),    # /users/* → users app
    path('admin/', admin.site.urls),          # /admin → Django admin
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**how it works:**
1. request comes in: `http://localhost:8000/users/profile/`
2. Django checks `EngineersEcho/urls.py`
3. matches `users/` → delegates to `users.urls`
4. `users/urls.py` matches `profile/` → calls `views.profile()`

**other URL patterns:**

```python
# direct view (no app delegation)
from blog import views
urlpatterns = [
    path('', views.home, name='home'),
]

# API endpoints (with Django REST Framework)
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

# versioned API
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
]

# internationalization
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]
```

**advanced routing:**
```python
# regex patterns (old style)
from django.urls import re_path
urlpatterns = [
    re_path(r'^post/(?P<slug>[\w-]+)/$', views.post_detail),
]

# path converters
urlpatterns = [
    path('post/<int:pk>/', views.post_detail),      # integers only
    path('post/<slug:slug>/', views.post_detail),   # slugs only
    path('post/<uuid:id>/', views.post_detail),     # UUID only
]

# custom path converter
from django.urls.converters import register_converter

class YearConverter:
    regex = '[0-9]{4}'
    def to_python(self, value):
        return int(value)
    def to_url(self, value):
        return str(value)

register_converter(YearConverter, 'yyyy')

urlpatterns = [
    path('archive/<yyyy:year>/', views.archive),
]
```

---

### 4. `wsgi.py` - PRODUCTION INTERFACE

**what it is:**
- **WSGI** = Web Server Gateway Interface
- interface for production servers (Gunicorn, uWSGI)
- handles synchronous requests

**current code:**
```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EngineersEcho.settings')
application = get_wsgi_application()
```

**when it's used:**
- running with Gunicorn: `gunicorn EngineersEcho.wsgi:application`
- running with uWSGI: `uwsgi --module=EngineersEcho.wsgi:application`

**rarely need to modify** unless you're doing advanced deployment stuff

---

### 5. `asgi.py` - ASYNC INTERFACE

**what it is:**
- **ASGI** = Asynchronous Server Gateway Interface
- for async features (WebSockets, long-polling, HTTP/2)
- newer than WSGI

**current code:**
```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EngineersEcho.settings')
application = get_asgi_application()
```

**when you'd use it:**
```python
# with Django Channels (WebSockets)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

**deployment:**
```bash
# with Daphne (ASGI server)
daphne EngineersEcho.asgi:application
```

---

## what else can go in the orchestrator?

### celery.py (async tasks)
```python
# EngineersEcho/celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EngineersEcho.settings')
app = Celery('EngineersEcho')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### custom settings modules
```
EngineersEcho/
├── settings/
│   ├── __init__.py
│   ├── base.py        # common settings
│   ├── dev.py         # development
│   ├── prod.py        # production
│   └── test.py        # testing
```

```python
# settings/dev.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### middleware.py (custom middleware)
```python
# EngineersEcho/middleware.py
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        return response
```

---

## orchestrator best practices

1. **keep settings organized**
   - use environment variables for secrets
   - separate dev/prod configs
   
2. **minimal urls.py**
   - delegate to apps, don't define views here
   
3. **don't put business logic here**
   - this is for config only
   - views/models belong in apps
   
4. **use .env for secrets**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

5. **structure for scalability**
   ```
   EngineersEcho/
   ├── settings/
   │   ├── base.py
   │   ├── dev.py
   │   └── prod.py
   ├── urls.py
   ├── wsgi.py
   └── asgi.py
   ```

---

## common settings you might add

```python
# CORS for frontend apps
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
]

# REST Framework (for APIs)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# logging
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}

# internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True
```

---

## summary

**the orchestrator is:**
- global configuration hub
- main URL entry point
- production server interface
- does NOT contain business logic
- delegates to apps for actual functionality

**key files:**
- `settings.py` - the brain (all config)
- `urls.py` - the router (delegates to apps)
- `wsgi.py` / `asgi.py` - production interfaces

**think of it as:** the `application.properties` + main class in Spring Boot, but more powerful
