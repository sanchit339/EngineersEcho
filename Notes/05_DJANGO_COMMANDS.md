# 05: Django Commands - Building This Project From Scratch

## project creation timeline (step-by-step)

this is exactly how you would recreate EngineersEcho from nothing.

---

## phase 1: initial setup

### step 1: create project directory
```bash
# create a directory for your project
mkdir EngineersEcho
cd EngineersEcho
```

### step 2: set up virtual environment
```bash
# create virtual environment
python -m venv venv

# activate it
# on macOS/Linux:
source venv/bin/activate

# on Windows:
venv\Scripts\activate

# you should see (venv) in your terminal now
```

**why virtual environment?**
- isolates project dependencies
- different projects can use different versions
- doesn't pollute global Python installation

### step 3: install Django
```bash
# install Django
pip install django

# check version
django-admin --version
# should show something like: 4.2.8
```

### step 4: create Django project (the orchestrator)
```bash
# django-admin startproject <project_name> .
# the . means create in current directory
django-admin startproject EngineersEcho .

# this creates:
# EngineersEcho/
# ├── EngineersEcho/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── asgi.py
# │   └── wsgi.py
# └── manage.py
```

**at this point you have:**
- the orchestrator (EngineersEcho/)
- manage.py (your command-line tool)

---

## phase 2: create apps

### step 5: create blog app
```bash
# python manage.py startapp <app_name>
python manage.py startapp blog

# this creates:
# blog/
# ├── __init__.py
# ├── admin.py
# ├── apps.py
# ├── models.py
# ├── tests.py
# └── views.py
```

### step 6: create users app
```bash
python manage.py startapp users

# creates users/ directory with same structure
```

### step 7: register apps in settings.py
```bash
# edit EngineersEcho/settings.py
# add to INSTALLED_APPS:
INSTALLED_APPS = [
    # ...
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
]
```

---

## phase 3: database setup

### step 8: create models
```bash
# edit blog/models.py
# add Post model

# edit users/models.py
# add Profile model
```

### step 9: make migrations (prepare database changes)
```bash
# create migration files
python manage.py makemigrations

# output:
# Migrations for 'blog':
#   blog/migrations/0001_initial.py
#     - Create model Post
# Migrations for 'users':
#   users/migrations/0001_initial.py
#     - Create model Profile
```

**what this does:**
- analyzes your models
- creates migration files (blueprints for database changes)
- doesn't actually change the database yet

**other makemigrations options:**
```bash
# make migrations for specific app
python manage.py makemigrations blog

# see what SQL will be executed
python manage.py sqlmigrate blog 0001

# dry run (show what would be created)
python manage.py makemigrations --dry-run

# name your migration
python manage.py makemigrations --name add_slug_to_post
```

### step 10: run migrations (apply to database)
```bash
# apply all migrations
python manage.py migrate

# output:
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying blog.0001_initial... OK
#   Applying users.0001_initial... OK
#   ...
```

**what this does:**
- executes migration files
- creates/modifies database tables
- tracks which migrations have been applied

**other migrate options:**
```bash
# migrate specific app
python manage.py migrate blog

# migrate to specific migration
python manage.py migrate blog 0001

# show migration status
python manage.py showmigrations

# rollback to previous migration
python manage.py migrate blog 0001  # if you're at 0002

# fake a migration (mark as applied without running)
python manage.py migrate --fake blog 0001
```

**migration commands cheat sheet:**
```bash
# see all migrations
python manage.py showmigrations

# check for model changes without creating migrations
python manage.py makemigrations --check

# squash multiple migrations into one (clean up)
python manage.py squashmigrations blog 0001 0005
```

---

## phase 4: create superuser (admin access)

### step 11: create admin account
```bash
python manage.py createsuperuser

# prompts:
# Username: admin
# Email: admin@example.com
# Password: ********
# Password (again): ********
# Superuser created successfully.
```

**what you can do now:**
- access `/admin/` panel
- manage users, posts, profiles
- CRUD operations through UI

---

## phase 5: running the development server

