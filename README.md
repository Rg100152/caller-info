# Caller Info

**Caller Info** is an open-source, Python-based web application for real-time telephone number intelligence and telecom metadata lookup. It provides a dark cyber-glassmorphism interface for scanning domestic and international phone numbers.

> Developed by **Raj Gautam** · MIT License

## Features

- **Telecom Metadata** — Carrier/operator, telecom circle/region, line type, and time zone.
- **Caller Identification** — Crowdsourced caller names, verification tags, and spam report counts.
- **Community Contributions** — Submit caller names and report spam through the web UI.
- **REST API** — JSON endpoints for scan and update operations.
- **Zero-config Storage** — Embedded SQLite database auto-created on startup.

## Tech Stack

- **Backend:** Python, Flask
- **Telecom Engine:** `phonenumbers`
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)

## Project Structure

```text
caller-info/
├── app.py                  # Flask HTTP server + REST API
├── database.db             # Auto-generated SQLite3 database
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── LICENSE                 # MIT License
└── templates/
    └── index.html          # Frontend UI
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python app.py
```

### 3. Open the app

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000).

## API

### `POST /api/scan`

Request:

```json
{
  "number": "7234999557",
  "region": "IN"
}
```

Success response:

```json
{
  "status": "success",
  "data": {
    "e164": "+917234999557",
    "formatted": "+91 72349 99557",
    "name": "Raj Gautam",
    "tag": "Founder & Developer",
    "spam": 0,
    "operator": "Reliance Jio",
    "circle": "Uttar Pradesh (East)",
    "line": "Mobile",
    "timezone": "Asia/Calcutta"
  }
}
```

### `POST /api/update`

Request:

```json
{
  "e164": "+919876543210",
  "name": "Rohan Verma",
  "is_spam": false
}
```

Success response:

```json
{
  "status": "success",
  "message": "Caller Info database updated successfully."
}
```

## Notes

- Carrier data is based on original number allocation and may show `Unknown / Ported` for ported numbers.
- All database writes use parameterized SQL queries.

## License

MIT © Raj Gautam
