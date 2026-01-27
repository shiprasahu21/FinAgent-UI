"""
Application Configuration

Contains configuration settings for the application.
"""

# Application settings
APP_NAME = "Financial Advisor Agent"
APP_VERSION = "1.0.0"

# API Configuration
API_BASE_URL = "http://localhost:5111"
AGENTS_ENDPOINT = f"{API_BASE_URL}/agents"
TEAMS_ENDPOINT = f"{API_BASE_URL}/teams"

# Agent/Team run endpoints (use .format(agent_id=...) or .format(team_id=...))
AGENT_RUN_ENDPOINT = f"{API_BASE_URL}/agents/{{agent_id}}/runs"
TEAM_RUN_ENDPOINT = f"{API_BASE_URL}/teams/{{team_id}}/runs"
