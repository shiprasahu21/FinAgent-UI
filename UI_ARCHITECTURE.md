# Financial Advisor UI - Architecture Overview

## 1. Overview

The Financial Advisor UI is a **Streamlit-based web application** that provides an interface for users to interact with AI-powered financial advisory agents. The UI connects to a **FastAPI backend (FinAgent)** running on `localhost:5111`.

**Key Technologies:**
- Frontend: Streamlit (Python)
- Backend: FastAPI (AgentOS)
- Database: SQLite (local user profiles)
- Styling: Custom CSS with dark theme

---

## 2. Agent Library

**File:** `pages/1_Agents_Library.py`

The Agent Library allows users to browse and select from available AI agents and teams.

### Features:
- **Teams Section:** Collaborative agent teams (e.g., Investment Team, Personal Finance Team)
- **Agents Section:** Individual specialized agents for specific tasks
- **Card Display:** Each agent/team shows name, description, model info, and tools available
- **Actions per Card:**
  - 💬 **Chat** - Start conversation with selected agent/team
  - ⚙️ **Config** - View raw JSON configuration
  - 📄 **Details** - Human-readable breakdown (team members, tools, instructions)

### Data Flow:
```
UI → GET /agents, /teams → Render Cards → User Selection → Navigate to Chat
```

---

## 3. User Data Gathering

**File:** `pages/2_User_Profile.py`

Comprehensive financial profile form collecting user data for personalized advice.

### Data Categories Collected:

| Section | Fields |
|---------|--------|
| **Personal** | Age, gender, marital status, dependents, city |
| **Income** | Monthly income, employment type, job stability, industry |
| **Expenses** | Housing, food, transport, utilities, healthcare, EMIs (9 categories) |
| **Insurance** | Life, health, term coverage + annual premiums |
| **Savings** | Emergency fund, FDs, MFs, stocks, PPF, NPS, EPF, gold, real estate |
| **Tax Planning** | 80C, 80D, 80CCD deductions with progress tracking |
| **Real Estate** | Ownership status, rent, property value, home loan details |
| **Goals** | Short/medium/long-term goals, retirement age, SIP targets |

### Storage:
- **SQLite database** (`data/users.db`)
- Profile data stored as **JSON** for flexibility
- Functions: `save_user_profile()`, `get_user_profile()`, `format_user_profile_for_agent()`

### Key Feature:
User profile is **formatted into structured text** and injected into agent prompts for context-aware responses.

---

## 4. Chat Component

**File:** `app.py`

The main chat interface for conversing with agents/teams.

### Session Management:
```python
session_state = {
    "messages": [],           # Chat history
    "selected_agent_id": str, # Current agent/team
    "selected_type": str,     # "agent" or "team"
    "session_id": uuid,       # Unique per conversation
    "active_user_id": str,    # Selected user profile
}
```

### Core Functions:

| Function | Purpose |
|----------|---------|
| `send_message_to_agent()` | POST to `/agents/{id}/runs` or `/teams/{id}/runs` |
| `build_message_with_history()` | Combines user profile + current query + last 5 messages |
| `render_chat_view()` | Full chat interface with message bubbles |
| `render_home_view()` | Landing page with `@agent-id` search |

### Message Flow:
```
User Input → Parse @mention → Build Structured Message (Profile + History + Query) 
           → POST to Backend → Display Response with Token Count
```

### Agent Selection Methods:
1. **Direct mention:** Type `@agent-id message` in chat
2. **Search:** Type `@name` to search agents/teams
3. **Library:** Browse and click "Chat" from Agent Library

---

## 5. Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
├─────────────┬─────────────────┬─────────────────────────┤
│  app.py     │ 1_Agents_Library│  2_User_Profile.py      │
│  (Chat)     │ (Browse)        │  (Data Collection)      │
└──────┬──────┴────────┬────────┴───────────┬─────────────┘
       │               │                    │
       │ HTTP Requests │                    │ SQLite
       ▼               ▼                    ▼
┌──────────────────────────┐         ┌─────────────┐
│  FinAgent API (:5111)    │         │  users.db   │
│  - GET /agents           │         │  (profiles) │
│  - GET /teams            │         └─────────────┘
│  - POST /agents/{id}/runs│
│  - POST /teams/{id}/runs │
└──────────────────────────┘
```

---

## 6. Configuration

**File:** `config/config.py`

```python
API_BASE_URL = "http://localhost:5111"
AGENTS_ENDPOINT = f"{API_BASE_URL}/agents"
TEAMS_ENDPOINT = f"{API_BASE_URL}/teams"
AGENT_RUN_ENDPOINT = f"{API_BASE_URL}/agents/{agent_id}/runs"
TEAM_RUN_ENDPOINT = f"{API_BASE_URL}/teams/{team_id}/runs"
```

---

**Summary:** The UI provides a clean separation between agent discovery (Library), user context gathering (Profile), and conversation (Chat), with all components sharing state via Streamlit's `session_state` and communicating with the FinAgent backend via REST APIs.

