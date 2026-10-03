# Serendib AI

> An intelligent multi-agent AI travel planning system for personalized Sri Lankan travel experiences.

## Overview

**Serendib AI** is a multi-agent tourism planning system that helps travellers create personalized trips across Sri Lanka.

The system combines traveller preferences, destination and attraction recommendations, local food and accommodation suggestions, route planning, budget analysis, safety and travel-context information, crowd prediction, dynamic replanning, and day-by-day itinerary generation.

Instead of relying on one AI component for the complete planning process, Serendib AI uses specialized agents that communicate through a structured backend workflow.

## Key Features

- Natural-language travel planning
- Traveller profile and preference extraction
- Destination and attraction recommendations
- Interest-to-experience matching
- Local food and restaurant recommendations
- Accommodation recommendations
- Route and travel-time planning
- Budget estimation and constraint checking
- Safety and travel-context information
- Crowd prediction
- Dynamic itinerary replanning
- Personalized day-by-day itinerary generation
- User authentication and protected APIs
- Premium subscription and payment support

## System Architecture

```text
Natural-Language Traveller Request
                |
                v
      Agent 1 - Traveller Profile
                |
                v
      Structured Traveller Profile
                |
        +-------+-------+
        |               |
        v               v
 Agent 2 -          Agent 3 -
 Destination &      Food / Restaurant &
 Experience         Accommodation
        |               |
        +-------+-------+
                |
                v
      Agent 4 - Smart Trip Planner
                |
        +-------+-------+-------+
        |       |               |
        v       v               v
      Route   Budget     Safety / Context
                |
                v
      Crowd Prediction & Replanning
                |
                v
      Agent 5 - Schedule / Itinerary
                |
                v
       Final Day-by-Day Plan
                |
                v
             Frontend
```

## Agents

### Agent 1 - Traveller Profile & Preference Agent

Extracts and normalizes traveller information from natural-language requests.

Main responsibilities:

- Traveller profile extraction
- Preference normalization
- Travel type identification
- Budget and flexibility extraction
- Travel pace identification
- Crowd preference identification
- Dietary preference extraction
- Missing-information handling

### Agent 2 - Destination & Experience Intelligence Agent

Uses information retrieval and relevance ranking to recommend destinations, attractions, and experiences.

Main responsibilities:

- Destination discovery
- Explicit destination handling
- Attraction retrieval
- Interest-to-experience matching
- Attraction ranking
- Destination relevance scoring

### Agent 3 - Local Food / Restaurant & Accommodation Agent

Provides destination-specific food and accommodation recommendations.

Main responsibilities:

- Restaurant recommendations
- Dietary compatibility
- Local food recommendations
- Accommodation recommendations
- Traveller and destination context matching

### Agent 4 - Smart Trip Planner Agent

Combines outputs from the previous agents with route, budget, safety, context, and crowd information.

Main responsibilities:

- Destination sequencing
- Route and travel-time estimation
- Budget calculation
- Budget constraint checking
- Safety and travel-context handling
- Crowd prediction
- Travel constraint handling
- Dynamic replanning
- Route-aware planning

### Agent 5 - Schedule / Itinerary Agent

Transforms the final planning context into a structured day-by-day itinerary.

Main responsibilities:

- Daily activity scheduling
- Morning, afternoon, and evening planning
- Travel blocks
- Accommodation integration
- Food integration
- Activity timing
- Travel-pace handling
- Personalized itinerary generation

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- LangGraph

### Database

- MongoDB Atlas

### AI / Intelligence

- Groq
- Gemini
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Information Retrieval (IR)

### External APIs and Services

- Geoapify - geocoding and routing
- Stripe - subscription and payment processing

## Data Sources

The system uses structured and curated data for destination intelligence and trip planning.

Key data includes:

- Sri Lankan cities and destinations
- Attractions
- Activities and experiences
- Attraction-experience relationships
- Sri Lankan road data
- Bus fare data
- Scenic place data
- Application data stored in MongoDB Atlas

The validated destination dataset includes:

- 13 cities
- 87 attractions
- 33 activity/experience definitions
- 279 attraction-experience relationships

## Project Structure

```text
serendib-ai/
|
+-- backend/
|   +-- agents/
|   +-- graph/
|   +-- routes/
|   +-- services/
|   +-- data/
|   +-- tests/
|   +-- main.py
|   +-- requirements.txt
|   +-- package.json
|
+-- frontend/
|   +-- src/
|   +-- public/
|   +-- package.json
|
+-- README.md
+-- .gitignore
```

