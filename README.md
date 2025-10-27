# PythonMVC

Rails-style, batteries-included **PythonMVC**: Starlette + SQLAlchemy, generators, migrations, Redis cache, security middleware (HSTS/CSRF/ratelimit), and a minimal admin — with **convention over configuration**.

> Status: v0.2.x (developer preview)

## ✨ Features
- **Fast ASGI** app (Starlette) + **clean MVC** conventions
- **Generators**: `pymvc new`, `pymvc generate model|controller|scaffold`
- **ORM & Migrations**: SQLAlchemy 2.x + Alembic
- **Multi-DB (SQL)**: SQLite / PostgreSQL / MySQL
- **Caching**: Redis (async)
- **Security**: HSTS, X-Frame-Options, nosniff, CSRF token cookie, simple rate limit
- **Admin (minimal)**: `/admin` lists models (CRUD roadmap)

## 🚀 Quickstart
```bash
pip install -e .

# create a new app
pymvc new blog --database=sqlite
# or
pymvc new blog --database=postgresql
pymvc new blog --database=mysql

cd blog

# configure (examples)
export DATABASE_URL=sqlite:///db/app.db
# export DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/blog
# export DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/blog
export CACHE_URL=redis://localhost:6379/0

# init schema (SQL backends)
pymvc db init
pymvc db migrate "init"
pymvc db upgrade

# run
pymvc server
# visit http://127.0.0.1:8000/posts and /admin
