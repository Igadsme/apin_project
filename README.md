# APIN – AI Parking Spot Intelligence Network (MVP)

This repository contains a minimal end‑to‑end prototype of the **AI Parking Spot Intelligence Network (APIN)**:

- Backend API built with FastAPI + SQLite
- Data model for lots, cameras, and parking spots
- Mock vision service that simulates occupancy detection
- Simple web dashboard that shows live availability per lot

This is an MVP scaffold designed so you can replace the mock vision service with a real computer‑vision model later.

In the later update patch
upgraded features include: ML models that can predict when the reduction in traffic is happening
ML model that can predict the time when traffic and use phone motion sensors to reduce traffic and phone prediction models to tell when traffic is reduced


## Quick Start

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend API:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at: `http://127.0.0.1:8000`  
   Docs: `http://127.0.0.1:8000/docs`

4. Seed a demo parking lot with spots:

   ```bash
   python app/seed_demo_data.py
   ```

5. Start the mock detector (simulates CV reading from cameras and updating spot status):

   ```bash
   python scripts/run_mock_detector.py
   ```

6. Open the web dashboard:

   - Open `frontend/index.html` in your browser (or serve it with a simple HTTP server).
