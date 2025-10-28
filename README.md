# Placement Tracker 2025-26

A full-stack web application for tracking college placement data with statistics, search, and sortable data table.

## Features

- 📊 **Statistics Dashboard**: View comprehensive placement statistics including:

  - Total unique companies
  - Average stipend and CTC
  - Student distribution by offer type
  - Median package secured

- 🔍 **Search & Filter**: Search companies by name with real-time filtering

- 📈 **Sortable Table**: Click on column headers to sort by any field

- ➕ **Add/Edit Records**: Easy-to-use form to add or edit company data

- 🗑️ **Delete Records**: Remove outdated or incorrect entries

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Frontend**: React
- **API**: RESTful API with CORS enabled

## Quick Start (Windows)

### Prerequisites

- Python 3.8+
- Node.js 14+

### 🚀 Setup & Run (Super Easy!)

**Option 1: Batch Files (Recommended)**

1. Double-click `start_backend.bat` - Backend starts with 31 sample companies
2. Double-click `start_frontend.bat` - Frontend opens in browser
3. Done! You're viewing the app at http://localhost:3000

**Option 2: Manual Commands**

**Backend:**

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Frontend:**

```bash
cd frontend
npm install
npm start
```

> **Note:** Using SQLite - no database setup needed! The app automatically creates the database and seeds it with your data.

## Troubleshooting

### "localhost not reachable" Error

**Solution:** Make sure the backend is running first!

1. Check the backend terminal - it should show "Application startup complete"
2. Look for `placement_tracker.db` file in the backend folder
3. Backend must run before frontend can connect

### Port Already in Use

**Solution:**

- Change backend port in `backend/run.py` (line 13)
- Or kill the process using that port

### Module Not Found Errors

**Solution:**

- Backend: Run `pip install -r requirements.txt` in backend folder
- Frontend: Run `npm install` in frontend folder

## API Endpoints

- `GET /api/companies` - Get all companies
- `GET /api/companies/{id}` - Get a specific company
- `POST /api/companies` - Create a new company
- `PUT /api/companies/{id}` - Update a company
- `DELETE /api/companies/{id}` - Delete a company
- `GET /api/stats` - Get placement statistics

**API Docs:** http://localhost:8000/docs (auto-generated Swagger UI)

## Usage

1. Start backend server (creates database and seeds data)
2. Start frontend server
3. Open `http://localhost:3000` in your browser
4. View statistics and search/sort companies
5. Click "+ Add Company" to add new records
6. Use Edit/Delete buttons to manage existing data

## Sample Data

The app comes pre-loaded with 31 placement records from your provided data, including companies like:

- DEShaw (₹59.3L CTC)
- ZS Associates (₹14.15L CTC)
- MakeMyTrip (₹22L CTC)
- Tekion, Sprinklr, Whatfix, and many more!

## Database

SQLite database file: `backend/placement_tracker.db`

- Automatically created on first run
- Pre-seeded with sample data
- No configuration needed!

## Contributing

Feel free to submit issues and pull requests!

## License

MIT
## Admin Access (RBAC)

- Reads are public (no login needed):
  - `GET /api/companies`, `GET /api/companies/{id}`, `GET /api/stats`
- Writes require admin token:
  - `POST /api/companies`, `PUT /api/companies/{id}`, `DELETE /api/companies/{id}`

### Configure admin token

- Set `ADMIN_TOKEN` in `backend/.env` (copy from `backend/.env.example`):

```
cd backend
copy .env.example .env
# edit .env and change ADMIN_TOKEN
```

The frontend provides a small "Admin token" field in the header. Paste your token there to enable Add/Edit/Delete buttons. Without a token the app runs in read‑only mode.
