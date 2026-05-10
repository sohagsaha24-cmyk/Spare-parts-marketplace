# Auto Parts Marketplace (Single Page)

This project is a **single-page Auto Parts Marketplace** built with:

- **Python (Flask)**
- **PostgreSQL**
- **HTML/CSS/JS** (one-page UI at `/` that loads data via `/api/*`)

## Quick start (Windows)

### 1) Create `.env`

Copy `autoparts/.env.example` to `autoparts/.env` and set your DB credentials.

> Important: do **not** commit `.env` to git (it’s ignored by `.gitignore`).

### 2) Setup database + tables

From the `autoparts/` folder:

```bash
python setup_db.py
```

### 3) Run the app

```bash
python run.py
```

Open `http://localhost:5000`.

## Endpoints

- `GET /` single-page marketplace
- `GET /api/categories`
- `GET /api/products?category=&search=`
- `POST /api/products` (JSON body)

