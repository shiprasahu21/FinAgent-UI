"""
Financial Advisor Agent - Main Chat Application
"""

import streamlit as st
import requests
import re
import uuid
from config.config import (
    APP_NAME,
    AGENTS_ENDPOINT,
    TEAMS_ENDPOINT,
    AGENT_RUN_ENDPOINT,
    TEAM_RUN_ENDPOINT,
)
from utils.database import (
    get_all_users,
    get_user_profile,
    format_user_profile_for_agent,
)

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_agent_id" not in st.session_state:
    st.session_state.selected_agent_id = None
if "selected_type" not in st.session_state:
    st.session_state.selected_type = None  # "agent" or "team"
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "agents_list" not in st.session_state:
    st.session_state.agents_list = []
if "teams_list" not in st.session_state:
    st.session_state.teams_list = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "current_agent_for_session" not in st.session_state:
    st.session_state.current_agent_for_session = None
if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = None
if "active_user_name" not in st.session_state:
    st.session_state.active_user_name = None


def clear_session():
    """
    Clear the current chat session.
    Resets messages and generates a new session_id.
    Called when:
    - User clicks "New Chat" button
    - User returns to home screen
    - User selects a different agent/team
    """
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_started = False
    st.session_state.current_agent_for_session = None


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
        font-size: 3.5rem;
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
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* Agent tag styling */
    .agent-tag {
        display: inline-block;
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    /* Team tag styling */
    .team-tag {
        display: inline-block;
        background: linear-gradient(135deg, #f472b6 0%, #fb7185 100%);
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    /* Selected label - small, above input */
    .selected-agent-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .selected-agent-label .agent-pill {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .selected-agent-label .team-pill {
        background: linear-gradient(135deg, #f472b6 0%, #fb7185 100%);
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .selected-agent-label .item-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        color: #94a3b8;
    }
    
    .selected-agent-label .type-badge {
        font-family: 'Space Mono', monospace;
        font-size: 0.6rem;
        color: #64748b;
        background: rgba(100, 116, 139, 0.2);
        padding: 0.1rem 0.4rem;
        border-radius: 3px;
        text-transform: uppercase;
    }
    
    /* Message styling */
    .message-container {
        margin-bottom: 1.5rem !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        border-radius: 20px 20px 4px 20px !important;
        margin-left: 20% !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }
    
    .agent-message {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #f1f5f9 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 20px 20px 20px 4px !important;
        margin-right: 20% !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Assistant message container wrapper */
    .assistant-message-wrapper {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 16px 16px 16px 4px;
        padding: 1rem 1.25rem;
        margin-right: 10%;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .assistant-message-wrapper p,
    .assistant-message-wrapper li,
    .assistant-message-wrapper span {
        color: #e2e8f0 !important;
    }
    
    .assistant-message-wrapper h1,
    .assistant-message-wrapper h2,
    .assistant-message-wrapper h3,
    .assistant-message-wrapper h4,
    .assistant-message-wrapper h5,
    .assistant-message-wrapper h6 {
        color: #00d4ff !important;
    }
    
    .assistant-message-wrapper code {
        background: rgba(0, 0, 0, 0.4) !important;
        color: #a78bfa !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
    
    .assistant-message-wrapper pre {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .assistant-message-wrapper a {
        color: #7c3aed !important;
    }
    
    .assistant-message-wrapper strong {
        color: #f472b6 !important;
    }
    
    .message-header {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem !important;
        color: #64748b !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }
    
    .user-header {
        text-align: right !important;
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Hint text */
    .hint-text {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        color: #64748b;
        text-align: center;
        margin-top: 1rem;
    }
    
    .hint-highlight {
        color: #7c3aed;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        border: none;
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        padding: 0.8rem 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b;
    }
    
    /* Tab hint styling */
    .tab-hint {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #64748b;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    
    /* Suggestion category */
    .suggestion-category {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
        padding-left: 0.2rem;
    }
    
    /* Token info styling - very small */
    .token-info {
        font-family: 'Space Mono', monospace;
        font-size: 0.55rem;
        color: #475569;
        margin-top: 0.4rem;
        text-align: left;
        letter-spacing: 0.02em;
    }
    
    /* Spinner/loading styling - more visible */
    div[data-testid="stSpinner"] {
        background: rgba(124, 58, 237, 0.1);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    div[data-testid="stSpinner"] > div {
        color: #e2e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stSpinner"] svg {
        stroke: #a78bfa !important;
    }
    
    /* Chat input styling - dark theme */
    [data-testid="stChatInput"],
    .stChatInput {
        background: transparent !important;
    }
    
    [data-testid="stChatInput"] > div,
    .stChatInput > div {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(100, 116, 139, 0.4) !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stChatInput"] textarea,
    .stChatInput textarea {
        background: transparent !important;
        color: #f1f5f9 !important;
        font-family: 'DM Sans', sans-serif !important;
        caret-color: #a78bfa !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder,
    .stChatInput textarea::placeholder {
        color: #64748b !important;
    }
    
    [data-testid="stChatInput"] button,
    .stChatInput button {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stChatInput"] button:hover,
    .stChatInput button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%) !important;
    }
    
    /* Target the bottom chat input container specifically */
    [data-testid="stBottom"] {
        background: linear-gradient(180deg, transparent 0%, rgba(15, 15, 26, 0.95) 20%) !important;
    }
    
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }
    
    /* Override any white backgrounds in chat input area */
    [data-testid="stChatInput"] * {
        background-color: transparent !important;
    }
    
    [data-testid="stChatInput"] > div:first-child {
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Force message styling in Streamlit markdown containers */
    div[data-testid="stMarkdown"] .message-container {
        margin-bottom: 1.5rem !important;
    }
    
    div[data-testid="stMarkdown"] .user-message {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
        color: #ffffff !important;
        padding: 1rem 1.5rem !important;
        border-radius: 20px 20px 4px 20px !important;
        margin-left: 20% !important;
    }
    
    div[data-testid="stMarkdown"] .agent-message {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #f1f5f9 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 20px 20px 20px 4px !important;
        margin-right: 20% !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[data-testid="stMarkdown"] .assistant-message-wrapper {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Form submit button styling */
    .stForm [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        min-height: 42px !important;
    }
    
    .stForm [data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%) !important;
    }
    
    /* User selector styling */
    .user-selector-container {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    .user-info {
        flex: 1;
    }
    
    .user-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #f1f5f9;
    }
    
    .user-id-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #64748b;
    }
    
    .no-user-badge {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #94a3b8;
        background: rgba(100, 116, 139, 0.2);
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
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
        agents = response.json()
        st.session_state.agents_list = agents
        return agents
    except requests.exceptions.RequestException:
        return st.session_state.agents_list if st.session_state.agents_list else []


def fetch_teams():
    """Fetch teams from the API"""
    try:
        response = requests.get(TEAMS_ENDPOINT, timeout=None)
        response.raise_for_status()
        teams = response.json()
        st.session_state.teams_list = teams
        return teams
    except requests.exceptions.RequestException:
        return st.session_state.teams_list if st.session_state.teams_list else []


def build_message_with_history(current_message: str, max_history: int = 5) -> str:
    """
    Build a structured message with conversation history and user profile.

    Args:
        current_message: The current user query
        max_history: Maximum number of historical messages to include (default 5)

    Returns:
        Formatted string with user profile, current query and conversation history
    """
    # Get the last N messages from history (excluding the current message we just added)
    messages = st.session_state.messages

    # If the current message was already added, exclude it from history
    if (
        messages
        and messages[-1].get("role") == "user"
        and messages[-1].get("content") == current_message
    ):
        history_messages = messages[:-1]
    else:
        history_messages = messages

    # Get only the last max_history messages
    history_messages = history_messages[-max_history:] if history_messages else []

    # Build the structured message
    structured_message = ""

    # Include user profile if active user is selected
    if st.session_state.active_user_id:
        user_data = get_user_profile(st.session_state.active_user_id)
        if user_data:
            profile_text = format_user_profile_for_agent(user_data)
            if profile_text:
                structured_message += f"USER PROFILE:\n{profile_text}\n\n"

    structured_message += f"CURRENT USER QUERY: {current_message}"

    if history_messages:
        structured_message += "\nHISTORY CONVERSATION:"
        for msg in history_messages:
            role = msg.get("role", "user")
            # Use "you" instead of "assistant" for agent messages
            display_role = "you" if role == "assistant" else role
            content = msg.get("content", "")
            structured_message += f"\n{display_role}: {content}"

    return structured_message


def send_message_to_agent(
    agent_id: str, message: str, item_type: str = "agent"
) -> dict:
    """
    Send a message to an agent or team and get the response.

    Args:
        agent_id: The ID of the agent or team
        message: The message to send
        item_type: Either "agent" or "team"

    Returns:
        dict with 'content' and 'total_tokens' keys, or error info
    """
    try:
        # Build the endpoint URL
        if item_type == "team":
            endpoint = TEAM_RUN_ENDPOINT.format(team_id=agent_id)
        else:
            endpoint = AGENT_RUN_ENDPOINT.format(agent_id=agent_id)

        # Build message with conversation history (last 5 messages)
        structured_message = build_message_with_history(message, max_history=5)

        # Prepare form data
        form_data = {
            "message": structured_message,
            "stream": "false",
            "session_id": st.session_state.session_id,
            "user_id": st.session_state.user_id,
        }

        # Make the request
        response = requests.post(
            endpoint,
            data=form_data,
            headers={"accept": "application/json"},
            timeout=None,  # No timeout - wait indefinitely for response
        )
        response.raise_for_status()

        result = response.json()

        # Extract content and token info
        content = result.get("content", "No response received.")
        metrics = result.get("metrics", {})
        total_tokens = metrics.get("total_tokens", 0)

        return {
            "success": True,
            "content": content,
            "total_tokens": total_tokens,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "content": "⏱️ Request timed out. The agent is taking too long to respond. Please try again.",
            "total_tokens": 0,
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "content": "🔌 Unable to connect to the backend. Please ensure the API is running at http://localhost:5111",
            "total_tokens": 0,
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "content": f"❌ Error communicating with the agent: {str(e)}",
            "total_tokens": 0,
        }


def get_item_by_id(item_id):
    """Get agent or team details by ID"""
    # Check agents first
    for agent in st.session_state.agents_list:
        if agent.get("id") == item_id:
            return agent, "agent"

    # Check teams
    for team in st.session_state.teams_list:
        if team.get("id") == item_id:
            return team, "team"

    return None, None


def parse_agent_from_message(message):
    """Parse @agent-id from message and return (agent_id, remaining_message)"""
    pattern = r"^@([\w-]+)\s*(.*)$"
    match = re.match(pattern, message.strip())
    if match:
        return match.group(1), match.group(2).strip()
    return None, message


def render_user_selector():
    """Render user selection component."""
    users = get_all_users()

    # Create user options
    user_options = ["👤 No User Selected"] + [
        f"{u['name']} ({u['user_id']})" for u in users
    ]

    # Find current selection index
    current_index = 0
    if st.session_state.active_user_id:
        for i, u in enumerate(users):
            if u["user_id"] == st.session_state.active_user_id:
                current_index = i + 1
                break

    col1, col2 = st.columns([4, 1])

    with col1:
        selected = st.selectbox(
            "Active User Profile",
            user_options,
            index=current_index,
            key="user_profile_selector",
            label_visibility="collapsed",
        )

    with col2:
        if st.button("👤 Profile", key="goto_profile", use_container_width=True):
            st.switch_page("pages/2_User_Profile.py")

    # Update session state based on selection
    if selected == "👤 No User Selected":
        if st.session_state.active_user_id is not None:
            st.session_state.active_user_id = None
            st.session_state.active_user_name = None
    else:
        # Extract user_id from selection
        selected_user_id = selected.split("(")[-1].rstrip(")")
        if selected_user_id != st.session_state.active_user_id:
            st.session_state.active_user_id = selected_user_id
            # Find the user name
            for u in users:
                if u["user_id"] == selected_user_id:
                    st.session_state.active_user_name = u["name"]
                    break

    # Show active user indicator
    if st.session_state.active_user_id:
        st.markdown(
            f"""
            <div class="user-selector-container">
                <div class="user-avatar">👤</div>
                <div class="user-info">
                    <div class="user-name">{st.session_state.active_user_name}</div>
                    <div class="user-id-label">Profile active • Financial data will be included</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="user-selector-container" style="border-color: rgba(100, 116, 139, 0.3);">
                <span class="no-user-badge">No profile selected • Create one for personalized advice</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_message(role, content, responder_name=None, total_tokens=None):
    """Render a chat message"""
    if role == "user":
        st.markdown(
            f"""
        <div class="message-container">
            <div class="message-header user-header">You</div>
            <div class="user-message">{content}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        header = responder_name or "Assistant"

        # Render header
        st.markdown(
            f'<div class="message-header">🤖 {header}</div>',
            unsafe_allow_html=True,
        )

        # Wrap assistant message in styled container
        st.markdown(
            f'<div class="assistant-message-wrapper">{content}</div>',
            unsafe_allow_html=True,
        )

        # Render token info if available
        if total_tokens and total_tokens > 0:
            st.markdown(
                f'<div class="token-info">tokens: {total_tokens:,}</div>',
                unsafe_allow_html=True,
            )


def clear_chat_messages():
    """
    Clear chat messages but keep the current agent selected.
    Generates a new session_id for fresh context.
    """
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())


def render_chat_view():
    """Render the full chat view"""
    item, item_type = get_item_by_id(st.session_state.selected_agent_id)
    item_name = item.get("name", "Assistant") if item else "Assistant"

    # Determine tag class based on type
    tag_class = "team-tag" if item_type == "team" else "agent-tag"

    # Header with info and new chat button
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

    with col1:
        if st.button("← Back", key="go_back"):
            clear_session()
            st.session_state.selected_agent_id = None
            st.session_state.selected_type = None
            st.rerun()

    with col2:
        st.markdown(
            f"""
        <div style="text-align: center;">
            <span class="{tag_class}">@{st.session_state.selected_agent_id}</span>
            <span style="color: #f1f5f9; font-family: 'DM Sans', sans-serif; font-size: 1.1rem; margin-left: 0.5rem;">{item_name}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            clear_chat_messages()
            st.rerun()

    with col4:
        if st.button("📚 Library", key="browse_library_chat"):
            st.switch_page("pages/1_Agents_Library.py")

    # User selector in chat view
    render_user_selector()

    st.markdown("---")

    # Chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_message(
                msg["role"],
                msg["content"],
                item_name if msg["role"] == "assistant" else None,
                msg.get("total_tokens") if msg["role"] == "assistant" else None,
            )

    # Chat input - uses st.chat_input for Enter key support and auto-clear
    st.markdown("---")

    user_input = st.chat_input("Type your message...", key="chat_input")

    if user_input:
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show user message immediately
        render_message("user", user_input)

        # Show thinking indicator and call the backend
        with st.spinner("🤔 Thinking..."):
            response = send_message_to_agent(
                st.session_state.selected_agent_id,
                user_input,
                st.session_state.selected_type or "agent",
            )

        # Add agent response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response["content"],
                "total_tokens": response["total_tokens"],
            }
        )

        # Show agent response immediately
        render_message(
            "assistant", response["content"], item_name, response["total_tokens"]
        )

        # Rerun to clean up state
        st.rerun()


def render_home_view():
    """Render the home view with centered chat input"""
    # Clear session when returning to home screen (no agent selected and not in chat)
    if not st.session_state.chat_started and st.session_state.messages:
        clear_session()

    # Spacer for vertical centering
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)

    # Title
    st.markdown(
        '<h1 class="main-title">💼 Financial Advisor Agent</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">// AI-POWERED FINANCIAL ANALYSIS</p>',
        unsafe_allow_html=True,
    )

    # Fetch data if not loaded
    if not st.session_state.agents_list:
        fetch_agents()
    if not st.session_state.teams_list:
        fetch_teams()

    # Wider center column for chat input
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # User selector
        render_user_selector()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Show selected item label ABOVE the input
        if st.session_state.selected_agent_id:
            item, item_type = get_item_by_id(st.session_state.selected_agent_id)
            item_name = item.get("name", "") if item else ""
            pill_class = "team-pill" if item_type == "team" else "agent-pill"
            type_label = "team" if item_type == "team" else "agent"

            # Small label row above input
            label_col, clear_col = st.columns([8, 1])
            with label_col:
                st.markdown(
                    f"""
                    <div class="selected-agent-label">
                        <span class="{pill_class}">@{st.session_state.selected_agent_id}</span>
                        <span class="item-name">{item_name}</span>
                        <span class="type-badge">{type_label}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with clear_col:
                if st.button("✕", key="clear_selection", help="Clear selection"):
                    st.session_state.selected_agent_id = None
                    st.session_state.selected_type = None
                    st.rerun()

        # Initialize search state
        if "search_term" not in st.session_state:
            st.session_state.search_term = ""

        # Chat input
        placeholder = (
            "Type your message..."
            if st.session_state.selected_agent_id
            else "Type @name to search or @agent-id message to send"
        )

        user_input = st.chat_input(placeholder, key="home_chat_input")

        # Handle input
        if user_input:
            if st.session_state.selected_agent_id:
                # Check if agent changed - clear session if different agent selected
                if (
                    st.session_state.current_agent_for_session
                    != st.session_state.selected_agent_id
                ):
                    clear_session()
                    st.session_state.current_agent_for_session = (
                        st.session_state.selected_agent_id
                    )

                # Agent already selected - send message directly
                st.session_state.messages.append(
                    {"role": "user", "content": user_input}
                )

                with st.spinner("🤔 Thinking..."):
                    response = send_message_to_agent(
                        st.session_state.selected_agent_id,
                        user_input,
                        st.session_state.selected_type or "agent",
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response["content"],
                        "total_tokens": response["total_tokens"],
                    }
                )
                st.session_state.chat_started = True
                st.rerun()
            elif user_input.startswith("@"):
                # Parse @agent-id from message
                item_id, message = parse_agent_from_message(user_input)

                if item_id and message:
                    # Has @agent-id AND a message - try to send
                    item, item_type = get_item_by_id(item_id)
                    if item:
                        # Clear session if starting with a new agent
                        if st.session_state.current_agent_for_session != item_id:
                            clear_session()
                        st.session_state.selected_agent_id = item_id
                        st.session_state.selected_type = item_type
                        st.session_state.current_agent_for_session = item_id
                        st.session_state.messages.append(
                            {"role": "user", "content": message}
                        )

                        with st.spinner("🤔 Thinking..."):
                            response = send_message_to_agent(
                                item_id, message, item_type
                            )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": response["content"],
                                "total_tokens": response["total_tokens"],
                            }
                        )
                        st.session_state.chat_started = True
                        st.session_state.search_term = ""
                        st.rerun()
                    else:
                        # Exact agent not found - use as search term
                        st.session_state.search_term = item_id
                        st.rerun()
                else:
                    # Just @something with no message - it's a search
                    search = user_input[1:].strip()
                    st.session_state.search_term = search if search else ""
                    st.rerun()
            else:
                st.warning("Type @agent-id to search or select from the Library.")

        # Show search results
        if st.session_state.search_term and not st.session_state.selected_agent_id:
            search_term = st.session_state.search_term.lower()

            # Search teams
            matching_teams = [
                t
                for t in st.session_state.teams_list
                if search_term in t.get("id", "").lower()
                or search_term in t.get("name", "").lower()
            ]

            # Search agents
            matching_agents = [
                a
                for a in st.session_state.agents_list
                if search_term in a.get("id", "").lower()
                or search_term in a.get("name", "").lower()
            ]

            if matching_teams or matching_agents:
                st.markdown(
                    f"**Results for '@{st.session_state.search_term}'** — click to select:"
                )

                for team in matching_teams[:3]:
                    team_id = team.get("id", "")
                    team_name = team.get("name", "")
                    if st.button(
                        f"👥 @{team_id} • {team_name}",
                        key=f"r_team_{team_id}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_agent_id = team_id
                        st.session_state.selected_type = "team"
                        st.session_state.search_term = ""
                        st.rerun()

                for agent in matching_agents[:5]:
                    agent_id = agent.get("id", "")
                    agent_name = agent.get("name", "")
                    if st.button(
                        f"🤖 @{agent_id} • {agent_name}",
                        key=f"r_agent_{agent_id}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_agent_id = agent_id
                        st.session_state.selected_type = "agent"
                        st.session_state.search_term = ""
                        st.rerun()

                if st.button("✕ Clear", key="clear_search"):
                    st.session_state.search_term = ""
                    st.rerun()
            else:
                st.warning(f"No results for '@{st.session_state.search_term}'")
                if st.button("✕ Clear", key="clear_search"):
                    st.session_state.search_term = ""
                    st.rerun()

        # Hint text
        st.markdown(
            """
        <p class="hint-text">
            Type <span class="hint-highlight">@name</span> to search agents, or 
            <a href="/Agents_Library" style="color: #7c3aed; text-decoration: none;">browse library</a>
        </p>
        """,
            unsafe_allow_html=True,
        )

        # Browse library button
        if st.button(
            "📚 Browse Library", key="browse_library", use_container_width=True
        ):
            st.switch_page("pages/1_Agents_Library.py")


def main():
    if st.session_state.chat_started and st.session_state.selected_agent_id:
        render_chat_view()
    else:
        render_home_view()


if __name__ == "__main__":
    main()
