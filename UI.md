# Financial Advisor UI - User Guide

An AI-powered financial advisory platform providing personalized guidance through specialized AI agents.

## System Requirements

- **Backend API**: Service running on `http://localhost:5111`
- **Browser**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- **Internet**: Required for AI processing
- **Storage**: Local SQLite database for user profiles

## Quick Start

1. Ensure backend service is running at `http://localhost:5111`
2. Open the application in your web browser
3. Create your profile for personalized advice (optional but recommended)
4. Start chatting with AI agents using `@agent-id` syntax

## Key Features

- Access AI specialists for investment, tax, retirement, insurance, budgeting, and real estate
- Team collaboration for comprehensive analysis
- Local data storage for privacy
- Personalized recommendations based on your financial profile

---

## Interface Overview

### 1. Chat Interface

Start conversations with AI financial advisors:

**Starting a Conversation:**
- Type `@agent-id your question` (e.g., `@tax-planner How can I save tax?`)
- Type `@` to search for agents by partial name
- Click "Browse Library" to see all available agents

**Profile Selection:**
- Select your profile at the top for personalized advice (green border when active)
- Without a profile, agents provide general guidance

**Controls:**
- **Clear Chat**: Start fresh conversation with same agent
- **Back**: Return home and clear session
- **Token Counter**: Shows AI processing usage (informational)

### 2. Agent Library

Browse and select from available AI agents and teams:

**Teams**: Groups of AI agents collaborating for comprehensive analysis (e.g., Investment Team, Personal Finance Team)

**Individual Agents**: Specialists focused on specific tasks (tax, insurance, investment, etc.)

**Card Actions:**
- **Chat**: Start conversation immediately
- **Config**: View JSON configuration
- **Details**: See full description, tools, and capabilities

### 3. User Profile

Store your financial data for personalized recommendations. Agents use this data to provide context-aware advice, accurate calculations, and tailored strategies.

**Profile Management:**
- **Create**: Select "Create New User" → Fill form → Save
- **Load**: Select profile → Load Profile → Edit → Save
- **Delete**: Select profile → Delete button → Confirm

### Profile Sections

#### 1. Personal Information
User ID, Name, Age, Gender, Marital Status, Dependents, City

#### 2. Income & Employment
- Monthly Income (auto-calculates annual)
- Employment Type: Salaried/Self-Employed/Business Owner/Freelancer/Retired/Student
- Job Stability: Stable/Moderate/Unstable
- Industry/Sector

#### 3. Monthly Expenses
Track: Housing, Food, Transportation, Utilities, Healthcare, Education, Entertainment, EMIs, Other
- Auto-calculates total expenses and savings rate
- Color-coded: Green (20%+), Yellow (10-20%), Red (<10%)

#### 4. Insurance Coverage
- Life, Health, and Term Insurance amounts
- Annual premiums
- Auto-calculates adequacy using 10-20x income rule

#### 5. Savings & Investments
Track: Emergency Fund, FDs, Mutual Funds, Stocks, PPF, NPS, EPF, Gold, Real Estate, Other
- Risk Tolerance: Low/Medium/High
- Auto-calculates total portfolio value

#### 6. Tax Planning
- **Section 80C** (₹1.5L limit): PPF, ELSS, Life Insurance, EPF, Home Loan Principal, Tuition, Sukanya Samriddhi
- **Section 80D**: Health insurance premiums (Self/Family: ₹25K/₹50K; Parents: ₹25K/₹50K)
- **Section 80CCD(1B)**: NPS contribution (₹50K additional)
- Visual progress bars show utilization vs. limits

#### 7. Real Estate & Home Planning
- Home Ownership Status: Renting/Own (Fully Paid)/Own (With Loan)/Living with Family
- For Renters: Current rent
- For Homeowners: Property value, loan outstanding, EMI, interest rate, tenure
- Auto-calculates FOIR (Fixed Obligation to Income Ratio) with 40% affordability rule

#### 8. Financial Goals
- Short-term (1-3 years): Emergency fund, vacation, gadgets
- Medium-term (3-7 years): Car, education, wedding
- Long-term (7+ years): Home, children's education, retirement
- Target Retirement Age & Monthly SIP

