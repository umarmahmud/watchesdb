## A demo FastAPI project

This is a demo project that can serve as a production-ready template for FastAPI apps.

### Features (v1.0)

- `src`-based project layout with sample models, services and CRUD endpoints (with `async`)
- Database setup with SQLAlchemy 2.x (with `async`) and PostgreSQL
- Auth setup using JWT tokens and scopes
- Files for logging configuration and custom exceptions
- A `tests` folder with sample tests using pytest and HTTPX `AsyncClient`
- Redis caching with fastapi-cache
- A `docker-compose.yml` file with profiles for *dev*, *test* and *prod* environments
- A robust `nginx.conf` file for *prod* environments with SSL (using Let's Encrypt) and rate limiting

To run the app in *dev*: `docker compose --profile dev up`

To run the app in *prod*: `docker compose --profile prod up -d`