### step 12: run server
```bash
# default (localhost:8000)
python manage.py runserver

# custom port
python manage.py runserver 8080

# custom host and port
python manage.py runserver 0.0.0.0:8000

# output:
# Watching for file changes with StatReloader
# Performing system checks...
# System check identified no issues (0 silenced).
# Django version 4.2.8, using settings 'EngineersEcho.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

**what this does:**
- starts development server
- auto-reloads on code changes
- NOT for production (use Gunicorn/uWSGI)

---

## phase 6: install dependencies

### step 13: install required packages
```bash
# for this project, you need:

# image handling
pip install Pillow

# AWS S3 storage
pip install boto3 django-storages

# forms styling
pip install django-crispy-forms crispy-bootstrap5

# environment variables
pip install python-dotenv

# production server
pip install gunicorn

# static files in production
pip install whitenoise

# all at once:
pip install Pillow boto3 django-storages django-crispy-forms crispy-bootstrap5 python-dotenv gunicorn whitenoise
```

### step 14: freeze dependencies
```bash
# save all installed packages
pip freeze > requirements.txt

# this creates requirements.txt with all versions
```

**installing from requirements.txt:**
```bash
# on a new machine
pip install -r requirements.txt
```

---

## phase 7: static and media files

### step 15: collect static files (for production)
```bash
# collect all static files to STATIC_ROOT
python manage.py collectstatic

# output:
# You have requested to collect static files...
# This will overwrite existing files!
# Are you sure you want to do this?
# Type 'yes' to continue: yes
# 
# 128 static files copied to '/path/to/staticfiles'
```

**what this does:**
- gathers CSS/JS from all apps
- copies to STATIC_ROOT directory
- ready for serving in production

**other static file commands:**
```bash
# check for static file issues
python manage.py findstatic style.css

# list all static files
python manage.py collectstatic --dry-run
```

---

## phase 8: database management commands

### viewing database
```bash
# open Django shell
python manage.py shell

# now you're in Python shell with Django loaded
>>> from blog.models import Post
>>> Post.objects.all()
>>> Post.objects.create(title='Test', content='Content', author_id=1)
>>> exit()
```

### database shell
```bash
# open database shell (SQLite, PostgreSQL, etc.)
python manage.py dbshell

# for SQLite:
sqlite> .tables
sqlite> SELECT * FROM blog_post;
sqlite> .quit
```

### flush database (DANGEROUS)
```bash
# delete all data (keeps structure)
python manage.py flush

# WARNING: this deletes EVERYTHING
# asks for confirmation
```

### reset a specific app
```bash
# delete and recreate tables for an app
python manage.py migrate blog zero  # rollback all migrations
python manage.py migrate blog       # reapply migrations
```

---

## phase 9: testing

### run tests
```bash
# run all tests
python manage.py test

# run tests for specific app
python manage.py test blog

# run specific test class
python manage.py test blog.tests.PostModelTest

# run specific test method
python manage.py test blog.tests.PostModelTest.test_post_creation

# verbose output
python manage.py test --verbosity=2

# keep test database (faster for repeated runs)
python manage.py test --keepdb
```

---

## phase 10: git setup

### step 16: initialize git
```bash
# initialize repository
git init

# output:
# Initialized empty Git repository in /path/to/EngineersEcho/.git/
```

### step 17: create .gitignore
```bash
# create .gitignore file
touch .gitignore

# add common Django ignores:
# - __pycache__/
# - *.pyc
# - db.sqlite3
# - .env
# - venv/
# - media/
# - staticfiles/
```

**typical Django .gitignore:**
```
# Python
__pycache__/
*.py[cod]
*.so

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
venv/
env/

# IDE
.vscode/
.idea/
*.swp
```

### step 18: first commit
```bash
# stage all files
git add .

# commit
git commit -m "Initial commit: Django project setup"
```

### step 19: create GitHub repository
```bash
# 1. go to github.com
# 2. click "New repository"
# 3. name it "EngineersEcho"
# 4. don't initialize with README (you already have code)
# 5. copy the repository URL
```

### step 20: push to GitHub
```bash
# add remote
git remote add origin https://github.com/yourusername/EngineersEcho.git

