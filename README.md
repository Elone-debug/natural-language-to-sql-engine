# Natural Language to SQL Engine

A full-stack AI-powered application that enables users to query a relational database using plain English. The system leverages a Large Language Model (Groq LLM API) to dynamically generate SQL queries, execute them against a real SQLite database, and present the results through an interactive web interface.

## Features

* Convert natural language questions into SQL queries.
* View and optionally edit the generated SQL before execution.
* Execute read-only SQL queries against a real SQLite database.
* Display query results in a dynamic and scrollable table.
* Maintain query history within the current session.
* Explore the database schema through a dedicated schema explorer.
* Prevent execution of unsafe SQL operations.

---

## Technologies Used

### Frontend

* React 19
* Vite
* Tailwind CSS
* Axios

### Backend

* Flask
* Flask-CORS
* SQLite
* Groq API (LLM for SQL generation)

---

## Database Schema

The application uses a realistic e-commerce database consisting of three related tables.

### Customers

Stores customer information such as:

* Customer ID
* Name
* Email
* City
* Account creation date

### Products

Stores product details including:

* Product ID
* Product Name
* Category
* Price
* Stock Quantity

### Orders

Stores purchase transactions:

* Order ID
* Customer ID (Foreign Key)
* Product ID (Foreign Key)
* Quantity
* Order Total
* Order Date

### Sample Dataset

The database is automatically seeded with:

* 60 Customers
* 60 Products
* 120 Orders

---

## Project Setup

### Backend Setup

Open the first terminal and execute:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Environment Configuration

The repository contains a `.env.example` file.

Create a new `.env` file by copying the example file:

```powershell
Copy-Item .env.example .env
```

Open the newly created `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
PORT=5000
```

**Note:** The `.env` file is intentionally excluded from version control for security reasons. Only `.env.example` is included in the repository.

### Database Setup

Seed the database with sample data:

```powershell
python seed.py
```

### Start Backend Server

```powershell
python app.py
```

The backend server runs on:

```text
http://localhost:5000
```

---

## Frontend Setup

Open a second terminal while keeping the backend server running.

Execute:

```powershell
cd frontend
npm install
npm run dev
```

The frontend application runs on:

```text
http://localhost:5173
```

---

## Running the Application

Both servers must be running simultaneously.

### Terminal 1

Run the Flask backend:

```powershell
cd backend
python app.py
```

### Terminal 2

Run the React frontend:

```powershell
cd frontend
npm run dev
```

After both servers start successfully, open:

```text
http://localhost:5173
```

in your browser.

---

## API Endpoints

| Method | Endpoint          | Description                         |
| ------ | ----------------- | ----------------------------------- |
| GET    | `/health`         | Checks backend health               |
| GET    | `/schema`         | Returns database schema             |
| POST   | `/generate-query` | Generates SQL from natural language |
| POST   | `/execute-query`  | Executes validated SQL              |

---

## Assumptions and Trade-offs

* Only read-only SQL operations (`SELECT`, `WITH`) are permitted.
* Data modification statements such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, and `ALTER` are blocked.
* SQLite is opened in query-only mode to provide an additional layer of security.
* Query results are limited to 1000 rows to maintain application performance.
* Browser-based query history is maintained locally for the current session.

---

## Future Improvements

Potential enhancements include:

* SQL AST parsing for advanced query validation.
* User authentication and authorization.
* Query result export as CSV.
* Server-side query history persistence.
* Query caching for repeated requests.
* Pagination support for large result sets.
* Advanced analytics and visualizations.

---

## Repository

Clone the repository using:

```bash
git clone https://github.com/Elone-debug/natural-language-to-sql-engine.git
```

---

## Author

**Elbin Sojan**

B.Tech Computer Science Engineering Graduate (2026)
