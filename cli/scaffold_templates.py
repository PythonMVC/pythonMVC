"""Code templates used by the CLI generators."""

PROJECT_SKELETON = {
    "app/__init__.py": "",
    "app/controllers/__init__.py": "",
    "app/models/__init__.py": "",
    "app/views/shared/placeholder.html": """{% extends 'shared/layout.html' %}{% block body %}
<h1>{{ action|capitalize }} placeholder</h1>
<p>Edit your controller to render a specific template.</p>
{% endblock %}""",
    "app/views/shared/layout.html": """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{{ title or 'PythonMVC' }}</title>
    <link rel="stylesheet" href="/static/app.css" />
  </head>
  <body>
    <main class="container">{% block body %}{% endblock %}</main>
  </body>
</html>""",
    "app/main.py": """from starlette.routing import Route
from PythonMVC import create_app, resource
from .controllers.posts_controller import PostsController


class Settings:
    DEBUG = True
    SECRET_KEY = 'dev-secret-change-me'
    STATIC_DIR = 'public'
    DATABASE_URL = 'sqlite:///db/app.db'  # swap to postgresql+psycopg://, mysql+pymysql://, or mongodb://
    CACHE_URL = 'redis://localhost:6379/0'
    SECURITY = {"secret": "dev-secret-change-me", "rate_limit": 120}
    ROUTES = []


# Define resources (add more as you build)
settings = Settings()
settings.ROUTES += resource('posts', PostsController)

app = create_app(settings)
""",
    "public/app.css": "body{font-family:system-ui;margin:2rem} .container{max-width:760px;margin:0 auto}",
    "db/.keep": "",
}

POSTS_CONTROLLER = """from PythonMVC.controller import BaseController
from starlette.requests import Request
from PythonMVC.model import db_session
from .schemas import PostCreate
from ..models.post import Post


class PostsController(BaseController):
    async def index(self, request: Request):
        with db_session() as s:
            posts = s.query(Post).order_by(Post.id.desc()).all()
        return self.render(request, 'posts/index.html', { 'posts': posts })

    async def new(self, request: Request):
        return self.render(request, 'posts/new.html')

    async def create(self, request: Request):
        form = dict(await request.form())
        data = PostCreate(**form)
        with db_session() as s:
            post = Post(title=data.title, body=data.body)
            s.add(post)
            s.commit()
        return self.redirect('/posts')

    async def show(self, request: Request):
        pid = int(request.path_params['id'])
        with db_session() as s:
            post = s.get(Post, pid)
        return self.render(request, 'posts/show.html', { 'post': post })

    async def edit(self, request: Request):
        pid = int(request.path_params['id'])
        with db_session() as s:
            post = s.get(Post, pid)
        return self.render(request, 'posts/edit.html', { 'post': post })

    async def update(self, request: Request):
        pid = int(request.path_params['id'])
        form = dict(await request.form())
        with db_session() as s:
            post = s.get(Post, pid)
            post.title = form.get('title', post.title)
            post.body = form.get('body', post.body)
            s.add(post)
            s.commit()
        return self.redirect(f'/posts/{pid}')

    async def destroy(self, request: Request):
        pid = int(request.path_params['id'])
        with db_session() as s:
            post = s.get(Post, pid)
            s.delete(post)
            s.commit()
        return self.redirect('/posts')
"""

POSTS_MODEL = """from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from PythonMVC.model import BaseModel


class Post(BaseModel):
    __tablename__ = 'posts'
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text())
"""

POSTS_SCHEMAS = """from pydantic import BaseModel, constr


class PostCreate(BaseModel):
    title: constr(min_length=1, max_length=255)
    body: constr(min_length=1)
"""

POSTS_VIEWS = {
    "app/views/admin/index.html": """{% extends 'shared/layout.html' %}{% block body %}
<h1>Admin</h1>
<ul>
  {% for m in models %}
    <li>{{ m.class_.__name__ }} (table: {{ m.local_table.name if m.local_table else 'n/a' }})</li>
  {% endfor %}
</ul>
{% endblock %}""",
    "app/views/posts/index.html": """{% extends 'shared/layout.html' %}{% block body %}
<h1>Posts</h1>
<p><a href="/posts/new">+ New Post</a> · <a href="/admin">Admin</a></p>
<ul>
  {% for p in posts %}
  <li><a href="/posts/{{ p.id }}">{{ p.title }}</a></li>
  {% else %}
  <li>No posts yet.</li>
  {% endfor %}
</ul>
{% endblock %}""",
    "app/views/posts/new.html": """{% extends 'shared/layout.html' %}{% block body %}
<h1>New Post</h1>
<form method="post" action="/posts">
  <p><label>Title <input name="title"></label></p>
  <p><label>Body <textarea name="body"></textarea></label></p>
  <button type="submit">Create</button>
</form>
{% endblock %}""",
    "app/views/posts/show.html": """{% extends 'shared/layout.html' %}{% block body %}
<article>
  <h1>{{ post.title }}</h1>
  <p>{{ post.body }}</p>
</article>
<p><a href="/posts/{{ post.id }}/edit">Edit</a> · <a href="/posts">Back</a></p>
{% endblock %}""",
    "app/views/posts/edit.html": """{% extends 'shared/layout.html' %}{% block body %}
<h1>Edit Post</h1>
<form method="post" action="/posts/{{ post.id }}">
  <input type="hidden" name="_method" value="patch">
  <p><label>Title <input name="title" value="{{ post.title }}"></label></p>
  <p><label>Body <textarea name="body">{{ post.body }}</textarea></label></p>
  <button type="submit">Save</button>
</form>
{% endblock %}""",
}

PYPROJECT = """[project]
name = "pythonmvc"
version = "0.2.1"
description = "Rails-like micro-framework on Starlette + SQLAlchemy, with cache, security, admin"
authors = [{name = "QuantaDev.io", email = "opensource@quantadev.io"}]
requires-python = ">=3.11"
dependencies = [
  "starlette>=0.40",
  "uvicorn[standard]>=0.30",
  "SQLAlchemy>=2.0",
  "alembic>=1.13",
  "jinja2>=3.1",
  "typer>=0.12",
  "pydantic>=2.8",
  "redis>=5.0",
  "psycopg[binary]>=3.2",
  "pymysql>=1.1",
  "itsdangerous>=2.2",
  "python-multipart>=0.0.9",
]

[project.scripts]
pmvc = "PythonMVC.cli:app"
"""

ALEMBIC_INI = """[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///db/app.db
"""

ALEMBIC_ENV = """from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import *  # import models for autogenerate
from PythonMVC.model import BaseModel

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