# push
git push -u origin main

# or if you're on master:
git push -u origin master
```

**other git commands:**
```bash
# check status
git status

# see changes
git diff

# add specific files
git add blog/models.py

# commit with message
git commit -m "Add Post model"

# push
git push

# pull latest changes
git pull

# create branch
git checkout -b feature-branch

# merge branch
git checkout main
git merge feature-branch

# view commit history
git log

# undo last commit (keep changes)
git reset --soft HEAD~1

# undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## other useful Django commands

### project information
```bash
# check Django version
python -m django --version

# or
django-admin --version

# check project settings
python manage.py check

# check with deployment checklist
python manage.py check --deploy

# show all available commands
python manage.py help

# help for specific command
python manage.py help migrate
```

### user management
```bash
# create superuser (interactive)
python manage.py createsuperuser

# change user password
python manage.py changepassword admin

# create user (in shell)
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('john', 'john@example.com', 'password123')
```

### shell commands
```bash
# standard shell
python manage.py shell

# shell with IPython (better)
pip install ipython
python manage.py shell  # automatically uses IPython

# shell with auto-imports
pip install django-extensions
python manage.py shell_plus
```

### cleaning commands
```bash
# remove all .pyc files
find . -name "*.pyc" -delete

# remove all __pycache__ directories
find . -type d -name "__pycache__" -delete

# clean migrations (CAREFUL)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

### development utilities
```bash
# show URLs (requires django-extensions)
pip install django-extensions
python manage.py show_urls

# run server with specific settings
python manage.py runserver --settings=EngineersEcho.settings.dev

# create app with custom template
python manage.py startapp myapp --template=/path/to/template
```

---

## complete project creation timeline (summary)

```bash
# 1. setup
mkdir EngineersEcho && cd EngineersEcho
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. install Django
pip install django

# 3. create project
django-admin startproject EngineersEcho .

# 4. create apps
python manage.py startapp blog
python manage.py startapp users

# 5. install dependencies
pip install Pillow boto3 django-storages django-crispy-forms crispy-bootstrap5 python-dotenv gunicorn whitenoise

# 6. edit settings.py, add apps to INSTALLED_APPS

# 7. create models in blog/models.py and users/models.py

# 8. create and apply migrations
python manage.py makemigrations
python manage.py migrate

# 9. create superuser
python manage.py createsuperuser

# 10. create views, URLs, templates

# 11. run server
python manage.py runserver

# 12. freeze dependencies
pip freeze > requirements.txt

# 13. git setup
git init
touch .gitignore  # add Django ignores
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/EngineersEcho.git
git push -u origin main
```

---

## deployment commands

### production setup
```bash
# collect static files
python manage.py collectstatic --no-input

# run with Gunicorn
gunicorn EngineersEcho.wsgi:application --bind 0.0.0.0:8000

# run with Gunicorn + workers
gunicorn EngineersEcho.wsgi:application --workers 3 --bind 0.0.0.0:8000

# run as daemon
gunicorn EngineersEcho.wsgi:application --daemon --workers 3 --bind 0.0.0.0:8000

# with environment variables
ENV=production python manage.py runserver
```

### migration in production
```bash
# check migrations status
python manage.py showmigrations

# migrate without asking
python manage.py migrate --no-input

# migrate with fake (mark as done without running)
python manage.py migrate --fake
```

---

## debugging commands

### check for issues
```bash
# run all checks
python manage.py check

# check specific app
python manage.py check blog

# check for deployment issues
python manage.py check --deploy

# check templates
python manage.py check --tag templates
```

### inspecting database
```bash
# show database info
python manage.py inspectdb

# export database to Python models (reverse engineering)
python manage.py inspectdb > models.py

# show SQL for a migration
python manage.py sqlmigrate blog 0001

# show SQL for all unapplied migrations
python manage.py sqlmigrate blog
```

### clear cache
```bash
# clear Django cache (if using caching)
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

## environment-specific commands

