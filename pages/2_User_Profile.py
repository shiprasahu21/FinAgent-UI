"""
User Profile Page - Financial Information Form
Collects comprehensive financial data for personalized advice.
"""

import streamlit as st
import uuid
from config.config import APP_NAME
from utils.database import (
    save_user_profile,
    get_user_profile,
    get_all_users,
    delete_user,
)

# Page configuration
st.set_page_config(
    page_title=f"User Profile - {APP_NAME}",
    page_icon="👤",
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
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* Section header */
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(100, 116, 139, 0.2);
    }
    
    .section-subheader {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .success-card {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Form input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(100, 116, 139, 0.3) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }
    
    /* Label styling */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stTextArea > label,
    .stRadio > label,
    .stSlider > label,
    .stCheckbox > label {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    
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
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 8px;
        color: #94a3b8;
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
        color: white !important;
    }
    
    /* User selector card */
    .user-selector-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
    }
    
    .user-badge {
        display: inline-block;
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        color: white;
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-right: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    /* Radio button horizontal layout */
    .stRadio > div {
        flex-direction: row !important;
        gap: 1rem !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_form_state():
    """Initialize form state with default values."""
    defaults = {
        # Personal
        "form_user_id": "",
        "form_name": "",
        "form_age": 30,
        "form_gender": "Male",
        "form_marital_status": "Single",
        "form_dependents": 0,
        "form_city": "",
        # Income
        "form_monthly_income": 50000,
        "form_employment_type": "Salaried",
        "form_job_stability": "Stable",
        "form_industry": "",
        # Expenses
        "form_exp_housing": 15000,
        "form_exp_food": 8000,
        "form_exp_transportation": 5000,
        "form_exp_utilities": 3000,
        "form_exp_healthcare": 2000,
        "form_exp_education": 0,
        "form_exp_entertainment": 3000,
        "form_exp_emi": 0,
        "form_exp_other": 2000,
        # Insurance
        "form_life_insurance": 0,
        "form_health_insurance": 0,
        "form_term_insurance": 0,
        "form_health_premium": 0,
        "form_life_premium": 0,
        # Savings
        "form_emergency_fund": 0,
        "form_fixed_deposits": 0,
        "form_mutual_funds": 0,
        "form_stocks": 0,
        "form_ppf": 0,
        "form_nps": 0,
        "form_epf": 0,
        "form_gold": 0,
        "form_real_estate_value": 0,
        "form_other_investments": 0,
        "form_risk_tolerance": "Medium",
        # Tax - 80C
        "form_ppf_contribution": 0,
        "form_elss_investment": 0,
        "form_life_premium_80c": 0,
        "form_epf_contribution": 0,
        "form_home_loan_principal": 0,
        "form_children_tuition": 0,
        "form_sukanya_samriddhi": 0,
        # Tax - 80D
        "form_health_premium_self": 0,
        "form_health_premium_parents": 0,
        "form_parents_senior": False,
        # Tax - 80CCD
        "form_nps_contribution": 0,
        "form_employer_nps": 0,
        # Real Estate
        "form_ownership_status": "Renting",
        "form_current_rent": 0,
        "form_property_value": 0,
        "form_home_loan_outstanding": 0,
        "form_home_loan_emi": 0,
        "form_loan_interest_rate": 8.5,
        "form_loan_tenure_remaining": 0,
        # Goals
        "form_short_term_goals": "",
        "form_medium_term_goals": "",
        "form_long_term_goals": "",
        "form_retirement_age": 60,
        "form_sip_target": 0,
        # Additional
        "form_additional_info": "",
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_user_to_form(user_data):
    """Load user data into form fields."""
    if not user_data:
        return
    
    profile = user_data.get("profile_data", {})
    
    # Personal
    personal = profile.get("personal", {})
    st.session_state.form_user_id = user_data.get("user_id", "")
    st.session_state.form_name = user_data.get("name", "")
    st.session_state.form_age = personal.get("age", 30)
    st.session_state.form_gender = personal.get("gender", "Male")
    st.session_state.form_marital_status = personal.get("marital_status", "Single")
    st.session_state.form_dependents = personal.get("dependents", 0)
    st.session_state.form_city = personal.get("city", "")
    
    # Income
    income = profile.get("income", {})
    st.session_state.form_monthly_income = income.get("monthly_income", 50000)
    st.session_state.form_employment_type = income.get("employment_type", "Salaried")
    st.session_state.form_job_stability = income.get("job_stability", "Stable")
    st.session_state.form_industry = income.get("industry", "")
    
    # Expenses
    expenses = profile.get("expenses", {})
    st.session_state.form_exp_housing = expenses.get("housing", 15000)
    st.session_state.form_exp_food = expenses.get("food", 8000)
    st.session_state.form_exp_transportation = expenses.get("transportation", 5000)
    st.session_state.form_exp_utilities = expenses.get("utilities", 3000)
    st.session_state.form_exp_healthcare = expenses.get("healthcare", 2000)
    st.session_state.form_exp_education = expenses.get("education", 0)
    st.session_state.form_exp_entertainment = expenses.get("entertainment", 3000)
    st.session_state.form_exp_emi = expenses.get("emi_payments", 0)
    st.session_state.form_exp_other = expenses.get("other", 2000)
    
    # Insurance
    insurance = profile.get("insurance", {})
    st.session_state.form_life_insurance = insurance.get("life_insurance", 0)
    st.session_state.form_health_insurance = insurance.get("health_insurance", 0)
    st.session_state.form_term_insurance = insurance.get("term_insurance", 0)
    st.session_state.form_health_premium = insurance.get("health_premium", 0)
    st.session_state.form_life_premium = insurance.get("life_premium", 0)
    
    # Savings
    savings = profile.get("savings", {})
    st.session_state.form_emergency_fund = savings.get("emergency_fund", 0)
    st.session_state.form_fixed_deposits = savings.get("fixed_deposits", 0)
    st.session_state.form_mutual_funds = savings.get("mutual_funds", 0)
    st.session_state.form_stocks = savings.get("stocks", 0)
    st.session_state.form_ppf = savings.get("ppf", 0)
    st.session_state.form_nps = savings.get("nps", 0)
    st.session_state.form_epf = savings.get("epf", 0)
    st.session_state.form_gold = savings.get("gold", 0)
    st.session_state.form_real_estate_value = savings.get("real_estate", 0)
    st.session_state.form_other_investments = savings.get("other", 0)
    st.session_state.form_risk_tolerance = savings.get("risk_tolerance", "Medium")
    
    # Tax
    tax = profile.get("tax", {})
    st.session_state.form_ppf_contribution = tax.get("ppf_contribution", 0)
    st.session_state.form_elss_investment = tax.get("elss_investment", 0)
    st.session_state.form_life_premium_80c = tax.get("life_insurance_premium", 0)
    st.session_state.form_epf_contribution = tax.get("epf_contribution", 0)
    st.session_state.form_home_loan_principal = tax.get("home_loan_principal", 0)
    st.session_state.form_children_tuition = tax.get("children_tuition", 0)
    st.session_state.form_sukanya_samriddhi = tax.get("sukanya_samriddhi", 0)
    st.session_state.form_health_premium_self = tax.get("health_premium_self", 0)
    st.session_state.form_health_premium_parents = tax.get("health_premium_parents", 0)
    st.session_state.form_parents_senior = tax.get("parents_senior", False)
    st.session_state.form_nps_contribution = tax.get("nps_contribution", 0)
    st.session_state.form_employer_nps = tax.get("employer_nps", 0)
    
    # Real Estate
    real_estate = profile.get("real_estate", {})
    st.session_state.form_ownership_status = real_estate.get("ownership_status", "Renting")
    st.session_state.form_current_rent = real_estate.get("current_rent", 0)
    st.session_state.form_property_value = real_estate.get("property_value", 0)
    st.session_state.form_home_loan_outstanding = real_estate.get("home_loan_outstanding", 0)
    st.session_state.form_home_loan_emi = real_estate.get("home_loan_emi", 0)
    st.session_state.form_loan_interest_rate = real_estate.get("loan_interest_rate", 8.5)
    st.session_state.form_loan_tenure_remaining = real_estate.get("loan_tenure_remaining", 0)
    
    # Goals
    goals = profile.get("goals", {})
    st.session_state.form_short_term_goals = goals.get("short_term", "")
    st.session_state.form_medium_term_goals = goals.get("medium_term", "")
    st.session_state.form_long_term_goals = goals.get("long_term", "")
    st.session_state.form_retirement_age = goals.get("retirement_age", 60)
    st.session_state.form_sip_target = goals.get("sip_target", 0)
    
    # Additional
    st.session_state.form_additional_info = profile.get("additional_info", "")


def collect_form_data():
    """Collect all form data into a structured dictionary."""
    monthly_income = st.session_state.form_monthly_income
    
    return {
        "personal": {
            "age": st.session_state.form_age,
            "gender": st.session_state.form_gender,
            "marital_status": st.session_state.form_marital_status,
            "dependents": st.session_state.form_dependents,
            "city": st.session_state.form_city,
        },
        "income": {
            "monthly_income": monthly_income,
            "annual_income": monthly_income * 12,
            "employment_type": st.session_state.form_employment_type,
            "job_stability": st.session_state.form_job_stability,
            "industry": st.session_state.form_industry,
        },
        "expenses": {
            "housing": st.session_state.form_exp_housing,
            "food": st.session_state.form_exp_food,
            "transportation": st.session_state.form_exp_transportation,
            "utilities": st.session_state.form_exp_utilities,
            "healthcare": st.session_state.form_exp_healthcare,
            "education": st.session_state.form_exp_education,
            "entertainment": st.session_state.form_exp_entertainment,
            "emi_payments": st.session_state.form_exp_emi,
            "other": st.session_state.form_exp_other,
        },
        "insurance": {
            "life_insurance": st.session_state.form_life_insurance,
            "health_insurance": st.session_state.form_health_insurance,
            "term_insurance": st.session_state.form_term_insurance,
            "health_premium": st.session_state.form_health_premium,
            "life_premium": st.session_state.form_life_premium,
        },
        "savings": {
            "emergency_fund": st.session_state.form_emergency_fund,
            "fixed_deposits": st.session_state.form_fixed_deposits,
            "mutual_funds": st.session_state.form_mutual_funds,
            "stocks": st.session_state.form_stocks,
            "ppf": st.session_state.form_ppf,
            "nps": st.session_state.form_nps,
            "epf": st.session_state.form_epf,
            "gold": st.session_state.form_gold,
            "real_estate": st.session_state.form_real_estate_value,
            "other": st.session_state.form_other_investments,
            "risk_tolerance": st.session_state.form_risk_tolerance,
        },
        "tax": {
            "ppf_contribution": st.session_state.form_ppf_contribution,
            "elss_investment": st.session_state.form_elss_investment,
            "life_insurance_premium": st.session_state.form_life_premium_80c,
            "epf_contribution": st.session_state.form_epf_contribution,
            "home_loan_principal": st.session_state.form_home_loan_principal,
            "children_tuition": st.session_state.form_children_tuition,
            "sukanya_samriddhi": st.session_state.form_sukanya_samriddhi,
            "health_premium_self": st.session_state.form_health_premium_self,
            "health_premium_parents": st.session_state.form_health_premium_parents,
            "parents_senior": st.session_state.form_parents_senior,
            "nps_contribution": st.session_state.form_nps_contribution,
            "employer_nps": st.session_state.form_employer_nps,
        },
        "real_estate": {
            "ownership_status": st.session_state.form_ownership_status,
            "current_rent": st.session_state.form_current_rent,
            "property_value": st.session_state.form_property_value,
            "home_loan_outstanding": st.session_state.form_home_loan_outstanding,
            "home_loan_emi": st.session_state.form_home_loan_emi,
            "loan_interest_rate": st.session_state.form_loan_interest_rate,
            "loan_tenure_remaining": st.session_state.form_loan_tenure_remaining,
        },
        "goals": {
            "short_term": st.session_state.form_short_term_goals,
            "medium_term": st.session_state.form_medium_term_goals,
            "long_term": st.session_state.form_long_term_goals,
            "retirement_age": st.session_state.form_retirement_age,
            "sip_target": st.session_state.form_sip_target,
        },
        "additional_info": st.session_state.form_additional_info,
    }


def render_user_selector():
    """Render user selection and management section."""
    st.markdown(
        """
        <div class="user-selector-card">
            <span style="font-family: 'DM Sans', sans-serif; font-size: 1rem; color: #f1f5f9; font-weight: 600;">
                👤 Select or Create User Profile
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    users = get_all_users()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        user_options = ["➕ Create New User"] + [
            f"{u['name']} ({u['user_id']})" for u in users
        ]
        selected = st.selectbox(
            "Select User",
            user_options,
            key="user_selector",
            label_visibility="collapsed",
        )
    
    with col2:
        if selected != "➕ Create New User":
            if st.button("📥 Load Profile", use_container_width=True):
                # Extract user_id from selection
                selected_user_id = selected.split("(")[-1].rstrip(")")
                user_data = get_user_profile(selected_user_id)
                if user_data:
                    load_user_to_form(user_data)
                    st.success(f"Loaded profile for {user_data['name']}")
                    st.rerun()
    
    with col3:
        if selected != "➕ Create New User":
            if st.button("🗑️ Delete", use_container_width=True):
                selected_user_id = selected.split("(")[-1].rstrip(")")
                if delete_user(selected_user_id):
                    st.success("User deleted")
                    # Clear form
                    for key in list(st.session_state.keys()):
                        if key.startswith("form_"):
                            del st.session_state[key]
                    initialize_form_state()
                    st.rerun()


def render_personal_section():
    """Render personal information section."""
    st.markdown(
        '<div class="section-header">👤 Personal Information</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Basic details for personalized recommendations</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input(
            "User ID *",
            key="form_user_id",
            placeholder="e.g., john_doe_123",
            help="Unique identifier for your profile",
        )
        st.text_input(
            "Full Name *",
            key="form_name",
            placeholder="e.g., John Doe",
        )
        st.number_input(
            "Age *",
            min_value=18,
            max_value=100,
            key="form_age",
        )
        st.selectbox(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"],
            key="form_gender",
        )
    
    with col2:
        st.selectbox(
            "Marital Status",
            ["Single", "Married", "Divorced", "Widowed"],
            key="form_marital_status",
        )
        st.number_input(
            "Number of Dependents",
            min_value=0,
            max_value=10,
            key="form_dependents",
            help="Children, elderly parents, etc.",
        )
        st.text_input(
            "City",
            key="form_city",
            placeholder="e.g., Mumbai, Bangalore",
        )


def render_income_section():
    """Render income and employment section."""
    st.markdown(
        '<div class="section-header">💰 Income & Employment</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Your earning capacity and job stability</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input(
            "Monthly Income (₹) *",
            min_value=0,
            max_value=100000000,
            step=5000,
            key="form_monthly_income",
            help="Total monthly take-home salary/income",
        )
        
        annual = st.session_state.form_monthly_income * 12
        st.markdown(
            f'<div style="color: #64748b; font-size: 0.8rem; margin-top: -0.5rem;">Annual Income: ₹{annual:,.0f}</div>',
            unsafe_allow_html=True,
        )
        
        st.selectbox(
            "Employment Type",
            ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Retired", "Student"],
            key="form_employment_type",
        )
    
    with col2:
        st.selectbox(
            "Job Stability",
            ["Stable", "Moderate", "Unstable"],
            key="form_job_stability",
            help="Stable: Govt/PSU/MNC | Moderate: Startup/Contract | Unstable: Freelance",
        )
        st.text_input(
            "Industry/Sector",
            key="form_industry",
            placeholder="e.g., IT, Banking, Healthcare",
        )


def render_expenses_section():
    """Render monthly expenses section."""
    st.markdown(
        '<div class="section-header">📊 Monthly Expenses</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Track your spending across categories (50-30-20 rule analysis)</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input(
            "Housing/Rent (₹)",
            min_value=0,
            step=1000,
            key="form_exp_housing",
        )
        st.number_input(
            "Food & Groceries (₹)",
            min_value=0,
            step=500,
            key="form_exp_food",
        )
        st.number_input(
            "Transportation (₹)",
            min_value=0,
            step=500,
            key="form_exp_transportation",
        )
    
    with col2:
        st.number_input(
            "Utilities (₹)",
            min_value=0,
            step=500,
            key="form_exp_utilities",
            help="Electricity, water, internet, phone",
        )
        st.number_input(
            "Healthcare (₹)",
            min_value=0,
            step=500,
            key="form_exp_healthcare",
        )
        st.number_input(
            "Education (₹)",
            min_value=0,
            step=500,
            key="form_exp_education",
        )
    
    with col3:
        st.number_input(
            "Entertainment (₹)",
            min_value=0,
            step=500,
            key="form_exp_entertainment",
        )
        st.number_input(
            "EMI Payments (₹)",
            min_value=0,
            step=1000,
            key="form_exp_emi",
            help="Car loan, personal loan EMIs",
        )
        st.number_input(
            "Other Expenses (₹)",
            min_value=0,
            step=500,
            key="form_exp_other",
        )
    
    # Total expenses summary
    total_expenses = sum([
        st.session_state.form_exp_housing,
        st.session_state.form_exp_food,
        st.session_state.form_exp_transportation,
        st.session_state.form_exp_utilities,
        st.session_state.form_exp_healthcare,
        st.session_state.form_exp_education,
        st.session_state.form_exp_entertainment,
        st.session_state.form_exp_emi,
        st.session_state.form_exp_other,
    ])
    
    income = st.session_state.form_monthly_income
    savings_rate = ((income - total_expenses) / income * 100) if income > 0 else 0
    
    st.markdown(
        f"""
        <div class="info-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #64748b; font-size: 0.8rem;">Total Monthly Expenses</span><br>
                <span style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600;">₹{total_expenses:,.0f}</span>
            </div>
            <div>
                <span style="color: #64748b; font-size: 0.8rem;">Savings Rate</span><br>
                <span style="color: {'#22c55e' if savings_rate >= 20 else '#eab308' if savings_rate >= 10 else '#ef4444'}; font-size: 1.2rem; font-weight: 600;">{savings_rate:.1f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insurance_section():
    """Render insurance coverage section."""
    st.markdown(
        '<div class="section-header">🛡️ Insurance Coverage</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Protection for you and your family (10-20x income rule)</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input(
            "Life Insurance Sum Assured (₹)",
            min_value=0,
            step=100000,
            key="form_life_insurance",
            help="Total life insurance coverage",
        )
        st.number_input(
            "Health Insurance Coverage (₹)",
            min_value=0,
            step=100000,
            key="form_health_insurance",
            help="Total health insurance sum insured",
        )
        st.number_input(
            "Term Insurance Coverage (₹)",
            min_value=0,
            step=100000,
            key="form_term_insurance",
        )
    
    with col2:
        st.number_input(
            "Annual Health Premium (₹)",
            min_value=0,
            step=1000,
            key="form_health_premium",
        )
        st.number_input(
            "Annual Life/Term Premium (₹)",
            min_value=0,
            step=1000,
            key="form_life_premium",
        )
    
    # Insurance adequacy check
    annual_income = st.session_state.form_monthly_income * 12
    total_life_cover = st.session_state.form_life_insurance + st.session_state.form_term_insurance
    recommended_cover = annual_income * 15  # 15x rule
    
    if annual_income > 0:
        coverage_ratio = total_life_cover / recommended_cover * 100
        st.markdown(
            f"""
            <div class="info-card">
                <span style="color: #64748b; font-size: 0.8rem;">Life Insurance Adequacy (Recommended: 10-20x Annual Income)</span><br>
                <span style="color: {'#22c55e' if coverage_ratio >= 100 else '#eab308' if coverage_ratio >= 50 else '#ef4444'}; font-size: 1rem;">
                    Current: ₹{total_life_cover:,.0f} | Recommended: ₹{recommended_cover:,.0f} ({coverage_ratio:.0f}% of recommended)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_savings_section():
    """Render savings and investments section."""
    st.markdown(
        '<div class="section-header">💵 Savings & Investments</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Your current wealth and investment portfolio</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input(
            "Emergency Fund (₹)",
            min_value=0,
            step=10000,
            key="form_emergency_fund",
            help="3-6-12 months of expenses recommended",
        )
        st.number_input(
            "Fixed Deposits (₹)",
            min_value=0,
            step=10000,
            key="form_fixed_deposits",
        )
        st.number_input(
            "Mutual Funds (₹)",
            min_value=0,
            step=10000,
            key="form_mutual_funds",
        )
        st.number_input(
            "Stocks/Equity (₹)",
            min_value=0,
            step=10000,
            key="form_stocks",
        )
    
    with col2:
        st.number_input(
            "PPF Balance (₹)",
            min_value=0,
            step=10000,
            key="form_ppf",
        )
        st.number_input(
            "NPS Balance (₹)",
            min_value=0,
            step=10000,
            key="form_nps",
        )
        st.number_input(
            "EPF Balance (₹)",
            min_value=0,
            step=10000,
            key="form_epf",
        )
        st.number_input(
            "Gold Value (₹)",
            min_value=0,
            step=10000,
            key="form_gold",
        )
    
    with col3:
        st.number_input(
            "Real Estate Value (₹)",
            min_value=0,
            step=100000,
            key="form_real_estate_value",
            help="Excluding primary residence",
        )
        st.number_input(
            "Other Investments (₹)",
            min_value=0,
            step=10000,
            key="form_other_investments",
        )
        st.selectbox(
            "Risk Tolerance",
            ["Low", "Medium", "High"],
            key="form_risk_tolerance",
            help="Low: Capital protection | Medium: Balanced | High: Growth focused",
        )
    
    # Total portfolio value
    total_portfolio = sum([
        st.session_state.form_emergency_fund,
        st.session_state.form_fixed_deposits,
        st.session_state.form_mutual_funds,
        st.session_state.form_stocks,
        st.session_state.form_ppf,
        st.session_state.form_nps,
        st.session_state.form_epf,
        st.session_state.form_gold,
        st.session_state.form_real_estate_value,
        st.session_state.form_other_investments,
    ])
    
    st.markdown(
        f"""
        <div class="info-card">
            <span style="color: #64748b; font-size: 0.8rem;">Total Portfolio Value</span><br>
            <span style="color: #00d4ff; font-size: 1.5rem; font-weight: 700;">₹{total_portfolio:,.0f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tax_section():
    """Render tax planning section (80C, 80D, 80CCD)."""
    st.markdown(
        '<div class="section-header">📑 Tax Planning</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Deductions under Section 80C, 80D, and 80CCD</div>',
        unsafe_allow_html=True,
    )
    
    # Section 80C
    with st.expander("📋 Section 80C Deductions (Limit: ₹1,50,000)", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input(
                "PPF Contribution (₹/year)",
                min_value=0,
                max_value=150000,
                step=5000,
                key="form_ppf_contribution",
            )
            st.number_input(
                "ELSS Investment (₹/year)",
                min_value=0,
                step=5000,
                key="form_elss_investment",
            )
            st.number_input(
                "Life Insurance Premium (₹/year)",
                min_value=0,
                step=5000,
                key="form_life_premium_80c",
            )
            st.number_input(
                "EPF Contribution (₹/year)",
                min_value=0,
                step=5000,
                key="form_epf_contribution",
            )
        
        with col2:
            st.number_input(
                "Home Loan Principal (₹/year)",
                min_value=0,
                step=5000,
                key="form_home_loan_principal",
            )
            st.number_input(
                "Children's Tuition Fee (₹/year)",
                min_value=0,
                step=5000,
                key="form_children_tuition",
            )
            st.number_input(
                "Sukanya Samriddhi (₹/year)",
                min_value=0,
                step=5000,
                key="form_sukanya_samriddhi",
            )
        
        total_80c = sum([
            st.session_state.form_ppf_contribution,
            st.session_state.form_elss_investment,
            st.session_state.form_life_premium_80c,
            st.session_state.form_epf_contribution,
            st.session_state.form_home_loan_principal,
            st.session_state.form_children_tuition,
            st.session_state.form_sukanya_samriddhi,
        ])
        
        utilized = min(total_80c, 150000)
        remaining = max(0, 150000 - total_80c)
        
        st.progress(min(total_80c / 150000, 1.0))
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; color: #94a3b8; font-size: 0.8rem;">
                <span>Claimed: ₹{utilized:,.0f}</span>
                <span>Remaining: ₹{remaining:,.0f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Section 80D
    with st.expander("🏥 Section 80D - Health Insurance"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input(
                "Self/Family Health Premium (₹/year)",
                min_value=0,
                step=1000,
                key="form_health_premium_self",
                help="Limit: ₹25,000 (₹50,000 if senior citizen)",
            )
        
        with col2:
            st.number_input(
                "Parents Health Premium (₹/year)",
                min_value=0,
                step=1000,
                key="form_health_premium_parents",
                help="Limit: ₹25,000 (₹50,000 if senior citizen)",
            )
            st.checkbox(
                "Parents are Senior Citizens (60+)",
                key="form_parents_senior",
            )
    
    # Section 80CCD
    with st.expander("🏦 Section 80CCD - NPS"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.number_input(
                "NPS Contribution - 80CCD(1B) (₹/year)",
                min_value=0,
                max_value=50000,
                step=5000,
                key="form_nps_contribution",
                help="Additional ₹50,000 deduction beyond 80C",
            )
        
        with col2:
            st.number_input(
                "Employer NPS Contribution (₹/year)",
                min_value=0,
                step=5000,
                key="form_employer_nps",
                help="10% of basic salary (14% for govt employees)",
            )


def render_real_estate_section():
    """Render real estate section."""
    st.markdown(
        '<div class="section-header">🏠 Real Estate & Home Planning</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Buy vs Rent analysis and EMI affordability (FOIR rule)</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox(
            "Home Ownership Status",
            ["Renting", "Own (Fully Paid)", "Own (With Loan)", "Living with Family"],
            key="form_ownership_status",
        )
        
        if st.session_state.form_ownership_status == "Renting":
            st.number_input(
                "Current Monthly Rent (₹)",
                min_value=0,
                step=1000,
                key="form_current_rent",
            )
        
        if st.session_state.form_ownership_status in ["Own (Fully Paid)", "Own (With Loan)"]:
            st.number_input(
                "Property Value (₹)",
                min_value=0,
                step=100000,
                key="form_property_value",
            )
    
    with col2:
        if st.session_state.form_ownership_status == "Own (With Loan)":
            st.number_input(
                "Home Loan Outstanding (₹)",
                min_value=0,
                step=100000,
                key="form_home_loan_outstanding",
            )
            st.number_input(
                "Home Loan EMI (₹/month)",
                min_value=0,
                step=1000,
                key="form_home_loan_emi",
            )
            st.number_input(
                "Loan Interest Rate (%)",
                min_value=0.0,
                max_value=20.0,
                step=0.1,
                key="form_loan_interest_rate",
            )
            st.number_input(
                "Loan Tenure Remaining (months)",
                min_value=0,
                max_value=360,
                step=12,
                key="form_loan_tenure_remaining",
            )
    
    # FOIR Analysis
    monthly_income = st.session_state.form_monthly_income
    total_emi = st.session_state.form_exp_emi + st.session_state.form_home_loan_emi
    
    if monthly_income > 0:
        foir = total_emi / monthly_income * 100
        max_affordable_emi = monthly_income * 0.4  # 40% FOIR rule
        
        st.markdown(
            f"""
            <div class="info-card">
                <span style="color: #64748b; font-size: 0.8rem;">Fixed Obligation to Income Ratio (FOIR)</span><br>
                <span style="color: {'#22c55e' if foir <= 40 else '#eab308' if foir <= 50 else '#ef4444'}; font-size: 1rem;">
                    Current FOIR: {foir:.1f}% | Max Affordable EMI: ₹{max_affordable_emi:,.0f}/month (40% rule)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_goals_section():
    """Render financial goals section."""
    st.markdown(
        '<div class="section-header">🎯 Financial Goals</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Short-term, medium-term, and long-term objectives</div>',
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_area(
            "Short-term Goals (1-3 years)",
            key="form_short_term_goals",
            placeholder="e.g., Emergency fund, vacation, gadget purchase",
            height=80,
        )
        st.text_area(
            "Medium-term Goals (3-7 years)",
            key="form_medium_term_goals",
            placeholder="e.g., Car purchase, higher education, wedding",
            height=80,
        )
    
    with col2:
        st.text_area(
            "Long-term Goals (7+ years)",
            key="form_long_term_goals",
            placeholder="e.g., Home purchase, children's education, retirement",
            height=80,
        )
        st.number_input(
            "Target Retirement Age",
            min_value=40,
            max_value=75,
            key="form_retirement_age",
        )
        st.number_input(
            "Target Monthly SIP (₹)",
            min_value=0,
            step=1000,
            key="form_sip_target",
            help="How much you want to invest monthly",
        )


def render_additional_section():
    """Render additional information section."""
    st.markdown(
        '<div class="section-header">📝 Additional Information</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subheader">Any other details relevant to your financial situation</div>',
        unsafe_allow_html=True,
    )
    
    st.text_area(
        "Additional Notes",
        key="form_additional_info",
        placeholder="Any other information not covered above...\n\nExamples:\n- Expecting promotion/salary hike\n- Planning to relocate\n- Health conditions affecting insurance\n- Inheritance expected\n- Business plans\n- Family financial obligations",
        height=150,
    )


def main():
    # Initialize form state
    initialize_form_state()
    
    # Header
    st.markdown('<h1 class="main-title">👤 User Profile</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">// FINANCIAL INFORMATION FOR PERSONALIZED ADVICE</p>',
        unsafe_allow_html=True,
    )
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("← Back to Chat", use_container_width=True):
                st.switch_page("app.py")
        with nav_col2:
            if st.button("📚 Browse Library", use_container_width=True):
                st.switch_page("pages/1_Agents_Library.py")
    
    st.markdown("---")
    
    # User selector
    render_user_selector()
    
    st.markdown("---")
    
    # Form sections
    render_personal_section()
    render_income_section()
    render_expenses_section()
    render_insurance_section()
    render_savings_section()
    render_tax_section()
    render_real_estate_section()
    render_goals_section()
    render_additional_section()
    
    st.markdown("---")
    
    # Save button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Profile", use_container_width=True, type="primary"):
            user_id = st.session_state.form_user_id.strip()
            name = st.session_state.form_name.strip()
            
            if not user_id:
                st.error("Please enter a User ID")
            elif not name:
                st.error("Please enter your name")
            else:
                profile_data = collect_form_data()
                if save_user_profile(user_id, name, profile_data):
                    st.success(f"✅ Profile saved successfully for {name}!")
                    
                    # Set as active user in session
                    st.session_state.active_user_id = user_id
                    st.session_state.active_user_name = name
                    
                    st.balloons()
                else:
                    st.error("Failed to save profile. Please try again.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; font-family: 'Space Mono', monospace; font-size: 0.7rem; padding: 1rem;">
            Your data is stored locally and used to provide personalized financial advice
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

