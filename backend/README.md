# APIN Backend

FastAPI + SQLite backend for the AI Parking Spot Intelligence Network (APIN).

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to explore the API.

## Seed demo data

```bash
python app/seed_demo_data.py
```

## Run mock detector

```bash
python scripts/run_mock_detector.py
```
