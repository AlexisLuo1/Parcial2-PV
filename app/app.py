from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

@app.route("/")
def home():
    return jsonify({"message": "Aplicación desplegada en AWS ECS correctamente"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/db-check")
def db_check():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"db_time": str(result[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
