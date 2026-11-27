import os
import sqlite3

import phonenumbers
from flask import Flask, jsonify, render_template, request
from phonenumbers import PhoneNumberType, carrier, geocoder, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"status": "error", "message": "Resource not found."}), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({"status": "error", "message": "Method not allowed."}), 405


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"status": "error", "message": "Internal server error."}), 500


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


def get_line_type(number_type):
    mapping = {
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Landline",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Mobile / Landline",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.TOLL_FREE: "Toll-Free",
        PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        PhoneNumberType.SHARED_COST: "Shared Cost",
        PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        PhoneNumberType.PAGER: "Pager",
        PhoneNumberType.UAN: "UAN",
        PhoneNumberType.VOICEMAIL: "Voicemail",
    }
    return mapping.get(number_type, "Unknown")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
def scan_number():
    payload = request.get_json(silent=True) or {}
    number = str(payload.get("number", "")).strip()
    region = str(payload.get("region", "IN")).strip().upper() or "IN"

    if not number:
        return jsonify({"status": "error", "message": "Phone number is required."}), 400

    try:
        parsed = phonenumbers.parse(number, region)
    except phonenumbers.NumberParseException:
        return jsonify({"status": "error", "message": "Invalid phone number format."}), 400

    if not phonenumbers.is_valid_number(parsed):
        return jsonify({"status": "error", "message": "Invalid phone number format."}), 400

    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    operator = carrier.name_for_number(parsed, "en") or "Unknown / Ported"
    circle = geocoder.description_for_number(parsed, "en") or "Unknown"
    line = get_line_type(phonenumbers.number_type(parsed))
    tz = timezone.time_zones_for_number(parsed)
    tz_value = ", ".join(tz) if tz else "Unknown"

    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT caller_name, tag, spam_reports FROM caller_records WHERE phone_number = ?",
            (e164,),
        ).fetchone()
    finally:
        conn.close()

    return jsonify(
        {
            "status": "success",
            "data": {
                "e164": e164,
                "formatted": formatted,
                "name": row["caller_name"] if row else "Unknown Caller",
                "tag": row["tag"] if row else "Unverified",
                "spam": row["spam_reports"] if row else 0,
                "operator": operator,
                "circle": circle,
                "line": line,
                "timezone": tz_value,
            },
        }
    )


@app.route("/api/update", methods=["POST"])
def update_caller():
    payload = request.get_json(silent=True) or {}
    e164 = str(payload.get("e164", "")).strip()
    name = str(payload.get("name", "")).strip()
    is_spam = bool(payload.get("is_spam", False))

    if not e164:
        return jsonify({"status": "error", "message": "E.164 number is required."}), 400

    try:
        parsed = phonenumbers.parse(e164, None)
    except phonenumbers.NumberParseException:
        return jsonify({"status": "error", "message": "Invalid phone number format."}), 400

    if not phonenumbers.is_valid_number(parsed):
        return jsonify({"status": "error", "message": "Invalid phone number format."}), 400

    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    spam_increment = 1 if is_spam else 0

    conn = get_db_connection()
    try:
        row = conn.execute(
            "SELECT caller_name, tag, spam_reports FROM caller_records WHERE phone_number = ?",
            (e164,),
        ).fetchone()
        if row:
            new_name = name or row["caller_name"]
            new_tag = "Spam Alert" if (row["spam_reports"] + spam_increment) > 0 else (row["tag"] if not name else "Verified User")
            conn.execute(
                """
                UPDATE caller_records
                SET caller_name = ?, tag = ?, spam_reports = spam_reports + ?
                WHERE phone_number = ?
                """,
                (new_name, new_tag, spam_increment, e164),
            )
        else:
            new_name = name or "Unknown Caller"
            new_tag = "Spam Alert" if spam_increment > 0 else "Verified User"
            conn.execute(
                """
                INSERT INTO caller_records (phone_number, caller_name, tag, spam_reports)
                VALUES (?, ?, ?, ?)
                """,
                (e164, new_name, new_tag, spam_increment),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"status": "success", "message": "Caller Info database updated successfully."})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
