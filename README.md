🚛 Route Optimization & Fuel Cost API (Django)
Overview

This project is a Django REST API that:

    - Accepts a start and finish location within the USA

    - Retrieves the driving route using a free routing API

    - Determines optimal fuel stops based on cost

    - Assumes:

        - Vehicle range = 500 miles

        - Fuel efficiency = 10 miles per gallon

    -Returns total fuel cost and route map link

        The routing API is called only once per request to ensure performance.

🚀 Tech Stack

    - Python 3.x

    - Django (latest stable)

    - Django REST Framework

    - Requests (for external API calls)

    - OpenRouteService (routing API)

📦 Setup Instructions
    1️- Clone the repository:
        cd <project-folder>
        git clone https://github.com/Damiemmy/fuel_project.git
        

    2- Create virtual environment:
        python -m venv venv
        source venv/bin/activate  # mac/linux
        venv\Scripts\activate     # windows

    3- Install dependencies:
        pip install -r requirements.txt

    4- Add OpenRouteService API Key
        In views.py:
        ORS_API_KEY = "YOUR_API_KEY"
    
    5️- Run migrations:
        python manage.py migrate

    6- Import fuel price data:
        python manage.py import_fuel_data

    7- Run server:
        python manage.py runserver

-🔍 Example API Request:
    GET /api/route/?start=-74.0060,40.7128&finish=-118.2437,34.0522

-📤 Example Response(JSON):
    {
    "route_distance_miles": 2793.52,
    "fuel_stops": [...],
    "total_cost": 750.61,
    "route_map_url": "https://www.openstreetmap.org/..."
    }

-🧮 Calculation Logic:
    Fuel Stops
    Vehicle max range = 500 miles
    number_of_stops = total_distance / 500
    Rounded up to ensure sufficient fuel stops.

-Fuel Cost
    Vehicle efficiency = 10 MPG
    gallons_needed = total_distance / 10
    total_cost = gallons_needed * fuel_price

-⚡ Performance Design

    Only one routing API call per request

    Fuel data stored locally in database

    No repeated external API calls

    Fast response time

-🎥 Demo

A Loom video demonstrating the API and code walkthrough is included with submission.