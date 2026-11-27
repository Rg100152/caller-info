# Caller Info

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Embedded-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

**Caller Info** is an open-source, Python-powered web application for real-time telephone number intelligence. It combines offline telecom metadata resolution with a lightweight crowdsourced caller directory, delivered through a modern dark cyber-glassmorphism interface.

> Built by **Raj Gautam** · [MIT License](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Security & Validation](#security--validation)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

Caller Info allows users to scan domestic or international phone numbers and instantly retrieve structured intelligence, including carrier details, region, line type, timezone, and community-reported caller identity signals.

The project is designed to be:

- **Lightweight** — No external database server or paid API required.
- **Portable** — Runs on Linux, Windows, and macOS with Python 3.9+.
- **Extensible** — Clean separation of UI, API routing, metadata extraction, and persistence.

---

## Features

| Capability | Description |
|---|---|
| **Number Validation** | Validates input against E.164 rules using `phonenumbers`. |
| **Telecom Metadata** | Resolves carrier/operator, circle/region, line type, and timezone. |
| **Caller Directory** | Looks up crowdsourced caller name, tag, and spam reports from SQLite. |
| **Community Updates** | Users can submit caller names and report spam via `/api/update`. |
| **REST API** | JSON endpoints for programmatic scan and update workflows. |
| **Responsive UI** | Dark cyber-glassmorphism interface with no external CSS framework. |
| **Safe Defaults** | Parameterized SQL queries and structured JSON error responses. |

---

## Tech Stack

- **Backend:** Python, Flask
- **Telecom Engine:** [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers)
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)

---

## Architecture

Caller Info follows a simple three-tier web architecture:

1. **Presentation Layer** — `templates/index.html` renders the UI and calls REST APIs asynchronously.
2. **Application Layer** — `app.py` handles validation, E.164 normalization, telecom metadata extraction, and API responses.
3. **Data Layer** — `database.db` stores crowdsourced caller records in the `caller_records` table.

```text
Browser (UI)
   │  POST /api/scan, /api/update
   ▼
Flask App (app.py)
   │  validation + phonenumbers metadata
   ▼
SQLite (database.db / caller_records)
```

---

## Getting Started

### Prerequisites

- Python **3.9+**
- `pip`

### Installation

```bash
git clone https://github.com/Rg100152/caller-info.git
cd caller-info
python -m venv venv
```

Activate the virtual environment:

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5000
```

> `database.db` is auto-created on first run and seeded with a baseline record.

---

## API Reference

### `POST /api/scan`

Scans a phone number and returns telecom metadata plus caller directory information.

**Request**

```json
{
  "number": "7234999557",
  "region": "IN"
}
```

**Success Response — `200 OK`**

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

**Error Response — `400 Bad Request`**

```json
{
  "status": "error",
  "message": "Invalid phone number format."
}
```

### `POST /api/update`

Creates or updates a caller record and optionally increments spam reports.

**Request**

```json
{
  "e164": "+919876543210",
  "name": "Rohan Verma",
  "is_spam": false
}
```

**Success Response — `200 OK`**

```json
{
  "status": "success",
  "message": "Caller Info database updated successfully."
}
```

---

## Project Structure

```text
caller-info/
├── app.py                  # Flask application, REST API, DB logic
├── database.db             # Auto-generated SQLite database (gitignored)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
└── templates/
    └── index.html          # Frontend UI (HTML/CSS/JS)
```

---

## Security & Validation

- **Input Validation:** Phone numbers are parsed and validated with `phonenumbers`.
- **SQL Injection Mitigation:** All database operations use parameterized queries (`?` placeholders).
- **Structured Errors:** Invalid inputs return JSON `400` responses; common HTTP/server errors return JSON error payloads.
- **No Secrets in Repo:** The SQLite DB is generated locally and excluded by `.gitignore`.

---

## Limitations

- **MNP (Mobile Number Portability):** Carrier results are based on original number allocation/prefix data. Ported numbers may appear as `Unknown / Ported`.
- **Crowdsourced Data:** Caller names/tags depend on community submissions and should be treated as informational signals.
- **Local Database:** SQLite is ideal for lightweight/local use; high-scale deployments should migrate to a managed database.

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature
   ```
3. Commit your changes with a clear message.
4. Push to your fork and open a Pull Request.

For bug reports or feature requests, please open an issue with reproduction steps and expected behavior.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Raj Gautam**  
Open-source developer and creator of Caller Info.

---

*Caller Info — Open-Source Caller & Telecom Intelligence*