## Requirements

Before running the project, install:

- Python 3.11+
- Node.js
- MongoDB Atlas access
- Required API credentials
- Stripe CLI for local payment/webhook testing

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd serendib-ai
```

### 2. Backend Setup

Open a terminal in the project directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend` directory.

Use the required configuration for your local environment:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=serendib_ai

APP_NAME=Serendib AI
APP_ENV=development

HOST=127.0.0.1
PORT=8000

JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

GEOAPIFY_API_KEY=your_geoapify_api_key
GEOAPIFY_GEOCODING_URL=https://api.geoapify.com/v1/geocode/search
GEOAPIFY_ROUTING_URL=https://api.geoapify.com/v1/routing

GENAI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

**Do not commit the real `.env` file or any secret values to GitHub.**

### 4. Start the Backend

From the `backend` directory:

```bash
npm start
```

Alternatively:

```bash
python -m uvicorn main:app --reload
```

The backend is available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Open the local URL displayed by Vite.

## Stripe Local Webhook Testing

Stripe is used for premium subscription processing.

For local development, authenticate the Stripe CLI:

```bash
stripe login
```

Then start the webhook listener:

```bash
stripe listen --events checkout.session.completed,customer.subscription.deleted --forward-to http://127.0.0.1:8000/api/payment/webhook
```

If a specific Stripe API key is required for the configured development sandbox:

```bash
stripe listen --api-key YOUR_STRIPE_TEST_SECRET_KEY --events checkout.session.completed,customer.subscription.deleted --forward-to http://127.0.0.1:8000/api/payment/webhook
```

Use the webhook signing secret printed by the active listener in the local backend environment.

**Never publish Stripe secret keys or webhook signing secrets in this repository.**

## Running the System

A typical local development setup uses three terminals.

### Terminal 1 - Backend

```bash
cd backend
npm start
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

### Terminal 3 - Stripe Webhook Listener

```bash
stripe listen --events checkout.session.completed,customer.subscription.deleted --forward-to http://127.0.0.1:8000/api/payment/webhook
```

Then open the frontend and use the travel planning and subscription features.

## Testing

Backend tests can be executed using:

```bash
pytest
```

The project includes testing for areas such as:

- Authentication
- Authorization
- Privacy and data protection
- Information retrieval
- Destination recommendation
- Route planning
- Agent functionality
- Itinerary generation
- Subscription and payment integration

## Security

Sensitive configuration is stored using environment variables.

The following must never be committed to GitHub:

- API keys
- Stripe secret keys
- Stripe webhook secrets
- JWT secrets
- Database passwords
- Authentication tokens
- Passwords

The `.gitignore` file should exclude local environment files and other sensitive development files.

## Responsible AI

Serendib AI is designed with responsible AI considerations including:

- Grounding recommendations in retrieved data
- Avoiding unsupported destination information
- Input and output validation
- Structured communication between agents
- Authentication and authorization
- User-data isolation
- Protection of sensitive information
- LLM fallback handling
- Graceful handling of invalid requests

## Example Use Case

A traveller can provide a natural-language request such as:

```text
I want to plan a relaxing trip to Sri Lanka.
I love nature, photography, mountains and waterfalls.
I prefer vegetarian food and want comfortable accommodation.
My budget is 100,000 LKR.
I want to avoid crowded places and long uncomfortable journeys.
```

Serendib AI processes the request through the multi-agent workflow and generates a personalized plan containing:

- Recommended destinations
- Relevant attractions and experiences
- Route information
- Estimated travel time
- Budget information
- Accommodation
- Food recommendations
- Safety and travel context
- Crowd considerations
- Day-by-day itinerary
- Replanning when constraints change

## Contributors

### Serendib AI Development Team

- Member 1 - Traveller Profile & Preference Agent
- Member 2 - Destination & Experience Intelligence Agent
- Member 3 - Food, Restaurant & Accommodation Intelligence Agent
- Member 4 - Smart Trip Planner Agent

## Academic Project

Serendib AI was developed as a university multi-agent AI tourism planning project.

The project demonstrates the practical integration of:

- Multi-Agent Systems
- Large Language Models
- Natural Language Processing
- Information Retrieval
- Recommendation Systems
- Route Planning
- Budget and Constraint Handling
- Responsible AI
- API Integration
- Secure Web Application Development
