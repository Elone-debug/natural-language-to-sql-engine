# Natural Language to SQL Engine

A polished full-stack app that turns plain-English questions into safe SQLite queries with Groq, lets users review/edit the SQL, executes it read-only, and displays searchable session history and dynamic results.

## Stack

- React 19, Vite, Tailwind CSS, Axios
- Flask, Flask-CORS, SQLite
- Groq API

## Setup

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Add your GROQ_API_KEY to .env
python seed.py
python app.py
```

The API runs at `http://localhost:5000`. The database is seeded automatically on first startup if missing. Re-run `python seed.py` to reset it.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to Flask. For a separately hosted API, set `VITE_API_URL=http://localhost:5000` in `frontend/.env`.

## Environment variables

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `GROQ_API_KEY` | Yes | — | Groq authentication |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Model used for SQL generation |
| `PORT` | No | `5000` | Flask port |
| `FLASK_DEBUG` | No | `0` | Set to `1` for debug mode |
| `VITE_API_URL` | No | `/api` | Frontend API base URL |

## Safety and trade-offs

Execution is intentionally separate from generation. SQL must begin with `SELECT` or `WITH`, prohibited write/DDL keywords and multiple statements are rejected, SQLite is opened read-only with `query_only`, and responses are capped at 1,000 rows. Database errors are logged server-side but replaced with safe messages. The lightweight lexical guard is defense in depth with SQLite read-only mode; a larger deployment could add an AST parser, auth, rate limiting, server-side audit history, and pagination. Browser history persists locally (up to 25 queries).
