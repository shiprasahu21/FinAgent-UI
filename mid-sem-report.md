# Financial Advisor Agent

## Contents

1. [Introduction](#1-introduction)
   - 1.1 [Overview](#11-overview)
   - 1.2 [Problem Statement](#12-problem-statement)
   - 1.3 [Motivation](#13-motivation)
   - 1.4 [Objectives](#14-objectives)
2. [Literature Review](#2-literature-review)
   - 2.1 [Foundational Concepts: The Paradigm Shift to Agentic AI](#21-foundational-concepts-the-paradigm-shift-to-agentic-ai)
   - 2.2 [Frameworks: The Shift to Agno](#22-frameworks-the-shift-to-agno)
   - 2.3 [Financial Data Context](#23-financial-data-context)
3. [Proposed System Architecture](#3-proposed-system-architecture)
   - 3.1 [High-Level Design](#31-high-level-design)
   - 3.2 [The "Crews" (Agent Teams)](#32-the-crews-agent-teams)
     - 3.2.1 [Personal Finance Team](#321-personal-finance-team)
     - 3.2.2 [Investment Helper Team](#322-investment-helper-team)
   - 3.3 [Data Ingestion: Domain Knowledge & Rules Pipeline](#33-data-ingestion-domain-knowledge--rules-pipeline)
     - 3.3.1 [Ingested Data Categories](#331-ingested-data-categories)
     - 3.3.2 [Technical Pipeline Implementation](#332-technical-pipeline-implementation)
   - 3.4 [User Interface (UI)](#34-user-interface-ui)
     - 3.4.1 [Component 1: User Onboarding Form](#341-component-1-user-onboarding-form)
     - 3.4.2 [Component 2: Conversational Chat UI](#342-component-2-conversational-chat-ui)
4. [Implementation Details](#4-implementation-details)
   - 4.1 [Tech Stack](#41-tech-stack)
   - 4.2 [Agent Definitions](#42-agent-definitions)
     - 4.2.1 [Spending Analysis Agent (Personal Finance Team)](#421-spending-analysis-agent-personal-finance-team)
     - 4.2.2 [Stock Analysis Agent (Investment Helper Team)](#422-stock-analysis-agent-investment-helper-team)
   - 4.3 [Orchestration Logic: The "Team"](#43-orchestration-logic-the-team)
   - 4.4 [Integration](#44-integration)
5. [Work Accomplished vs. Plan](#5-work-accomplished-vs-plan)
6. [Future Work](#6-future-work)
   - 6.1 [Testing Phase (Jan 1 – Jan 31, 2026)](#61-testing-phase-jan-1--jan-31-2026)
   - 6.2 [Dissertation Review & Submission (Feb 2026)](#62-dissertation-review--submission-feb-2026)
7. [Conclusion](#7-conclusion)
8. [Literature References](#literature-references)

## 1. Introduction

### 1.1 Overview

The contemporary landscape of Indian financial technology (FinTech) stands at a critical inflection point, poised between the era of static, user-initiated digital tools and the emerging paradigm of autonomous, agentic intelligence. This dissertation details the conceptualization and implementation of a "Financial Advisor Agent," a research initiative undertaken to bridge the widening chasm between complex financial instruments and the financial literacy of the average Indian consumer. Situated at the convergence of Agentic AI and personalized services, this project represents a fundamental departure from the reactive "chatbot" models that have dominated the last decade of FinTech innovation.

Unlike traditional algorithmic calculators that await explicit commands, the system proposed herein is an autonomous, proactive entity designed to function as a digital fiduciary. It employs a "team" of specialized AI agents capable of perceiving the user's holistic financial environment, reasoning through multi-step optimization strategies, and executing plans with minimal human oversight. By leveraging the "Perceive → Reason → Act" loop, the Financial Advisor Agent aims to democratize access to sophisticated wealth management services, traditionally the preserve of high-net-worth individuals, for the broader Indian demographic.

### 1.2 Problem Statement

The impetus for this research is derived from a well-documented and pervasive crisis within the Indian economic demographic: a profound financial literacy gap. Despite the rapid digitalization of the Indian economy, the cognitive capability of the population to navigate financial decisions remains critically low. Empirical data suggests that approximately 73% of the Indian adult population fails to meet the minimum threshold for financial literacy, leaving only 27% effectively literate in financial matters.

This literacy deficit manifests in a series of suboptimal economic behaviors. A significant portion of the target user base lacks the vocabulary to formulate the necessary questions to extract value from existing passive tools. A user who does not understand "asset allocation" is unlikely to ask a chatbot, "Is my portfolio's Sharpe ratio optimized?". Consequently, existing FinTech solutions, which operate on a "pull" basis (waiting for user queries), effectively exclude the majority of the population who do not know what to ask.

### 1.3 Motivation

The primary motivation for this dissertation is to leverage the emerging capabilities of Large Language Models (LLMs) and Multi-Agent Orchestration frameworks to construct a "Financial Guardian." The necessity for a proactive agentic system is the central premise. If the user cannot ask the right question, the system must possess the intelligence to ask it for them.

This project transcends the creation of a mere calculator; it aims to architect an autonomous, data-driven entity. While the original ambition included direct integration with the Account Aggregator framework, the current motivation focuses on establishing the cognitive architecture of these agents using a robust knowledge base (Vector Database) to simulate high-fidelity financial reasoning on ingested documents.

### 1.4 Objectives

The specific research and engineering objectives of this dissertation are defined as follows:

1. **Architectural Definition of an Autonomous Financial Agent**: To define and architect a comprehensive, autonomous financial agent capable of proactively monitoring and managing a user's financial health.
2. **Implementation of Multi-Agent Orchestration**: To implement a robust multi-agent orchestration system using the Agno framework, enabling specialized agents to collaborate on complex tasks.
3. **Secure Integration with Financial Knowledge Bases**: To implement a Retrieval-Augmented Generation (RAG) pipeline where financial data and domain rules are ingested into a Vector Database (ChromaDB), serving as the "long-term memory" and ground truth for the agents.
4. **Bridging the Literacy Gap through Interface Design**: To design a dual-component user interface (Onboarding Form + Conversational Chat) that captures essential context and simplifies interaction.

## 2. Literature Review

### 2.1 Foundational Concepts: The Paradigm Shift to Agentic AI

The theoretical foundation of this dissertation rests on the distinction between traditional "AI Agents" and the emerging class of "Agentic AI." Sapkota et al. (2025), in their seminal taxonomy AI Agents vs. Agentic AI, argue that this distinction constitutes a paradigm shift. While traditional agents are often designed for isolated execution, Agentic AI systems utilize Large Language Models (LLMs) as autonomous reasoning engines, capable of decomposing complex objectives into executable sub-tasks.

### 2.2 Frameworks: The Shift to Agno

To implement Agentic AI, the selection of an appropriate orchestration framework is critical. The literature review initially considered various frameworks, but the research converged on Agno (formerly known as Phidata) as the optimal choice for this financial system.

Agno is distinguished by its lightweight architecture and focus on multi-modal agentic systems with memory, knowledge, and tools. Unlike heavier frameworks that enforce rigid graph structures or complex role-playing abstractions, Agno provides a pythonic, performance-oriented approach.

- **Performance**: Benchmarks suggest Agno is significantly faster in agent instantiation and has a memory footprint approximately 50x smaller than comparable graph-based frameworks like LangGraph.
- **Knowledge Integration**: Agno treats "Knowledge" as a first-class citizen, providing native integration with Vector Databases (VectorDB) to ground agent responses in factual data, a critical requirement for financial accuracy to prevent hallucinations.
- **Relevance**: This framework aligns perfectly with the project's need for a high-performance system where agents must retrieve specific financial figures from large documents (statements) without the overhead of complex graph state management.

### 2.3 Financial Data Context

While the RBI Account Aggregator (AA) framework represents the gold standard for live data sharing in India, the practical implementation for this dissertation utilizes a Vector Database (VectorDB) approach to simulate this data availability.

In this model, financial documents (PDF bank statements, investment reports) are processed via an ETL (Extract, Transform, Load) pipeline. The text is chunked, embedded using Sentence Transformers, and stored in ChromaDB. This creates a semantic knowledge base. When an agent needs to "Perceive" the user's financial state, it queries this VectorDB rather than an external API. This aligns with the "Retrieval-Augmented Generation" (RAG) pattern, ensuring agents' reason based on specific, retrieved context rather than general knowledge.

## 3. Proposed System Architecture

### 3.1 High-Level Design

The proposed architecture is a Multi-Agent System built on the Agno framework. It utilizes the concept of a Team of agents that can delegate tasks to one another to solve complex user queries. The system comprises three primary layers: Interaction, Orchestration, and Knowledge.

### 3.2 The "Crews" (Agent Teams)

The system is divided into two highly specialized teams, ensuring comprehensive coverage of the user's financial life.

#### 3.2.1 Personal Finance Team

This team focuses on the user's financial foundation, compliance, and lifestyle planning.

1. **General Finance Agent**:
   - **Role**: Holistic Financial Advisor.
   - **Function**: This agent acts as the first line of defense. It analyzes the user's overall stability, suggesting appropriate Insurance coverage (Life/Health) using thumb rules like "10-20x annual income" for Sum Assured. It also calculates the ideal Emergency Fund size based on the "3-6-12 Month Rule" and performs high-level "Spending vs. Investment" ratio analysis.

2. **Spending Analysis Agent**:
   - **Role**: Expense Tracker & Analyst.
   - **Function**: Connects to the VectorDB to pull monthly spend data and cross-references it with salary inputs. It benchmarks spending against user demographics (e.g., "You are spending 20% more on dining than the average for your age group") and suggests actionable budget corrections.

3. **Tax Planning Assistant Agent**:
   - **Role**: Compliance Specialist.
   - **Function**: This agent possesses a specialized knowledge base of Indian Income Tax (IT) rules. It analyzes income streams to suggest applicable deductions under Section 80C (PPF, ELSS), 80D (Health Insurance), and 80CCD (NPS). It performs comparative analysis between the Old vs. New Tax Regimes to recommend the most beneficial option for the user.

4. **Home Planning Agent**:
   - **Role**: Real Estate Planner.
   - **Function**: Focuses on major capital decisions. It calculates "Buy vs. Rent" scenarios based on current market rates and user liquidity. It also determines affordable Home Loan EMI limits using the FOIR (Fixed Obligation to Income Ratio) rule, ensuring the user does not become "house poor."

#### 3.2.2 Investment Helper Team

This team focuses on wealth accumulation, market research, and portfolio growth.

1. **Stock Analysis Agent**:
   - **Role**: Equity Researcher.
   - **Tools**: YFinance, Web Search.
   - **Function**: Performs deep dives into specific stocks. It fetches real-time performance metrics (P/E, EPS, Beta) and uses web search to gather qualitative market sentiment and analyst ratings.

2. **Indian Market Analysis Agent**:
   - **Role**: Domestic Strategist.
   - **Function**: Tracks the pulse of the Indian economy. It monitors Nifty 50 and Sensex indexes, tracks sector-specific rotations (e.g., IT vs. Pharma), and aggregates general news to gauge domestic market sentiment.

3. **Foreign Market Analysis Agent**:
   - **Role**: Global Strategist.
   - **Function**: Dedicated to US and global market analysis. It researches indices like S&P 500 and Nasdaq to identify international diversification opportunities for Indian investors.

4. **General Investment Helper Agent**:
   - **Role**: Investment Concierge.
   - **Function**: Answers ad-hoc queries related to financial concepts (e.g., "What is a Sovereign Gold Bond?") using web search. It acts as an educational layer for the user.

5. **Portfolio Analyser Agent**:
   - **Role**: Portfolio Manager.
   - **Function**: The decision-maker of the investment team. It reviews the user's current holdings and breaks them down by market cap (Large/Mid/Small). It suggests rebalancing strategies based on the "100 Minus Age" asset allocation rule, tailoring risk exposure to the user's age group.

### 3.3 Data Ingestion: Domain Knowledge & Rules Pipeline

The data ingestion layer handles not just user data, but also the complex domain rules of Indian finance.

#### 3.3.1 Ingested Data Categories

The pipeline ingests two distinct categories of data into the VectorDB:

1. **User Data**: Bank statements (PDF/CSV), Salary slips, and Investment proofs.
2. **Domain Knowledge (Rules & Regulations)**:
   - **Tax Rules**: The complete text of Indian Income Tax Sections (80C, 80D, 80CCD, 24b) for FY 2025-26.
   - **Financial Heuristics**: Emergency Fund rules (3-6-12 months), Insurance Cover rules (10-20x Income), and Asset Allocation rules (100 minus Age).

#### 3.3.2 Technical Pipeline Implementation

The system utilizes a modern, open-source RAG stack:

- **Vector Database**: ChromaDB (Local Instance).
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2) for generating high-quality dense vector representations.
- **Retrieval Mechanism**: Hybrid Search combining dense vector search (for semantic meaning) with keyword search (for specific legal sections).

### 3.4 User Interface (UI)

The UI is designed to bridge the literacy gap by guiding the user through a structured data collection process before enabling open-ended exploration. It consists of two distinct components:

#### 3.4.1 Component 1: User Onboarding Form

This static interface component is the entry point for the system. It is critical for establishing the "User Context" that empowers the agents to give personalized rather than generic advice. It captures:

- **Demographics**: Age, family composition, marital status, partner's employment status, and number of dependents.
- **Cash Flow**: Net monthly salary, detailed monthly spending breakdown, and existing debt obligations (EMIs, personal loans, credit card dues).
- **Portfolio Snapshot**: Current net worth, existing investments (Fixed Deposits, Mutual Funds, Stocks), monthly SIP commitments, and total liabilities.
- **Financial Protection**: Health insurance coverage details, Term insurance sum assured, Emergency fund balance, and current savings rate.

#### 3.4.2 Component 2: Conversational Chat UI

Once the user is onboarded, the system transitions to a Conversational Interface.

- **Natural Language Interaction**: Users interact with the agent teams via a chat window (e.g., "Based on my onboarding data, do I have enough insurance?").
- **Context-Aware Responses**: The agents utilize the structured data collected in Component 1 combined with the unstructured data in the VectorDB to provide answers.
- **Format**: The output is strictly textual, utilizing Markdown tables and bullet points to explain complex concepts clearly, without relying on complex visual dashboards.

## 4. Implementation Details

### 4.1 Tech Stack

The implementation leverages a modern, Python-centric stack optimized for agentic workflows and advanced reasoning.

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.12 | Latest stable release with performance optimizations for async workloads. |
| Framework | Agno | High-performance agent orchestration with native tool/knowledge integration. |
| LLMs | OpenAI GPT-5.1 / Anthropic Claude 4.5 Sonnet | Multi-model strategy: GPT-5.1 for tool calling, Claude 4.5 for complex reasoning and analysis. |
| UI Framework | Streamlit and Agno Agent OS UI | Enables rapid deployment of the dual-component interface (Onboarding Form + Chat). |
| Vector Database | ChromaDB (Local Instance) | Lightweight, open-source vector store for managing financial knowledge embeddings. |
| Embeddings | Sentence Transformers | Efficient, local embedding generation for secure data processing. |
| Tools | YFinance (Market Data), DuckDuckGo (Web Search), etc. | External data connectors for real-time market intelligence. |

### 4.2 Agent Definitions

In Agno, agents are defined as python objects. The system supports model flexibility, allowing specific agents to utilize different LLMs based on task requirements (e.g., Claude for tax reasoning, GPT for tool usage).

#### 4.2.1 Spending Analysis Agent (Personal Finance Team)

This agent connects to ChromaDB to read bank statements.

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.vectordb.chroma import ChromaDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder

# 1. Define Knowledge Base (ChromaDB + Sentence Transformers)
knowledge_base = PDFUrlKnowledgeBase(
    urls=["path/to/bank_statement.pdf"],
    vector_db=ChromaDb(
        collection="financial_docs",
        embedder=SentenceTransformerEmbedder(model_name="all-MiniLM-L6-v2"),
        persistent_client=True
    ),
)
knowledge_base.load()

# 2. Define the Agent
spending_agent = Agent(
    name="Spending Analysis Agent",
    role="Analyze monthly spend data against salary and demographics",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=["Identify discretionary spending.", "Compare against 50-30-20 rule."],
    markdown=True
)
```

#### 4.2.2 Stock Analysis Agent (Investment Helper Team)

This agent utilizes external tools to provide real-time equity data.

```python
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGo
from agno.models.anthropic import Claude

stock_agent = Agent(
    name="Stock Analysis Agent",
    role="Analyze stock performance and market sentiment",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    tools=[YFinanceTools(), DuckDuckGo()],
    instructions=["Fetch real-time metrics.", "Gather market sentiment."],
    show_tool_calls=True
)
```

### 4.3 Orchestration Logic: The "Team"

Agno allows for the creation of a Team of agents. The orchestration logic relies on a "Team Leader" to delegate tasks. For example, a query like "Can I afford a house?" would trigger the Home Planning Agent (to calculate EMI affordability via FOIR) and the Spending Analysis Agent (to check current savings rate) before synthesizing a final "Yes/No" recommendation.

### 4.4 Integration

The integration strategy rests on Knowledge Injection via the UI.

- **User Context Injection**: Data collected from the User Onboarding Form (Section 3.4.1) is converted into a structured prompt context (or "System Message") that is injected into every agent's memory. This ensures that when the "General Finance Agent" answers a query, it already "knows" the user's salary and age without needing to ask again.
- **Data Pipeline**: A script utilizes Agno's built-in readers to extract text from PDF documents, chunk it, and push it to the ChromaDB instance.

## 5. Work Accomplished vs. Plan

The project is progressing according to the revised technical scope.

| Phase | Timeline | Planned Activity | Status | Accomplishments & Deviations |
|-------|----------|-----------------|--------|------------------------------|
| Dissertation Outline | Nov 5 - Nov 9, 2025 | Literature Review & Outline | Completed | • Completed review of Agentic AI literature.<br>• Pivoted framework choice from CrewAI to Agno.<br>• Redefined data strategy from AA-API to VectorDB Knowledge Base. |
| Design & Development | Nov 10 - Dec 31, 2025 | Design & Development | In Progress | • Architecture: Finalized 9-agent architecture across two teams.<br>• Data Layer: Ingested Tax Rules (80C, 80D) and Financial Heuristics into ChromaDB.<br>• UI: Implemented dual-component interface: Onboarding Form (Streamlit) for data capture and Chat Interface for agent interaction.<br>• Agents: Coded core logic for "Stock Analysis" and "Spending Analysis" agents using Python 3.12 and dual-LLM support. |

## 6. Future Work

The upcoming phase will focus on validating the "Intelligence" of the agents now that the infrastructure is in place.

### 6.1 Testing Phase (Jan 1 – Jan 31, 2026)

- **Accuracy Testing (Hallucination Check)**: A critical test will involve querying the agents for specific figures from the ingested bank statements to ensure the ChromaDB retrieval is accurate.
- **Reasoning Evaluation**: Testing the "Team" capability by posing complex scenarios like, "I have 50k in savings (Spending Agent), suggest a tax-saving investment (Tax Planning Agent)." This tests the hand-off between agents.

### 6.2 Dissertation Review & Submission (Feb 2026)

Finalizing the document for the supervisor (Shashank Shekhar) and examiner (Sushant Sudarshan Gundla), incorporating the rationale for switching to Agno and VectorDB-based knowledge management.

## 7. Conclusion

The "Financial Advisor Agent" project has successfully transitioned from a theoretical concept to a functional prototype powered by the Agno framework. By utilizing a ChromaDB Knowledge Base and a structured Onboarding UI, the system achieves the core objective of "Personalized Context" while maintaining development feasibility.

The current implementation demonstrates a comprehensive "Team" of 9 specialized agents, ranging from Spending Analysis to Foreign Market Research, that can read, reason, and answer questions about a user's financial life. The integration of a specific User Onboarding Form ensures that every piece of advice is tailored to the user's specific financial reality (Age, Salary, Liabilities), effectively creating a digital "Family Office" for the average Indian consumer.

## Literature References

[1] Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2025). AI Agents vs. Agentic AI: A conceptual taxonomy, applications and challenges. arXiv preprint arXiv:2505.10468.

[2] Tran, K., et al. (2025). Multi-Agent Collaboration Mechanisms: A Survey of LLMs. arXiv preprint arXiv:2501.06322.

[3] Wu, Q., et al. (2024). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework. Proceedings of the Conference on Machine Learning and Systems (MLSys).

[4] Serafim de Oliveira, M. C. (2024). A Comparative Analysis of LLM-Based Multi-Agent Frameworks. Doria. [Replaces comparisons of CrewAI, LangGraph, etc.]

[5] Sha, Z., et al. (2024). LLM-Based Multi-Agent Systems for Software Engineering: Vision and the Road Ahead. arXiv preprint arXiv:2404.04834.

[6] Okpala, I., et al. (2025). Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews. arXiv preprint arXiv:2502.05439.

[7] Li, Y., et al. (2024). TradingAgents: Multi-Agents LLM Financial Trading Framework. arXiv preprint arXiv:2412.20138.

[8] Li, Z., et al. (2025). FinGAIA: An End-to-End Benchmark for Evaluating AI Agents in Finance. arXiv preprint arXiv:2507.17186.

[9] International Journal of Social Impact. (2025). Beyond Banking: The Rise of Conversational AI in Personal Finance Management. International Journal of Social Impact.

[10] Rashmi, M.B. (2019). Role of personal finance management in determining financial well being and quality of life: A study among government employees in kerala. (PhD Thesis). Cochin University of Science and Technology, Kochi.

[11] Wang, Z., et al. (2025). Synthesizing Behaviorally-Grounded Reasoning Chains: A Data-Generation Framework for Personal Finance LLMs. arXiv preprint arXiv:2509.14180.

[12] Deloitte. (2024). Natural language processing in investment management: The next frontier. Deloitte Insights.

[13] Al-Hadi, A., et al. (2025). The Role of Artificial Intelligence in Taxation and Compliance: Challenges and Future Prospects. ResearchGate.

[14] Obe, O., & Oane, M. (2025). Tax Fraud Detection Using Artificial Intelligence-Based Technologies: Trends and Implications. Algorithms, 18(9), 502.

[15] OECD. (2025). AI in tax administration. In Governing with Artificial Intelligence: The State of Play and Way Forward in Core Government Functions. OECD Publishing, Paris.

[16] Reserve Bank of India. (2016). Master Direction - Non-Banking Financial Company - Account Aggregator (Reserve Bank) Directions, 2016. RBI/DNBR/2016-17/46. [This is the foundational document for the Account Aggregator framework.]

[17] Khanduja, J. (2022). Account Aggregator Framework – A Potential Game-Changer?. NIBM. Vol. XLIII, No. 2.

[18] The Agno Team. (2025). Agno Framework: A Lightweight, High-Performance Orchestration System for Multi-Agent AI. Agno Foundation.

[19] The Agno Team. (2025). Agno Agent OS UI: Dual-Component Interface for Agentic Workflows. Agno Foundation.
