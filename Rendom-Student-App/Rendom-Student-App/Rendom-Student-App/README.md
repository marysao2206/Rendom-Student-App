# Rendom-Student-App — API version

This small project now includes a minimal Flask-based API in `app.py`.

Quick start (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
python app.py
```

Endpoints:
- `GET /api/status` — simple health check JSON
- `GET /api/templates` — returns JSON list of templates in `Templates/`
- `GET /api/template/<name>` — returns rendered HTML in JSON, or raw HTML if `?html=true`

The root path `/` still renders `Templates/index.html` so the existing frontend can work.

Notes:
- Static files are served from the existing `Satic/` directory at `/api/static/<filename>`.
- For production use, run with a WSGI server (gunicorn/uvicorn) and behind a reverse proxy.
