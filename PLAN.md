# Vue + Django Learning Plan

Goal: build a minimal Django backend paired with a Vue frontend by hand, to get hands-on familiarity with both.

Layout: `django-backend/` (Django API) and `vue-frontend/` (Vue SPA) as sibling folders.

## Backend: Setup
1. `cd C:\Dev\Studies\scrap\vue-django-app\django-backend`
2. `uv` manages the virtual environment automatically per-project (`.venv/`, tracked via `pyproject.toml`/`uv.lock`) — no manual `python -m venv` step needed; every command below runs through `uv run` so it uses that environment
3. `uv add django` — installs Django into the project's `uv`-managed environment

## Backend: Scaffold the project
4. `uv run django-admin startproject config .` (the trailing dot avoids an extra nested folder) — generates `manage.py` and a `config/` package with `settings.py`, `urls.py`, `wsgi.py`
5. Run `uv run manage.py runserver` and hit `localhost:8000` — confirms the skeleton works before adding anything

## Backend: Create an app
6. `uv run manage.py startapp notes` — Django projects are composed of "apps" (reusable modules); one project can have many
7. Add `'notes'` to `INSTALLED_APPS` in `config/settings.py` — commonly forgotten step, good to know cold

## Backend: Switch to Postgres (job requirement — swapped in for the SQLite default)
8. Install Postgres locally (native Windows install, not Docker/hosted for this project) and set a password for the `postgres` superuser during setup
9. Create a dedicated database and role/user for this project via `psql` or pgAdmin, rather than using the `postgres` superuser directly — least-privilege habit, avoids an app with full DB-admin rights
10. `uv add "psycopg[binary]"` — the driver Django needs to speak Postgres' wire protocol (SQLite needs no driver since Python's stdlib has `sqlite3` built in; Postgres does)
11. In `config/settings.py`, change `DATABASES['default']['ENGINE']` from `django.db.backends.sqlite3` to `django.db.backends.postgresql`, and add `NAME`/`USER`/`PASSWORD`/`HOST`/`PORT` — pull these from `.env` (same pattern as `SECRET_KEY`), never hardcode DB credentials
12. `uv run manage.py check` — confirms Django can actually connect to the new Postgres database before building anything on top of it

## Backend: Model (the M in MTV)
13. In `notes/models.py`, define a simple `Note` model (e.g. `title`, `body`, `created_at`) — maps to a database table via Django's ORM
14. `uv run manage.py makemigrations` then `uv run manage.py migrate` — makemigrations diffs models against the last known state and writes a migration file; migrate applies it to the DB (now Postgres)

## Backend: Admin
15. `uv run manage.py createsuperuser`
16. Register `Note` in `notes/admin.py`
17. Log into `/admin` and add a record by hand — fastest way to see the ORM/admin value prop, a big Django talking point

## Backend: View + URL + Template (the V and T)
18. Write a simple view in `notes/views.py` that queries `Note.objects.all()` and renders a template
19. Wire up `notes/urls.py` and include it from `config/urls.py` — Django's URL routing is explicit and file-based, worth understanding vs. decorator-based routing in Flask
20. Create `notes/templates/notes/list.html` using Django's template language (`{% for note in notes %}`) to display the notes — this confirms the classic server-rendered MTV flow works before decoupling it behind an API

## Backend: expose an API (for the Vue frontend to consume)
21. `uv add djangorestframework` and add `'rest_framework'` to `INSTALLED_APPS` — DRF is the standard way to turn Django views into JSON endpoints
22. Create a `NoteSerializer` in `notes/serializers.py` — serializers convert model instances to/from JSON, DRF's analogue to a Django Form
23. Add an API view (e.g. `ListCreateAPIView`) and wire it to `/api/notes/` — this is the endpoint the Vue app will call, separate from the template-rendering view in step 18
24. `uv add django-cors-headers`, add it to `INSTALLED_APPS`/`MIDDLEWARE`, and allow the Vue dev server's origin (e.g. `http://localhost:5173`) — browsers block cross-origin requests by default, so the API needs to explicitly allow the frontend's dev port

## Frontend: Setup
25. `cd C:\Dev\Studies\scrap\vue-django-app\vue-frontend` then `npm create vue@latest .` — scaffolds a Vite-based Vue project (choose defaults; TypeScript/router optional for this scrap)
26. `npm install` then `npm run dev` — confirms the default Vue skeleton loads before wiring it to Django

## Frontend: consume the API
27. Create a `NotesList.vue` component that calls `fetch('http://localhost:8000/api/notes/')` (or `axios`) in `onMounted`, stores the result in a `ref`, and renders it with `v-for` — Vue's reactivity system (`ref`/`reactive`) is the equivalent of the state Django's template loop reads from `notes`
28. Import and render `NotesList` from `App.vue`
29. (Optional) Add a small form component that `POST`s a new note back to `/api/notes/`, so the round trip (Vue form → Django API → DB → back to Vue) is complete

## Wrap-up talking points to be ready to discuss

**Django**
- MTV vs MVC naming
- ORM vs raw SQL tradeoffs
- what a migration is and why they're checked into version control
- settings.py as the central config (DB, installed apps, middleware)
- Django REST Framework as the common pairing for building APIs
- SQLite vs Postgres: why Django defaults to SQLite (zero-config) but production/most real deployments use Postgres; swapping is just an `ENGINE` change plus a driver (`psycopg`), which speaks to the ORM's job of abstracting the specific database

**Vue**
- Composition API (`ref`/`reactive`, `<script setup>`) vs the older Options API
- Single-File Components (`.vue`: template/script/style together) vs JSX
- Vue's reactivity model vs React's virtual-DOM diffing, at a high level
- Vite as the dev server/build tool (fast HMR) vs older webpack-based tooling

**How the two sides fit together**
- decoupled SPA + API architecture vs server-rendered templates: what you gain (frontend/backend can scale and deploy independently, any client can consume the API) and what you give up (extra moving parts: CORS, two dev servers, auth has to cross the boundary)
- why CORS exists and why it bites people the first time they split frontend/backend onto different ports in dev
- this project deliberately builds both the server-rendered version (steps 18-20) and the API + SPA version (steps 21-24) so you can speak to trade-offs between them, not just recite one approach
