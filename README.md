# api

## Local development

### Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (see [`.env.example`](.env.example) for a template):
   - `JWT_SECRET`: Secret key for signing access and refresh tokens.
   - `SUPABASE_URL`: Supabase project URL.
   - `SUPABASE_KEY`: Supabase service or anon key used for database access.
   - `DATABASE_NAME`: Supabase schema/database name to query (e.g., `public`).
   - `ALLOWED_ORIGINS` (optional): Comma-separated list of allowed CORS origins; defaults to `*`.
4. Run the FastAPI application with auto-reload using uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

### Environment variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

### Example requests
- Public health check:
  ```bash
  curl http://127.0.0.1:8000/public/health
  ```
- Public listings (no authentication required):
  ```bash
  curl http://127.0.0.1:8000/public/listings
  ```
- Login to obtain tokens:
  ```bash
  curl -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "demo@example.com", "password": "changeme"}'
  ```
- Access private endpoints with the bearer token from the login response:
  ```bash
  ACCESS_TOKEN="<paste-access-token>"
  curl -X POST http://127.0.0.1:8000/private/listings \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"title": "New listing", "description": "Details", "price": 42}'
  ```
