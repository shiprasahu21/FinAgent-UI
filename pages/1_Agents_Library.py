"""
Agents Library Page - View all available agents and teams
"""

import streamlit as st
import requests
import json
import uuid
from config.config import APP_NAME, AGENTS_ENDPOINT, TEAMS_ENDPOINT

# Page configuration
st.set_page_config(
    page_title=f"Library - {APP_NAME}",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Title styling */
    .main-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #7c3aed, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-family: 'Space Mono', monospace;
        font-size: 0.95rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: 0.05em;
    }
    
    /* Section header */
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-subheader {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    
    /* Card base styling */
    .card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        transition: all 0.3s ease;
        min-height: 180px;
        cursor: pointer;
    }
    
    .card:hover {
        border-color: rgba(124, 58, 237, 0.5);
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
        transform: translateY(-2px);
    }
    
    /* Team card specific */
    .team-card {
        border-left: 3px solid #f472b6;
    }
    
    .team-card:hover {
        border-color: rgba(244, 114, 182, 0.5);
        border-left-color: #f472b6;
        box-shadow: 0 8px 32px rgba(244, 114, 182, 0.15);
    }
    
    /* Agent card specific */
    .agent-card {
        border-left: 3px solid #7c3aed;
    }
    
    .card-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.3rem;
        letter-spacing: -0.01em;
    }
    
    .card-role {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #7c3aed;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.8rem;
    }
    
    .team-role {
        color: #f472b6;
    }
    
    .card-description {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #94a3b8;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .card-footer {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #64748b;
        margin-top: 0.8rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(100, 116, 139, 0.2);
    }
    
    .id-badge {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    
    .agent-id-badge {
        background: rgba(124, 58, 237, 0.15);
        color: #a78bfa;
    }
    
    .team-id-badge {
        background: rgba(244, 114, 182, 0.15);
        color: #f472b6;
    }
    
    /* Members badge */
    .members-badge {
        display: inline-block;
        background: rgba(0, 212, 255, 0.15);
        color: #00d4ff;
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        margin-left: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: transparent;
        border: 1px solid rgba(100, 116, 139, 0.3);
        color: #94a3b8;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        border-color: #7c3aed;
        color: #a78bfa;
        background: rgba(124, 58, 237, 0.1);
    }
    
    /* Dialog styling */
    div[data-testid="stDialog"] {
        background: rgba(15, 23, 42, 0.95) !important;
    }
    
    div[data-testid="stDialog"] > div {
        background: rgba(30, 41, 59, 0.95) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 16px !important;
    }
    
    /* Error styling */
    .error-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    .error-text {
        font-family: 'DM Sans', sans-serif;
        color: #fca5a5;
        font-size: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def fetch_agents():
    """Fetch agents from the API"""
    try:
        response = requests.get(AGENTS_ENDPOINT, timeout=None)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


def fetch_teams():
    """Fetch teams from the API"""
    try:
        response = requests.get(TEAMS_ENDPOINT, timeout=None)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


def extract_description(item):
    """Extract a short description from the item"""
    # First check for direct description field (teams have this)
    if item.get("description"):
        desc = item.get("description", "")
        sentences = desc.split(". ")
        if sentences:
            return ". ".join(sentences[:2]) + (
                "." if not sentences[0].endswith(".") else ""
            )

    # Fall back to system_message for agents
    system_message = item.get("system_message", {})

    # Check for description in system_message
    if system_message.get("description"):
        desc = system_message.get("description", "")
        sentences = desc.split(". ")
        if sentences:
            return ". ".join(sentences[:2]) + (
                "." if not sentences[0].endswith(".") else ""
            )

    # Fall back to instructions
    instructions = system_message.get("instructions", "")
    sentences = instructions.split(". ")
    if sentences:
        description = ". ".join(sentences[:2])
        if not description.endswith("."):
            description += "."
        return description

    return "AI-powered financial analysis assistant."


def format_team_details(team):
    """Format team details in a natural language way"""
    name = team.get("name", "Unknown Team")
    description = team.get("description", "")
    model_info = team.get("model", {})
    members = team.get("members", [])
    system_message = team.get("system_message", {})
    instructions = system_message.get("instructions", "")

    details = f"""
### 👥 About {name}

{description}

---

### 🤖 Model Information

This team is powered by **{model_info.get('name', 'Unknown')}** using the **{model_info.get('provider', 'Unknown')}** provider.

---

### 👨‍👩‍👧‍👦 Team Members ({len(members)} members)

"""

    for member in members:
        member_name = member.get("name", "Unknown")
        member_role = member.get("role", "Member")
        member_desc = member.get("description", "")
        # Truncate description
        if len(member_desc) > 150:
            member_desc = member_desc[:150] + "..."
        details += f"**{member_name}** - _{member_role}_\n"
        details += f"> {member_desc}\n\n"

    details += f"""
---

### 📋 Team Instructions

{instructions}
"""

    return details


def format_agent_details(agent):
    """Format agent details in a natural language way"""
    name = agent.get("name", "Unknown Agent")
    role = agent.get("role", "Agent")
    model_info = agent.get("model", {})
    tools_info = agent.get("tools", {}).get("tools", [])
    system_message = agent.get("system_message", {})
    instructions = system_message.get("instructions", "")

    details = f"""
### 👤 About {name}

**{name}** serves as a **{role}** in the Financial Advisor system.

---

### 🤖 Model Information

This agent is powered by **{model_info.get('name', 'Unknown')}** using the **{model_info.get('provider', 'Unknown')}** provider.

---

### 🛠️ Available Tools

{name} has access to **{len(tools_info)} tools** to help with analysis:

"""

    for i, tool in enumerate(tools_info, 1):
        tool_name = tool.get("name", "Unknown")
        tool_desc = tool.get("description", "No description available")
        details += f"**{i}. {tool_name}**\n"
        if tool_desc:
            details += f"   _{tool_desc}_\n\n"
        else:
            details += "\n"

    details += f"""
---

### 📋 Instructions

{instructions}
"""

    return details


@st.dialog("Configuration", width="large")
def show_config_dialog(item, item_id, item_type):
    """Show configuration in a dialog"""
    item_name = item.get("name", "Unknown")

    st.markdown(f"### ⚙️ {item_name} Configuration")
    st.markdown("---")

    config_json = json.dumps(item, indent=2)
    st.code(config_json, language="json")

    if st.button("Close", key=f"close_config_{item_type}_{item_id}"):
        st.session_state[f"show_config_{item_type}_{item_id}"] = False
        st.rerun()


@st.dialog("Details", width="large")
def show_details_dialog(item, item_id, item_type):
    """Show details in a natural language dialog"""
    if item_type == "team":
        details = format_team_details(item)
    else:
        details = format_agent_details(item)

    st.markdown(details)

    if st.button("Close", key=f"close_details_{item_type}_{item_id}"):
        st.session_state[f"show_details_{item_type}_{item_id}"] = False
        st.rerun()


def render_team_card(team, col):
    """Render a single team card"""
    with col:
        team_id = team.get("id", "unknown")
        team_name = team.get("name", "Unknown Team")
        description = extract_description(team)
        model_info = team.get("model", {})
        members = team.get("members", [])

        # Card HTML
        st.markdown(
            f"""
        <div class="card team-card">
            <div class="card-name">{team_name}</div>
            <div class="card-role team-role">TEAM</div>
            <div class="card-description">{description}</div>
            <div>
                <span class="id-badge team-id-badge">@{team_id}</span>
                <span class="members-badge">{len(members)} members</span>
            </div>
            <div class="card-footer">
                Model: {model_info.get('provider', 'Unknown')}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button(
                "💬 Chat", key=f"chat_team_{team_id}", use_container_width=True
            ):
                # Clear session when selecting a new agent/team from library
                st.session_state["messages"] = []
                st.session_state["chat_started"] = False
                st.session_state["session_id"] = str(uuid.uuid4())
                st.session_state["current_agent_for_session"] = team_id
                st.session_state["selected_agent_id"] = team_id
                st.session_state["selected_type"] = "team"
                st.switch_page("app.py")

        with col2:
            if st.button(
                "⚙️ Config", key=f"config_team_{team_id}", use_container_width=True
            ):
                st.session_state[f"show_config_team_{team_id}"] = True

        with col3:
            if st.button(
                "📄 Details", key=f"details_team_{team_id}", use_container_width=True
            ):
                st.session_state[f"show_details_team_{team_id}"] = True

        # Show dialogs
        if st.session_state.get(f"show_config_team_{team_id}", False):
            show_config_dialog(team, team_id, "team")

        if st.session_state.get(f"show_details_team_{team_id}", False):
            show_details_dialog(team, team_id, "team")


def render_agent_card(agent, col):
    """Render a single agent card"""
    with col:
        agent_id = agent.get("id", "unknown")
        agent_name = agent.get("name", "Unknown Agent")
        agent_role = agent.get("role", "Agent")
        description = extract_description(agent)
        model_info = agent.get("model", {})
        tools = agent.get("tools", {}).get("tools", [])

        # Card HTML
        st.markdown(
            f"""
        <div class="card agent-card">
            <div class="card-name">{agent_name}</div>
            <div class="card-role">{agent_role}</div>
            <div class="card-description">{description}</div>
            <div class="id-badge agent-id-badge">@{agent_id}</div>
            <div class="card-footer">
                Model: {model_info.get('provider', 'Unknown')} • Tools: {len(tools)}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button(
                "💬 Chat", key=f"chat_agent_{agent_id}", use_container_width=True
            ):
                # Clear session when selecting a new agent/team from library
                st.session_state["messages"] = []
                st.session_state["chat_started"] = False
                st.session_state["session_id"] = str(uuid.uuid4())
                st.session_state["current_agent_for_session"] = agent_id
                st.session_state["selected_agent_id"] = agent_id
                st.session_state["selected_type"] = "agent"
                st.switch_page("app.py")

        with col2:
            if st.button(
                "⚙️ Config", key=f"config_agent_{agent_id}", use_container_width=True
            ):
                st.session_state[f"show_config_agent_{agent_id}"] = True

        with col3:
            if st.button(
                "📄 Details", key=f"details_agent_{agent_id}", use_container_width=True
            ):
                st.session_state[f"show_details_agent_{agent_id}"] = True

        # Show dialogs
        if st.session_state.get(f"show_config_agent_{agent_id}", False):
            show_config_dialog(agent, agent_id, "agent")

        if st.session_state.get(f"show_details_agent_{agent_id}", False):
            show_details_dialog(agent, agent_id, "agent")


def main():
    # Header
    st.markdown('<h1 class="main-title">📚 Library</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">// BROWSE TEAMS AND AGENTS</p>', unsafe_allow_html=True
    )

    # Back to chat button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Chat", use_container_width=True):
            st.switch_page("app.py")

    st.markdown("---")

    # Fetch data
    with st.spinner("Loading..."):
        teams = fetch_teams()
        agents = fetch_agents()

    if teams is None and agents is None:
        st.markdown(
            """
        <div class="error-card">
            <div class="error-text">
                ⚠️ Unable to connect to the service.<br>
                Please ensure the API is running at <code>http://localhost:5111</code>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("🔄 Retry Connection"):
            st.rerun()
        return

    # Store in session state
    st.session_state["teams_list"] = teams or []
    st.session_state["agents_list"] = agents or []

    # === TEAMS SECTION ===
    if teams:
        st.markdown(
            """
        <div class="section-header">👥 Teams</div>
        <div class="section-subheader">Collaborative agent teams for comprehensive analysis</div>
        """,
            unsafe_allow_html=True,
        )

        for i in range(0, len(teams), 3):
            row_teams = teams[i : i + 3]
            cols = st.columns(3)
            for j, team in enumerate(row_teams):
                render_team_card(team, cols[j])

        st.markdown("<br>", unsafe_allow_html=True)

    # === AGENTS SECTION ===
    if agents:
        st.markdown(
            """
        <div class="section-header">🤖 Agents</div>
        <div class="section-subheader">Individual specialized agents for specific tasks</div>
        """,
            unsafe_allow_html=True,
        )

        for i in range(0, len(agents), 3):
            row_agents = agents[i : i + 3]
            cols = st.columns(3)
            for j, agent in enumerate(row_agents):
                render_agent_card(agent, cols[j])

    if not teams and not agents:
        st.info("No teams or agents available.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #64748b; font-family: 'Space Mono', monospace; font-size: 0.7rem; padding: 1rem;">
        Click "Chat" to start a conversation with a team or agent
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
