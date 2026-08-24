# FlightHunterAI

A flight search and comparison engine with smart search, a custom scoring system (FlightHunter Score), and real bookings integrated with the [Duffel API](https://duffel.com).

A personal project built end to end: from setting up the environment to creating real orders with commercial airlines (Air Canada, American Airlines, and more).

---

## Screenshots

<!-- Add your screenshots here -->

| Flight search | Results with FlightHunter Score |
|---|---|
| (screenshot pending) | (screenshot pending) |

| Confirmed booking |
|---|
| (screenshot pending) |

---

## Features

- Real-time flight search by origin, destination, dates, and number of passengers, with airport autocomplete.
- Real connection to commercial airlines through the Duffel API (live mode).
- FlightHunter Score: a custom scoring system that evaluates each flight based on price, stops, and airline reliability, with clear reasons shown to the user.
- Automatic highlighting of the best option among the results.
- Duplicate removal and comparison across multiple providers (architecture ready to add more beyond Duffel).
- Full, real booking flow: offer verification, passenger data, order creation, and confirmation with booking reference (PNR) and Order ID.
- Custom HTML/CSS/JavaScript interface, with a minimalist Nike-inspired design (black/white with a red accent).

---

## Tech stack

**Backend**
- Python 3.12
- FastAPI
- Uvicorn
- HTTPX
- Pydantic

**Frontend**
- HTML / CSS / JavaScript (vanilla)

**Flight integration**
- [Duffel API](https://duffel.com/docs/api/overview/welcome) (Flights, Offer Requests, Orders)

---

## Project structure

```
FlightHunterAI/
  app/
    main.py                 # API routes (FastAPI)
    config.py                # Environment variable loading
    models/
      vuelo.py                # Flight data model
    providers/
      provider.py              # Base provider interface
      mock.py                   # Test provider (simulated data)
      duffel.py                 # Real provider (Duffel API)
      manager.py                # Provider orchestrator
    services/
      buscador.py               # Search logic and orchestration
      comparador.py              # Result deduplication
      duracion.py                 # Flight duration calculation
      evaluador.py                 # Flight evaluation
      scoring.py                    # FlightHunter Score
      iata.py                        # City to IATA code conversion
      buscador_ciudades.py            # City search
      oferta.py                        # Offer verification and order creation (Duffel)
    data/
      airport_service.py         # Airport autocomplete
    static/
      css/style.css
      js/app.js
    templates/
      index.html
  venv/
  .env                     # Environment variables (not included in the repo)
  .env.example              # Environment variable template
  .gitignore
  README.md
```

---

## Installation and setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/FlightHunterAI.git
cd FlightHunterAI
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and add your own Duffel API key:

```bash
cp .env.example .env
```

Edit `.env` with your data:

```env
DUFFEL_API_KEY=duffel_test_your_token_here
```

You can use a test token (`duffel_test_...`) to explore the project without connecting to real airlines, or a live token (`duffel_live_...`) if you have already activated your Duffel account for production mode. Get your token from the [Duffel Dashboard](https://app.duffel.com).

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The application will be available at http://127.0.0.1:8000.

---

## Main endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Home page |
| GET | `/vuelos` | Flight search (`origen`, `destino`, `fecha_salida`, `fecha_regreso`, `adultos`) |
| GET | `/ciudades` | City search |
| GET | `/aeropuertos` | Airport autocomplete (`?buscar=...`) |
| GET | `/oferta/{offer_id}` | Verifies that an offer is still valid |
| POST | `/reserva/preparar/{offer_id}` | Revalidates price and availability before booking |
| POST | `/reserva/crear/{offer_id}` | Creates the real order in Duffel with the passenger's data |

---

## How the FlightHunter Score works

Each flight receives a score from 0 to 100, calculated based on:

- Price relative to other options in the search
- Number of stops
- Airline reliability

The result includes explainable reasons (e.g. "Good price", "Many stops", "Reliable airline") shown directly on each flight card.

---

## Note on Duffel Live mode

This project can connect in test mode (simulated data, fictional "Duffel Airways" carrier) or in live mode (real airlines and real prices). In live mode, completing the booking flow (`POST /reserva/crear/{offer_id}`) creates a real order and a real charge against the Duffel Balance of the configured account. Use it with caution if you connect your own live token.

---

## Roadmap

- Custom-designed booking confirmation modal (replace `alert()`)
- Image upload from the admin panel
- Email notifications with booking details
- Production deployment

---

## Author

Armando

---

## License

This project is for personal use / portfolio purposes. If you would like to use parts of the code, please credit the original author.
