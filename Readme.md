# Aurenza Manager

This repository now includes a full React frontend implementation at `frontend-react` that replaces the earlier Streamlit UI.

## Backend (FastAPI)

```powershell
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

## Frontend (React + Vite)

```powershell
cd frontend-react
copy .env.example .env
npm install
npm run dev
```

React app runs at `http://localhost:5173` and connects to backend at `http://localhost:8000` by default.

## Implemented React Modules

- Login with token + role persistence
- Dashboard with P&L summary cards
- Projects create flow (`/projects/create`)
- Expenses add flow (`/expenses/add`)
- Users create flow (`/users/create`)
- P&L admin screen (`/pnl`)
- Responsive sidebar layout + modern UI theme
