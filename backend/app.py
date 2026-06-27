import os, re, sqlite3
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
BASE = Path(__file__).parent
DB_PATH = BASE / "database.db"
app = Flask(__name__)
CORS(app)

READ_ONLY_ERROR = "Only read-only SELECT queries are allowed."
INVALID_SQL_ERROR = "The generated query references tables or columns that do not exist."
FORBIDDEN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE|ATTACH|DETACH|PRAGMA|VACUUM)\b", re.I)

def db():
    connection = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    return connection

def schema_text():
    with db() as conn:
        parts=[]
        for row in conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
            parts.append(row["sql"])
        return "\n".join(parts)

def clean_sql(text):
    text = re.sub(r"^```(?:sql)?\s*|\s*```$", "", text.strip(), flags=re.I)
    match = re.search(r"\b(?:SELECT|WITH)\b[\s\S]*", text, re.I)
    return (match.group(0) if match else text).strip().rstrip(";")

def validate_sql(sql):
    normalized = re.sub(r"--.*?$|/\*[\s\S]*?\*/", " ", sql, flags=re.M).strip()
    if not re.match(r"^(SELECT|WITH)\b", normalized, re.I) or FORBIDDEN.search(normalized):
        raise ValueError(READ_ONLY_ERROR)
    if ";" in normalized.rstrip(";"):
        raise ValueError(READ_ONLY_ERROR)

def run_query(sql):
    validate_sql(sql)
    try:
        with db() as conn:
            cursor = conn.execute(sql)
            rows = [dict(r) for r in cursor.fetchmany(1001)]
        if len(rows)>1000: rows=rows[:1000]
        return rows
    except sqlite3.Error:
        raise LookupError(INVALID_SQL_ERROR)

def generate_sql(prompt):
    key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    app.logger.info("Groq API key loaded: %s", bool(key))
    app.logger.info("Using Groq model: %s", model_name)
    if not key:
        raise RuntimeError("Groq API key not found. Add GROQ_API_KEY to backend/.env")

    system_prompt = (
        "You are an expert SQLite query generator. Convert natural language into "
        "valid SQLite SELECT statements. Generate only read-only queries. Use only "
        "the provided schema. Return only SQL without explanations, markdown, or "
        "code fences."
    )
    user_prompt = f"Database Schema:\n{schema_text()}\n\nUser Request:\n{prompt}"

    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )
        response_text = response.choices[0].message.content
        if not response_text or not response_text.strip():
            raise RuntimeError(
                "Groq returned an empty response. Please rephrase your question and try again."
            )

        sql = clean_sql(response_text)
        app.logger.info("Generated SQL query: %s", sql)
        return sql
    except RuntimeError:
        raise
    except Exception:
        app.logger.exception("Groq SQL generation failed")
        raise RuntimeError(
            "Groq could not generate a SQL query. Please try again in a moment."
        )

def meaningful(value):
    return isinstance(value,str) and len(value.strip())>=3 and bool(re.search(r"[A-Za-z]",value))

@app.get("/health")
def health(): return jsonify(status="ok")

@app.get("/schema")
def schema():
    with db() as conn:
        tables=[]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
            cols=[dict(c) for c in conn.execute(f'PRAGMA table_info("{row[0]}")')]
            tables.append({"name":row[0],"columns":[{"name":c["name"],"type":c["type"]} for c in cols]})
    return jsonify(tables=tables)

@app.post("/generate-query")
def generate():
    prompt=(request.get_json(silent=True) or {}).get("prompt","")
    if not meaningful(prompt): return jsonify(error="Please enter a meaningful question."),400
    try:
        sql=generate_sql(prompt.strip()); validate_sql(sql)
        return jsonify(sql=sql,results=[],rowCount=0)
    except ValueError as e: return jsonify(error=str(e)),400
    except Exception as e:
        app.logger.exception("Query generation failed")
        message=str(e) if isinstance(e,RuntimeError) else "Unable to generate SQL right now. Please try again."
        return jsonify(error=message),502

@app.post("/execute-query")
def execute():
    sql=(request.get_json(silent=True) or {}).get("sql","")
    if not isinstance(sql,str) or not sql.strip(): return jsonify(error=INVALID_SQL_ERROR),400
    try:
        rows=run_query(clean_sql(sql)); message=None if rows else "Query executed successfully. No results found."
        return jsonify(sql=clean_sql(sql),results=rows,rowCount=len(rows),message=message)
    except ValueError as e: return jsonify(error=str(e)),400
    except LookupError as e: return jsonify(error=str(e)),400

if __name__ == "__main__":
    if not DB_PATH.exists():
        from seed import seed_database; seed_database()
    app.run(host="0.0.0.0",port=int(os.getenv("PORT",5000)),debug=os.getenv("FLASK_DEBUG")=="1")
