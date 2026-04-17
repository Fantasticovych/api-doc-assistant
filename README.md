# API Documentation Assistant

A robust, AI-powered tool designed to automatically generate clean, developer-facing API documentation from raw OpenAPI specifications. Built with a modern microservices architecture, it seamlessly analyzes endpoint descriptions and generates comprehensive Markdown documentation using LLMs.

## Key Features

- **Specification Upload:** Parse and store OpenAPI specifications (JSON/YAML) securely in the database.
- **AI-Powered Analysis:** Integrates with OpenAI to automatically generate endpoint summaries, request/response documentations, and realistic example payloads.
- **Validation Rules & Missing Fields:** Detects gaps in existing documentation and suggests robust validation rules.
- **Asynchronous Processing:** Utilizes FastAPI `BackgroundTasks` to prevent timeout errors during heavy LLM processing.
- **Markdown Export:** Generates and downloads a perfectly formatted `.md` file ready for developer portals or GitHub.

## 🛠 Tech Stack

- **Framework:** FastAPI (Python 3.11+)
- **Database ORM:** Prisma (PostgreSQL)
- **AI Integration:** OpenAI API (`gpt-4o-mini`)
- **Data Validation:** Pydantic (Strict typing with Union types)
- **Infrastructure:** Docker & Docker Compose
- **Testing & CI/CD:** Pytest, Flake8, GitHub Actions

##  Project Structure

```text
├── app/
│   ├── api/            # FastAPI routers (upload, documentation)
│   ├── core/           # Configuration and DB lifespan events
│   ├── schemas/        # Pydantic models for validation
│   ├── services/       # Business logic (LLM, Export, Upload)
│   └── main.py         # Application entry point
├── prisma/
│   └── schema.prisma   # Database schema models
├── tests/              # Pytest unit tests
├── .github/workflows/  # CI/CD pipelines
├── Dockerfile          # App containerization instructions
└── docker-compose.yml  # Multi-container orchestration
```
##  How to Run Locally (Docker)

The application is fully dockerized. You do not need to install Python or PostgreSQL on your local machine.

### 1. Prerequisites
- Docker Desktop installed and running
- An active OpenAI API key

---

### 2. Environment Setup

Create a `.env` file in the root directory and add your OpenAI key
(the database URL will be handled automatically by Docker):

```env
OPENAI_API_KEY=sk-your-real-openai-key-here
```
### 3. Start the Application

Run the following command in your terminal to build and start the containers:

```bash
docker-compose up --build -d
```
### 4.  Access the API

Once the containers are running, navigate to the interactive Swagger UI:

 **Swagger Docs:** http://localhost/docs

---

##  Available Commands & Usage

If you prefer to run the project locally without Docker, use the following commands:

###  Setup

```bash
# Create virtual environment
python -m venv venv

# Activate venv (Linux/Mac)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
###  Database

```bash
# Generate Prisma Client
prisma generate

# Push DB Schema
prisma db push
```

###  Run & Test

```bash
# Run local server
uvicorn app.main:app --reload

# Run tests
pytest -v

# Check code style
flake8 .
```
