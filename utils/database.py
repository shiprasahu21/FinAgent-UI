"""
Database utility for storing user profiles.
Uses SQLite with JSON data storage for flexibility.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, Dict, List, Any

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection, creating the database if needed."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            profile_data TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def save_user_profile(user_id: str, name: str, profile_data: Dict[str, Any]) -> bool:
    """
    Save or update a user profile.
    
    Args:
        user_id: Unique identifier for the user
        name: Display name
        profile_data: Dictionary containing all profile information
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        profile_json = json.dumps(profile_data, ensure_ascii=False)
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute("""
                UPDATE users 
                SET name = ?, profile_data = ?, updated_at = ?
                WHERE user_id = ?
            """, (name, profile_json, now, user_id))
        else:
            cursor.execute("""
                INSERT INTO users (user_id, name, profile_data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, profile_json, now, now))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving user profile: {e}")
        return False


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user profile by ID.
    
    Args:
        user_id: The user's unique identifier
    
    Returns:
        Dictionary with user data or None if not found
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, name, profile_data, created_at, updated_at
            FROM users WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "user_id": row["user_id"],
                "name": row["name"],
                "profile_data": json.loads(row["profile_data"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
        return None
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None


def get_all_users() -> List[Dict[str, Any]]:
    """
    Get all users (basic info only for selection dropdowns).
    
    Returns:
        List of dictionaries with user_id and name
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, name, updated_at
            FROM users
            ORDER BY updated_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {"user_id": row["user_id"], "name": row["name"], "updated_at": row["updated_at"]}
            for row in rows
        ]
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []


def delete_user(user_id: str) -> bool:
    """
    Delete a user profile.
    
    Args:
        user_id: The user's unique identifier
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def format_user_profile_for_agent(user_data: Dict[str, Any]) -> str:
    """
    Format user profile data into a readable string for the agent.
    
    Args:
        user_data: The complete user data dictionary
    
    Returns:
        Formatted string with all profile information
    """
    if not user_data:
        return ""
    
    profile = user_data.get("profile_data", {})
    name = user_data.get("name", "User")
    
    sections = []
    
    # Personal Information
    personal = profile.get("personal", {})
    if personal:
        sections.append(f"""
📋 PERSONAL INFORMATION:
- Name: {name}
- Age: {personal.get('age', 'N/A')} years
- Gender: {personal.get('gender', 'N/A')}
- Marital Status: {personal.get('marital_status', 'N/A')}
- Dependents: {personal.get('dependents', 0)}
- City: {personal.get('city', 'N/A')}
""")
    
    # Income & Employment
    income = profile.get("income", {})
    if income:
        sections.append(f"""
💰 INCOME & EMPLOYMENT:
- Monthly Income: ₹{income.get('monthly_income', 0):,.0f}
- Annual Income: ₹{income.get('annual_income', 0):,.0f}
- Employment Type: {income.get('employment_type', 'N/A')}
- Job Stability: {income.get('job_stability', 'N/A')}
- Industry: {income.get('industry', 'N/A')}
""")
    
    # Monthly Expenses
    expenses = profile.get("expenses", {})
    if expenses:
        total_expenses = sum([
            expenses.get('housing', 0),
            expenses.get('food', 0),
            expenses.get('transportation', 0),
            expenses.get('utilities', 0),
            expenses.get('healthcare', 0),
            expenses.get('education', 0),
            expenses.get('entertainment', 0),
            expenses.get('emi_payments', 0),
            expenses.get('other', 0)
        ])
        sections.append(f"""
📊 MONTHLY EXPENSES (Total: ₹{total_expenses:,.0f}):
- Housing/Rent: ₹{expenses.get('housing', 0):,.0f}
- Food & Groceries: ₹{expenses.get('food', 0):,.0f}
- Transportation: ₹{expenses.get('transportation', 0):,.0f}
- Utilities: ₹{expenses.get('utilities', 0):,.0f}
- Healthcare: ₹{expenses.get('healthcare', 0):,.0f}
- Education: ₹{expenses.get('education', 0):,.0f}
- Entertainment: ₹{expenses.get('entertainment', 0):,.0f}
- EMI Payments: ₹{expenses.get('emi_payments', 0):,.0f}
- Other: ₹{expenses.get('other', 0):,.0f}
""")
    
    # Insurance
    insurance = profile.get("insurance", {})
    if insurance:
        sections.append(f"""
