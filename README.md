# Legal document portal


# Legal Document Search Portal

A full-stack web application for searching and summarizing legal documents. Built with React frontend and FastAPI backend.

## Project Overview

This application provides a user-friendly interface for legal professionals to search through legal documents and receive AI-assisted summaries. The system uses a mock backend with hardcoded legal documents for demonstration purposes.

## Technology Stack

### Frontend
- **React** - UI framework
- **Vite** - Build tool and development server
- **JavaScript/JSX** - Programming language
- **Tailwind CSS** - CSS Library

### Backend
- **FastAPI** - Python web framework
- **Python 3.9+** - Backend runtime
- **Uvicorn** - ASGI server

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
legal-search-portal/
├── frontend/               # React application
│   ├── src/
│   │   ├── App.jsx        # Main application component
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
├── backend/               # FastAPI application
│   ├── main.py           # API server
│   └── requirements.txt
├── docker-compose.yml    # Docker orchestration
├── Dockerfile.frontend   # Frontend container
├── Dockerfile.backend    # Backend container
└── README.md             # This file
```

## Prerequisites

### For Docker Setup (Recommended)
- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

### For Local Development
- Node.js (version 22)
- npm or yarn
- Python 3.11 
- pip

## Quick Start with Docker

The easiest way to run the application is using Docker Compose:

### 1. Clone or Navigate to Project Directory

```bash
cd legal-search-portal
```

### 2. Build the Docker Images

```bash
docker compose build
```

This command will:
- Build the frontend React application container
- Build the backend FastAPI application container
- Install all necessary dependencies

### 3. Start the Application

```bash
docker compose up
```

Or run in detached mode (background):

```bash
docker compose up -d
```

### 4. Access the Application

Once the containers are running:

- **Frontend**: http://0.0.0.0:3000
- **Backend API**: http://0.0.0.0:8000
- **API Documentation**: http://0.0.0.0:8000/docs

### 5. Stop the Application

Press `Ctrl+C` in the terminal, or if running in detached mode:

```bash
docker compose down
```

## Local Development Setup

If you prefer to run the application without Docker:

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## Features

### User Interface
- Clean, intuitive search interface
- Query input field with submission button
- Real-time response display
- Loading state indicators
- Error handling with user-friendly messages
- Responsive design

### Backend API
- `/generate` endpoint for document search and summarization
- Mock responses using 3 hardcoded legal documents
- CORS enabled for frontend integration
- Comprehensive API documentation via Swagger UI

### Integration
- Seamless frontend-backend communication
- RESTful API architecture
- Error handling and validation

## API Endpoints

### POST /generate

## Docker Configuration Details

### docker-compose.yml

The Docker Compose configuration:
- Orchestrates both frontend and backend services
- Maps appropriate ports for each service
- Sets up network communication between containers
- Manages environment variables

### Dockerfile.frontend

Frontend container specifications:
- Based on Node.js image
- Installs npm dependencies
- Runs Vite development server
- Exposes port 3000

### Dockerfile.backend

Backend container specifications:
- Based on Python image
- Installs Python dependencies
- Runs Uvicorn server
- Exposes port 8000

## Troubleshooting

### Port Already in Use

If you encounter port conflicts:

**Frontend (Port 3000):**
```bash
# Modify in docker-compose.yml or vite.config.js
```

**Backend (Port 8000):**
```bash
# Modify in docker-compose.yml or run command
```

### Docker Build Issues

If build fails, try:
```bash
docker compose build --no-cache
```

### Frontend Can't Connect to Backend

Ensure:
- Both containers are running: `docker compose ps`
- Backend is accessible: http://0.0.0.0:8000/docs
- Check browser console for CORS errors

### Permission Denied (Linux/macOS)

Run Docker commands with sudo or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```

## Development Guidelines

### Code Structure
- Clean, modular component architecture
- Separation of concerns between UI and business logic
- Clear naming conventions
- Comprehensive error handling

### Best Practices
- Use environment variables for configuration
- Implement proper loading states
- Provide meaningful error messages
- Follow React and Python best practices

## Testing

### Manual Testing
1. Start the application using Docker Compose
2. Open http://0.0.0.0:3000 in your browser
3. Enter a search query (e.g., "contract law")
4. Verify the response is displayed correctly
5. Test error scenarios (empty query, network issues)

## Production Deployment

For production deployment, consider:
- Using production builds (React production build)
- Setting up proper environment variables
- Implementing authentication and authorization
- Adding rate limiting and security measures
- Using a production-grade database
- Setting up proper logging and monitoring

## Contributing

This is a test assignment project. For actual contributions:
1. Follow the existing code structure
2. Maintain code quality and documentation
3. Test thoroughly before submission
