# Natural Language to SQL Engine

A full-stack AI-powered application that enables users to query a relational database using plain English. The system leverages a Large Language Model (Groq LLM API) to dynamically generate SQL queries, execute them against a real SQLite database, and present the results through an interactive web interface.

The application allows users to:

* Enter natural language questions.
* View and optionally edit the generated SQL query.
* Execute read-only SQL queries against a real database.
* Visualize query results in a dynamic table.
* Access query history during the current session.
* Explore the database schema through a dedicated schema explorer.

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

The application uses a realistic e-commerce database consisting of three related tables:

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
* Product name
* Category
* Price
* Stock quantity

### Orders

Stores purchase transactions:

* Order ID
* Customer ID (Foreign Key)
* Product ID (Foreign Key)
* Quantity
* Order total
* Order date

Sample dataset:

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
Copy-Item .env.example .env
```

Update the `.env` file with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Seed the database:

```powershell
python seed.py
```

Start the Flask server:

```powershell
python app.py
```

The backend server runs on:

```text
http://localhost:5000
```

---

### Frontend Setup

Open a second terminal while keeping the backend terminal running.

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

The frontend communicates with the Flask backend through API endpoints.

---

## Running the Application

Both servers must be running simultaneously:

* Terminal 1 → Flask Backend (`http://localhost:5000`)
* Terminal 2 → React Frontend (`http://localhost:5173`)

After starting both servers, open:

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
* SQLite is opened in query-only mode for additional security.
* Query results are limited to 1000 rows to maintain performance.
* Browser-based session history is maintained locally for the current session.

---

## Future Improvements

Potential enhancements include:

* SQL AST parsing for advanced validation.
* User authentication and authorization.
* Query caching for repeated requests.
* Exporting query results as CSV files.
* Server-side query history persistence.
* Pagination for large result sets.

---