🛡️ INSURANCE:
- Life Insurance Coverage: ₹{insurance.get('life_insurance', 0):,.0f}
- Health Insurance Coverage: ₹{insurance.get('health_insurance', 0):,.0f}
- Term Insurance Coverage: ₹{insurance.get('term_insurance', 0):,.0f}
- Annual Health Premium: ₹{insurance.get('health_premium', 0):,.0f}
- Annual Life Premium: ₹{insurance.get('life_premium', 0):,.0f}
""")
    
    # Savings & Investments
    savings = profile.get("savings", {})
    if savings:
        sections.append(f"""
💵 SAVINGS & INVESTMENTS:
- Emergency Fund: ₹{savings.get('emergency_fund', 0):,.0f}
- Fixed Deposits: ₹{savings.get('fixed_deposits', 0):,.0f}
- Mutual Funds: ₹{savings.get('mutual_funds', 0):,.0f}
- Stocks/Equity: ₹{savings.get('stocks', 0):,.0f}
- PPF Balance: ₹{savings.get('ppf', 0):,.0f}
- NPS Balance: ₹{savings.get('nps', 0):,.0f}
- EPF Balance: ₹{savings.get('epf', 0):,.0f}
- Gold: ₹{savings.get('gold', 0):,.0f}
- Real Estate Value: ₹{savings.get('real_estate', 0):,.0f}
- Other Investments: ₹{savings.get('other', 0):,.0f}
- Risk Tolerance: {savings.get('risk_tolerance', 'N/A')}
""")
    
    # Tax Planning (80C, 80D, 80CCD)
    tax = profile.get("tax", {})
    if tax:
        total_80c = sum([
            tax.get('ppf_contribution', 0),
            tax.get('elss_investment', 0),
            tax.get('life_insurance_premium', 0),
            tax.get('epf_contribution', 0),
            tax.get('home_loan_principal', 0),
            tax.get('children_tuition', 0),
            tax.get('sukanya_samriddhi', 0)
        ])
        sections.append(f"""
📑 TAX PLANNING:
Section 80C (Total: ₹{min(total_80c, 150000):,.0f} / ₹1,50,000):
- PPF Contribution: ₹{tax.get('ppf_contribution', 0):,.0f}
- ELSS Investment: ₹{tax.get('elss_investment', 0):,.0f}
- Life Insurance Premium: ₹{tax.get('life_insurance_premium', 0):,.0f}
- EPF Contribution: ₹{tax.get('epf_contribution', 0):,.0f}
- Home Loan Principal: ₹{tax.get('home_loan_principal', 0):,.0f}
- Children's Tuition: ₹{tax.get('children_tuition', 0):,.0f}
- Sukanya Samriddhi: ₹{tax.get('sukanya_samriddhi', 0):,.0f}

Section 80D (Health Insurance):
- Self/Family Premium: ₹{tax.get('health_premium_self', 0):,.0f}
- Parents Premium: ₹{tax.get('health_premium_parents', 0):,.0f}
- Parents are Senior Citizens: {tax.get('parents_senior', False)}

Section 80CCD (NPS):
- NPS Contribution (80CCD 1B): ₹{tax.get('nps_contribution', 0):,.0f}
- Employer NPS Contribution: ₹{tax.get('employer_nps', 0):,.0f}
""")
    
    # Real Estate
    real_estate = profile.get("real_estate", {})
    if real_estate:
        sections.append(f"""
🏠 REAL ESTATE:
- Home Ownership: {real_estate.get('ownership_status', 'N/A')}
- Current Rent: ₹{real_estate.get('current_rent', 0):,.0f}/month
- Property Value: ₹{real_estate.get('property_value', 0):,.0f}
- Home Loan Outstanding: ₹{real_estate.get('home_loan_outstanding', 0):,.0f}
- Home Loan EMI: ₹{real_estate.get('home_loan_emi', 0):,.0f}
- Home Loan Interest Rate: {real_estate.get('loan_interest_rate', 0)}%
- Loan Tenure Remaining: {real_estate.get('loan_tenure_remaining', 0)} months
""")
    
    # Goals
    goals = profile.get("goals", {})
    if goals:
        sections.append(f"""
🎯 FINANCIAL GOALS:
- Short-term Goals (1-3 years): {goals.get('short_term', 'N/A')}
- Medium-term Goals (3-7 years): {goals.get('medium_term', 'N/A')}
- Long-term Goals (7+ years): {goals.get('long_term', 'N/A')}
- Target Retirement Age: {goals.get('retirement_age', 60)}
- Monthly SIP Target: ₹{goals.get('sip_target', 0):,.0f}
""")
    
    # Additional Information
    additional = profile.get("additional_info", "")
    if additional:
        sections.append(f"""
📝 ADDITIONAL INFORMATION:
{additional}
""")
    
    return "\n".join(sections)


# Initialize database on module import
init_database()

