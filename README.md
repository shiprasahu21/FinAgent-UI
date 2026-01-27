# Financial Advisor Agent UI

A Streamlit-based user interface for the Financial Advisor Agent platform, providing a visual dashboard for AI-powered financial analysis agents.

## Features

- **Agent Dashboard**: View all available LLM agents in a clean card-based layout (max 3 per row)
- **Agent Configuration**: View the complete JSON configuration for each agent
- **Agent Details**: Natural language description of agent capabilities, tools, and instructions
- **Real-time API Integration**: Fetches agent data from the backend API

## Prerequisites

- Python 3.9+
- Backend API running at `http://localhost:5111`

## Setup

1. Activate the conda environment:
```bash
conda activate ui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## API Requirements

The application expects the following API endpoint to be available:

- `GET http://localhost:5111/agents` - Returns list of available agents

## Project Structure

```
.
├── app.py                  # Main application entry point
├── pages/                  # Multi-page app pages
├── components/             # Reusable UI components
├── utils/                  # Utility functions and helpers
├── assets/                 # Static assets
│   ├── images/            # Image files
│   └── styles/            # Custom CSS files
├── config/                 # Configuration files
│   └── config.py          # API and app configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration

Edit `config/config.py` to modify:
- `API_BASE_URL`: Backend API base URL (default: `http://localhost:5111`)
- `APP_NAME`: Application title

## Development

- Add new pages in the `pages/` directory
- Create reusable components in the `components/` directory
- Add utility functions in the `utils/` directory
