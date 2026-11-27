import os
import sqlite3

from flask import Flask, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS caller_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                caller_name TEXT NOT NULL,
                tag TEXT DEFAULT 'Verified',
                spam_reports INTEGER DEFAULT 0
            )
            """
        )
        seed_records = [
            ("+917234999557", "Raj Gautam", "Founder & Developer", 0),
        ]
        for phone_number, caller_name, tag, spam_reports in seed_records:
            conn.execute(
                """
                INSERT OR IGNORE INTO caller_records (phone_number, caller_name, tag, spam_reports)
                VALUES (?, ?, ?, ?)
                """,
                (phone_number, caller_name, tag, spam_reports),
            )
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def home():
    return render_template("index.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True)
