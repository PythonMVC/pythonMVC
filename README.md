# PythonMVC

Rails-style, batteries-included **PythonMVC** — Starlette + SQLAlchemy, generators, migrations, Redis cache, security middleware (HSTS/CSRF/rate-limit), and a minimal admin — with **convention over configuration**.

<p align="left">
  <a href="https://github.com/PythonMVC/pythonMVC/actions/workflows/python-package.yml">
    <img alt="CI" src="https://github.com/PythonMVC/pythonMVC/actions/workflows/python-package.yml/badge.svg">
  </a>
  <a href="https://github.com/PythonMVC/pythonMVC/actions/workflows/workflow.yml">
    <img alt="Publish" src="https://github.com/PythonMVC/pythonMVC/actions/workflows/workflow.yml/badge.svg">
  </a>
  <a href="https://github.com/PythonMVC/pythonMVC/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/badge/License-Apache--2.0-blue.svg">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.7%2B-3776AB">
</p>

> Status: **v0.2 – developer preview** (APIs may change before v1.0)

---

## ✨ Features

- **Fast ASGI** app (Starlette) with clean MVC conventions  
- **Generators**: `pmvc new`, `pmvc generate model|controller|scaffold`  
- **ORM & Migrations**: SQLAlchemy 2.x + Alembic  
- **Multi-DB (SQL)**: SQLite / PostgreSQL / MySQL (via `DATABASE_URL`)  
- **Caching**: Redis (async)  
- **Security**: HSTS, X-Frame-Options, NoSniff, CSRF token cookie, basic rate limiting  
- **Admin (minimal)**: `/admin` lists models (CRUD on roadmap)

---

## 🚀 Quickstart

```bash
# 0) clone & install (from source)
git clone https://github.com/PythonMVC/pythonMVC.git
cd pythonMVC
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 1) create a new app
pmvc new blog --database=sqlite
# or:
# pmvc new blog --database=postgresql
# pmvc new blog --database=mysql

cd blog

# 2) configure DB + cache
export DATABASE_URL=sqlite:///db/app.db
# export DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/blog
# export DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/blog
export CACHE_URL=redis://localhost:6379/0

# 3) initialize schema (SQL backends)
pmvc db init
pmvc db migrate "init"
pmvc db upgrade

# 4) run dev server
pmvc server
# open http://127.0.0.1:8000/posts  and  http://127.0.0.1:8000/admin
```
PyPI install: once published, you’ll be able to pip install <package-name> and use pmvc directly.

## 🧱 Architecture (at a glance)

- **ASGI app factory** with sensible defaults (sessions, CORS, security headers)
- **MVC**: resource-style routing → controllers → Jinja2 templates
- **Data**: SQLAlchemy 2.x models + Alembic migrations (wrapped by `pmvc db ...`)
- **Cache**: Redis adapter (decorators & cache-aside helpers on roadmap)
- **Security**: middleware for HSTS, frame-deny, NoSniff, CSRF (cookie + header), simple per-IP rate limit
- **Admin**: minimal index at `/admin`; SQLAlchemy CRUD planned

---

## 🗂️ Generated app layout
```kotlin
app/
  controllers/
  models/
  views/
alembic/
db/
public/
python_mvc/       # framework package (installed from this repo)

```


---

## 🧰 CLI

```bash
pmvc new <appname> --database=sqlite|postgresql|mysql
pmvc db init
pmvc db migrate "message"
pmvc db upgrade

# (coming soon)
pmvc generate model <Name> field:type ...
pmvc generate controller <Name>
pmvc generate scaffold <Name> field:type ...
```

**Database URLs**
- SQLite: `sqlite:///db/app.db`  
- PostgreSQL: `postgresql+psycopg://user:pass@host:5432/dbname`  
- MySQL: `mysql+pymysql://user:pass@host:3306/dbname`

---

## ⚙️ Configuration

| Key             | Example                                         | Notes                                   |
|-----------------|--------------------------------------------------|-----------------------------------------|
| `DATABASE_URL`  | `sqlite:///db/app.db`                            | Postgres/MySQL/SQLite via SQLAlchemy    |
| `CACHE_URL`     | `redis://localhost:6379/0`                       | Redis connection string                 |
| `PYTHONMVC_ENV` | `development`                                    | (planned) switch per-environment config |

Security settings (secret, rate limit, header toggles) live in your app `Settings`.

---

## 🔐 Security

- **Headers:** HSTS, X-Frame-Options (DENY), X-Content-Type-Options (NoSniff)  
- **CSRF:** cookie token + `X-CSRF-Token` header or `_csrf` form field  
- **Rate limiting:** simple per-IP bucket (per minute)  
- **CORS/Sessions:** enabled with safe defaults for local dev

---

## 🧪 Testing

- Unit tests via **pytest**  
- (Planned) CI matrix across SQLite, PostgreSQL, and MySQL using GitHub Actions services  
- Run tests:
  ```bash
  pytest -q
  ```

## 🛣️ Roadmap
- **v0.2** - Developer Preview
- **v0.3** — Admin CRUD (SQLAlchemy introspection), Auth generator, Flash messages  
- **v0.4** — Scaffold parity, Alembic UX (`pmvc db` wrappers), env settings, logging/request-IDs  
- **v0.5** — CI DB matrix, CSRF tests (form+JSON), admin integration tests  
- **v1.0** — Docs site (MkDocs), examples, stability, perf pass

See [Issues](https://github.com/PythonMVC/pythonMVC/issues) and the Project board for live progress.

---

## 👋 Contributing

Contributions welcome! A great place to start is any issue labeled **good first issue** / **help wanted**.

Please:
1. Open an issue to discuss significant changes.  
2. Add tests/docs for user-visible behavior.  
3. Run linters/tests locally if configured.

> We use **Apache-2.0**. Add `SPDX-License-Identifier: Apache-2.0` to new files.

---

## 🚢 Release (Trusted Publishing)

Releases are automated from tags using GitHub Actions OIDC (no API tokens).  
Tagging `vX.Y.Z` builds and publishes the wheel/sdist to PyPI.

```bash
# bump version in pyproject.toml + python_mvc/__init__.py
git commit -am "release v0.2.1"
git tag -a v0.2.1 -m "PythonMVC 0.2.1"
git push --follow-tags
```

## 📜 License

**Apache License 2.0** — see [LICENSE](./LICENSE).

---

## 🙌 Acknowledgements

Starlette, SQLAlchemy, Alembic, Typer, and Jinja2 — the foundations this project builds upon.
