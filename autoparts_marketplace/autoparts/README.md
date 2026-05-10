# AutoParts BD — Spare Parts Marketplace

A production-ready spare parts marketplace web application built with Flask + PostgreSQL.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

---

## 📦 Installation

### Step 1 — Clone / Extract the project
```
cd autoparts
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up PostgreSQL
1. Make sure PostgreSQL is running on your machine.
2. Create the database and tables:

```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql:
CREATE DATABASE autoparts;
\q
```

3. Run the schema file (creates tables + seed data):
```bash
psql -U postgres -d autoparts -f database/schema.sql
```

### Step 5 — Configure environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values:
# - DB_PASSWORD=your_postgres_password
# - FLASK_SECRET_KEY=some-random-secret
```

### Step 6 — Run the application
```bash
python run.py
```

Open your browser: **http://localhost:5000**

Admin panel: **http://localhost:5000/admin**  
Default login: `admin` / `admin123`

---

## 📁 Project Structure

```
autoparts/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── README.md                       # This file
│
├── database/
│   └── schema.sql                  # PostgreSQL schema + seed data
│
└── backend/
    ├── __init__.py
    ├── models/
    │   ├── db.py                   # Database connection helper
    │   ├── product.py              # Product model (CRUD)
    │   └── order.py                # Order model (CRUD)
    │
    ├── routes/
    │   ├── main.py                 # Homepage & search
    │   ├── products.py             # Product detail page
    │   ├── orders.py               # Checkout & order placement
    │   └── admin.py                # Admin panel routes
    │
    ├── templates/
    │   ├── base.html               # Base layout
    │   ├── index.html              # Homepage
    │   ├── product_detail.html     # Product detail
    │   ├── checkout.html           # Order form
    │   ├── order_success.html      # Order confirmation
    │   └── admin/
    │       ├── base.html           # Admin layout
    │       ├── login.html          # Admin login
    │       ├── dashboard.html      # Stats & recent orders
    │       ├── products.html       # Products list
    │       ├── product_form.html   # Add/Edit product form
    │       └── orders.html         # Orders list
    │
    └── static/
        ├── css/
        │   ├── style.css           # Main stylesheet
        │   └── admin.css           # Admin panel styles
        └── js/
            └── main.js             # Frontend JavaScript
```

---

## 🗄️ Database Schema

### products
| Column        | Type          | Notes                  |
|---------------|---------------|------------------------|
| id            | SERIAL PK     | Auto-increment         |
| name          | VARCHAR(255)  | Product name           |
| category      | VARCHAR(100)  | Engine, Brake, etc.    |
| brand         | VARCHAR(100)  | Brand name             |
| price         | DECIMAL(10,2) | Price in BDT (৳)       |
| stock         | INTEGER       | Available quantity     |
| image_url     | VARCHAR(500)  | Product image URL      |
| description   | TEXT          | Product description    |
| compatibility | TEXT          | Compatible vehicles    |
| created_at    | TIMESTAMP     | Auto-set               |

### orders
| Column        | Type          | Notes                        |
|---------------|---------------|------------------------------|
| id            | SERIAL PK     | Auto-increment               |
| product_id    | INTEGER FK    | References products(id)      |
| customer_name | VARCHAR(255)  | Buyer's full name            |
| mobile        | VARCHAR(20)   | Contact number               |
| address       | TEXT          | Delivery address             |
| quantity      | INTEGER       | Units ordered                |
| order_date    | TIMESTAMP     | Auto-set on insert           |
| status        | VARCHAR(50)   | pending/confirmed/shipped... |

---

## 🌐 Routes Reference

| URL                          | Method | Description               |
|------------------------------|--------|---------------------------|
| `/`                          | GET    | Homepage / product list   |
| `/?category=Engine`          | GET    | Filter by category        |
| `/?search=brake`             | GET    | Search products           |
| `/products/<id>`             | GET    | Product detail page       |
| `/orders/checkout/<id>`      | GET    | Checkout form             |
| `/orders/place`              | POST   | Submit order              |
| `/orders/success/<id>`       | GET    | Order confirmation        |
| `/admin/`                    | GET    | Admin dashboard           |
| `/admin/login`               | GET/POST | Admin login            |
| `/admin/products`            | GET    | Product list (admin)      |
| `/admin/products/add`        | GET/POST | Add new product        |
| `/admin/products/edit/<id>`  | GET/POST | Edit product           |
| `/admin/products/delete/<id>`| POST   | Delete product            |
| `/admin/orders`              | GET    | Orders list (admin)       |
| `/admin/orders/status/<id>`  | POST   | Update order status       |
| `/admin/orders/delete/<id>`  | POST   | Delete order              |

---

## ⚙️ Configuration (.env)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=autoparts
DB_USER=postgres
DB_PASSWORD=your_password

FLASK_SECRET_KEY=your-random-secret-key
FLASK_DEBUG=True
FLASK_PORT=5000

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

---

## 🔧 Troubleshooting

**psycopg2 install fails on Windows?**
```bash
pip install psycopg2-binary
```

**Database connection error?**
- Check PostgreSQL is running: `pg_ctl status` or check Services
- Verify credentials in `.env` file
- Make sure database `autoparts` exists

**Port already in use?**
- Change `FLASK_PORT=5001` in `.env`

---

## 🚀 Production Deployment Notes

1. Set `FLASK_DEBUG=False` in `.env`
2. Change `ADMIN_PASSWORD` to a strong password
3. Use a proper WSGI server: `pip install gunicorn && gunicorn run:app`
4. Put behind Nginx for static files & SSL
5. Use environment variables instead of `.env` file in production