### development
```bash
# run with debug mode
DEBUG=True python manage.py runserver

# run with specific settings
python manage.py runserver --settings=EngineersEcho.settings.dev

# enable auto-reload
python manage.py runserver --noreload  # disable auto-reload
```

### testing
```bash
# run with test settings
python manage.py test --settings=EngineersEcho.settings.test

# run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # creates htmlcov/ directory
```

### production
```bash
# check production readiness
python manage.py check --deploy

# run without debug
DEBUG=False python manage.py runserver

# use production settings
python manage.py runserver --settings=EngineersEcho.settings.prod
```

---

## data management commands

### backup database
```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# dump data to JSON
python manage.py dumpdata > backup.json

# dump specific app
python manage.py dumpdata blog > blog_backup.json

# dump with indentation (readable)
python manage.py dumpdata --indent 2 > backup.json

# exclude specific models
python manage.py dumpdata --exclude auth.permission > backup.json
```

### restore database
```bash
# load data from JSON
python manage.py loaddata backup.json

# load specific fixture
python manage.py loaddata blog/fixtures/initial_data.json
```

### clear database
```bash
# delete all data
python manage.py flush

# delete specific app's data (in shell)
python manage.py shell
>>> from blog.models import Post
>>> Post.objects.all().delete()
```

---

## custom management commands

### creating your own commands
```bash
# create directory structure:
# blog/
# └── management/
#     ├── __init__.py
#     └── commands/
#         ├── __init__.py
#         └── my_command.py

# my_command.py:
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom command'
    
    def handle(self, *args, **options):
        self.stdout.write('Hello!')

# run it:
python manage.py my_command
```

---

## package management

### pip commands
```bash
# list installed packages
pip list

# show package details
pip show django

# check for outdated packages
pip list --outdated

# upgrade package
pip install --upgrade django

# upgrade all packages (careful!)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

# uninstall package
pip uninstall django

# install specific version
pip install django==4.2.8

# install from GitHub
pip install git+https://github.com/user/repo.git
```

---

## quick reference cheat sheet

### daily use
```bash
python manage.py runserver        # start dev server
python manage.py makemigrations   # create migrations
python manage.py migrate          # apply migrations
python manage.py createsuperuser  # create admin
python manage.py shell            # open shell
python manage.py test             # run tests
```

### project setup
```bash
django-admin startproject name .  # create project
python manage.py startapp name    # create app
pip freeze > requirements.txt     # save dependencies
pip install -r requirements.txt   # install dependencies
```

### database
```bash
python manage.py dbshell          # database shell
python manage.py dumpdata         # backup data
python manage.py loaddata         # restore data
python manage.py flush            # clear database
```

### git
```bash
git add .                         # stage all
git commit -m "message"           # commit
git push                          # push to remote
git pull                          # pull latest
git status                        # check status
```

### production
```bash
python manage.py collectstatic    # collect static files
python manage.py check --deploy   # deployment check
gunicorn EngineersEcho.wsgi:application  # run with Gunicorn
```

---

## troubleshooting commands

### common issues

**"No module named 'app_name'"**
```bash
# check INSTALLED_APPS in settings.py
# make sure app is registered
```

**"No migrations to apply"**
```bash
# delete migrations folder (except __init__.py)
# run makemigrations again
rm -rf blog/migrations
mkdir blog/migrations
touch blog/migrations/__init__.py
python manage.py makemigrations
```

**"Table already exists"**
```bash
# fake initial migration
python manage.py migrate --fake-initial
```

**"Port already in use"**
```bash
# find process using port 8000
lsof -i :8000  # on macOS/Linux
# kill it
kill -9 <PID>

# or use different port
python manage.py runserver 8080
```

**"CSRF verification failed"**
```bash
# clear browser cookies
# check CSRF_TRUSTED_ORIGINS in settings.py
# check {% csrf_token %} in forms
```

---

## summary

you now have:
- **complete project creation steps**
- **all Django management commands**
- **git workflow commands**
- **debugging and troubleshooting commands**
- **production deployment commands**

keep this as a reference - you'll use these constantly!