#### 9. Additional Information
Free-form text for: promotions, relocations, health conditions, inheritance, business plans, family obligations

---

## Using the Platform Effectively

### Profile Best Practices
- Fill all relevant sections for better recommendations
- Update quarterly when financial situation changes
- Be accurate with numbers
- Define clear goals to help agents prioritize advice

### Chatting with Agents
- **Be Specific**: Ask "I want to save ₹10 lakhs in 5 years for a car" instead of "How do I save money?"
- **Select Profile**: Always use your profile for personalized advice
- **Ask Follow-ups**: Agents remember conversation context
- **Try Different Specialists**: Different agents offer different expertise

### Individual Agents vs Teams
- **Use Agents**: Specific questions, quick focused advice, single-domain exploration
- **Use Teams**: Comprehensive planning, multiple perspectives, major financial decisions, coordinated cross-domain advice

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Cannot connect to service | Verify backend runs at `http://localhost:5111`, check firewall |
| Agent not responding | Wait (complex queries take time), verify backend, try simpler query |
| Profile not saving | Ensure User ID and Name are filled, check error messages, try different User ID |
| Search not finding agents | Browse Library for exact agent IDs, search with partial names (`@tax`) |

---

## Privacy & Data

**Local Storage:**
- User profiles: SQLite database (`data/users.db`)
- Chat history: Session memory (cleared on close)

**Data Shared with Backend:**
- Current message
- Last 5 conversation messages
- Active user profile (if selected)

**Privacy:**
- Profile data stays local except during conversations
- No external service access without interaction
- Profiles can be deleted anytime

**Data Retention:**
- Chat history: Session only
- User profiles: Until manually deleted
- No automatic backup (manual export not currently available)

---

## Financial Planning Workflow

1. **Build Profile**: Complete all sections, update quarterly
2. **General Assessment**: Start with teams (e.g., "Personal Finance Team, review my financial situation")
3. **Specific Deep Dives**: Use specialized agents for tax, insurance, investment, retirement planning
4. **Regular Check-ins**: Quarterly profile updates, annual comprehensive reviews

### Sample Questions by Domain

**Investment**: "Create a diversified portfolio for ₹50K monthly investment" | "Rebalance my portfolio"
**Tax**: "Maximize tax savings under 80C" | "NPS vs PPF for tax benefits?" | "Calculate tax liability"
**Insurance**: "Is my coverage adequate?" | "Term vs endowment insurance comparison"
**Retirement**: "Monthly savings needed to retire at 60 with ₹5 crores?" | "Review retirement portfolio"
**Real Estate**: "Buy vs rent analysis for Mumbai" | "Can I afford ₹50L home loan?" | "Real estate vs mutual funds"
**Emergency Fund**: "Optimal emergency fund size?" | "Bank FD vs liquid funds?"

---

## Additional Information

**Keyboard Shortcuts**: Enter (send), @ (search agents), Esc (clear search)

**Updates**: Platform regularly adds new agents, enhanced capabilities, and additional features

**Support**: Check this guide → Verify backend service → Refresh page → Contact administrator

---

## Quick Reference

| Action | Method |
|--------|--------|
| Start conversation | `@agent-id question` |
| Search agents | `@partial-name` |
| Browse library | Click "Browse Library" |
| Create profile | User Profile > Create New User > Save |
| Load/edit profile | Select from dropdown > Load Profile > Edit > Save |
| Delete profile | Select > Delete > Confirm |
| Clear chat | "Clear Chat" button |
| New session | "Back" button |

**Key Terms:**
- **FOIR**: Fixed Obligation to Income Ratio (EMIs as % of income)
- **80C/80D/80CCD**: Indian Income Tax deduction sections
- **SIP**: Systematic Investment Plan (regular monthly investments)
- **Token**: AI processing unit (informational only)

---

The more complete your profile, the better the personalized recommendations. Start by building a comprehensive profile, then explore specialized agents or teams for your financial planning needs.
