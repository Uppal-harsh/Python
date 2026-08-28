# 🚨 SENTINEL — Smart No-Parking Zone Violation Detection System

A real-time vehicle monitoring and enforcement simulation system with ANPR (Automatic Number Plate Recognition) simulation, automated challan generation, and SMS warning alerts.

---

## 🏗️ Architecture

```
smart-parking-system/
│
├── backend/
│   ├── app.py              # Flask server with REST API endpoints
│   ├── enforcement.py      # Background enforcement thread (timer logic)
│   ├── database.py         # In-memory data store (vehicles, SMS, challans)
│   └── plate_generator.py  # Indian number plate generator
│
├── frontend/
│   ├── index.html          # Single-page monitoring dashboard
│   ├── style.css           # Dark theme CSS (no frameworks)
│   └── app.js              # Vanilla JS (API calls, DOM updates, polling)
│
└── README.md
```

---

## ⚙️ Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- A modern web browser (Chrome, Firefox, Edge)

---

## 🚀 Setup & Run

### 1. Install Python dependencies

```bash
pip install flask flask-cors
```

### 2. Start the backend server

```bash
cd smart-parking-system
python backend/app.py
```

The server will start on **http://localhost:5000** with the enforcement thread running in the background.

### 3. Open the frontend

Open `frontend/index.html` directly in your browser (double-click it or use a local file server).

> **Tip:** If you want to use a local server:
> ```bash
> cd frontend
> python -m http.server 8080
> ```
> Then open **http://localhost:8080**

---

## 🎮 How to Use

1. **Click "Simulate Vehicle Detection"** — Adds a vehicle with a random Indian number plate to the monitoring zone.
2. **Watch the timer** — The table auto-refreshes every 5 seconds showing elapsed time.
3. **After 5 minutes** — Status changes to `ILLEGAL PARKING` → `SMS Sent` (warning logged in SMS panel).
4. **After 7 minutes** — A challan is auto-generated (appears in Challan Records panel).
5. **Click "Vehicle Left"** — Removes a vehicle from tracking before it gets flagged.
6. **Click "View" on a challan** — Opens a styled modal showing the official eChallan document.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/vehicle/detect` | Register a new vehicle (auto-generates plate) |
| `GET` | `/api/vehicles` | Get all active vehicles with elapsed times |
| `POST` | `/api/vehicle/exit` | Remove a vehicle from tracking |
| `GET` | `/api/sms-log` | Get all simulated SMS warnings |
| `GET` | `/api/challans` | Get all issued challans |
| `GET` | `/api/stats` | Get dashboard statistics |

---

## 🔄 Enforcement Logic

```
Vehicle enters zone → Status: "Monitoring"
    │
    ├─ >= 5 minutes → Status: "ILLEGAL PARKING" → SMS Warning → Status: "SMS Sent"
    │
    └─ >= 7 minutes → Challan Generated → Status: "Challan Issued"
```

- Background thread checks all vehicles every **10 seconds**
- SMS warnings include vehicle plate, location, and timestamp
- Challans include unique ID, GPS coordinates, fine amount (₹500), and location

---

## 📝 Notes

- All data is stored **in-memory** — restarting the server clears everything
- No real ANPR, SMS, or database is used — this is a **simulation/demo**
- CORS is enabled on all endpoints for local development
- Number plates follow real Indian format: `[STATE] [DISTRICT] [SERIES] [NUMBER]`

---

## 👥 Built For

JOE (Joint Open Enforcement) Project — Smart Traffic Management System demonstration.

---
