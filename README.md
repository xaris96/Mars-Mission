# 🚀 Mars Mission CRUD App

## **Description**  
The **Mars Mission CRUD App** is a mission-critical system for managing resources (crew members, equipment, supplies) at the first Martian colony. Built with **Flask**, **SQLite**, and **Docker**, it provides a RESTful API and a simple UI for CRUD operations. The project includes a **CI/CD pipeline** (GitHub Actions) for automated testing, Docker image builds, and secure deployment.

---

## **Key Features**  
- **CRUD Operations**: Manage resources via API or web UI.
- **Automated Testing**: Unit tests with `pytest` (86% coverage) and code quality checks with `pylint`.
- **CI/CD Pipeline**:  
  - Linting, testing, and Docker image builds on every commit.
  - Automatic push to Docker Hub on `main` branch updates.
- **Infrastructure as Code**:  
  - Docker Compose setup for local development (Flask + Nginx).
  - Persistent SQLite database with volume mounting.
- **Simple UI**: Vanilla JavaScript frontend for intuitive resource management.

---

## **🚀 Quick Start with Docker Compose**  
**Prerequisites**: Docker and Docker Compose installed.  

1. Clone the repository:
   ```bash
   git clone https://github.com/xaris96/Mars-Mission.git
   cd Mars-Mission
Start the stack:

bash
Copy
docker-compose up --build
Access the application:

Web UI: http://localhost

API Docs: http://localhost/api

🛠️ Development Setup
Run Locally (Without Docker)
Install Python 3.12+ and dependencies:

bash
Copy
pip install -r requirements.txt
Initialize the database:

bash
Copy
python -c "from app import init_db; init_db()"
Start the Flask server:

bash
Copy
python app.py
Access the UI at http://localhost:5000.

📂 Project Structure
Copy
Mars-Mission/
├── app.py               # Flask backend
├── static/              # Frontend assets (JS/CSS)
│   └── app.js
├── templates/           # HTML templates
│   └── index.html
├── data/                # Database storage
├── Dockerfile           # Flask container setup
├── docker-compose.yml   # Full-stack deployment
├── .github/workflows/   # CI/CD pipelines
│   └── main.yml
└── requirements.txt     # Python dependencies
🔧 CI/CD Pipeline
The GitHub Actions workflow (.github/workflows/main.yml) includes:

Linting: Code quality checks with pylint.

Testing: Unit tests with pytest.

Docker Build:

Builds and pushes the Docker image to Docker Hub.

Tags: xaris96/mars-mission-app:latest.

Branch Protection: Merges to main require passing checks.

API Endpoints
Endpoint	Method	Description	Example Request Body
/api/users	GET	List all resources	-
/add	POST	Add a new resource	{"name": "Rover", "age": 5}
/edit	POST	Update a resource	{"id": 1, "name": "Updated"}
/delete	POST	Delete a resource	{"id": 1}
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
