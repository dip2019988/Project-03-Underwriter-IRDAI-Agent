# Conversational Life Insurance Underwriter & IRDAI-Compliant Advisory Agent

## Overview

An AI-powered conversational life insurance underwriting and advisory platform built for Indian insurance products.

The solution supports:

•	Financial underwriting
•	HLV (Human Life Value) calculations
•	Medical risk assessment
•	ULIP illustrations
•	IRDAI regulatory guidance
•	Long-term conversational memory
•	PII redaction
•	Anti-mis-selling guardrails
•	MCP tool integration
•	Vector RAG using FAISS

---

# Features

## Privacy & Security

Implemented using Microsoft Presidio.

Supported Redaction:

•	PAN
•	Aadhaar
•	Bank Account
•	IFSC
•	Phone Number
•	Email
•	Salary
•	Employer Information
•	Residential Address

Reversible token mapping is maintained and restored only in final outputs.

---

## Regulatory & Product Knowledge RAG

Implemented using:

•	FAISS
•	OpenAI Embeddings
•	Chunking
•	Hybrid Retrieval
•	Source Attribution

Supports:

•	IRDAI Guidelines
•	Section 45
•	ULIP Rules
•	Term Insurance Rules
•	Underwriting Guidelines

---

## Long-Term Memory

Implemented using:

•	Mem0
•	Qdrant

Stores:

•	Dependents
•	Family History
•	Smoking Habits
•	Medical Conditions
•	Financial Goals
•	Risk Preferences

Memory is reused during future underwriting assessments.

---

## MCP Services

### BMI Service

Calculates:

•	BMI
•	BMI Risk Category


### HLV Service

Calculates:

- Human Life Value
- Financial Eligibility

### Premium Service

Calculates:

- Premium Recommendation
- Loading Factors

---

## Guardrails

Implemented:

•	Prompt Injection Detection
•	Tobacco Concealment Detection
•	Anti-Mis-Selling Controls
•	Guaranteed Returns Blocking
•	IRDAI Compliance Validation
•	Structured Output Validation

---

## ULIP Illustration Engine

Supports:

•	4% Illustration
•	8% Illustration

Mandatory Disclosure:

```text
Market-linked returns are not guaranteed.

# Architecture
 ↓
Streamlit / FastAPI
 ↓
Input Guardrails
    • Presidio
    • Prompt Injection Detection
    • Compliance Validation
 ↓
LangGraph Workflow
    • Profile Extraction
    • Risk Assessment
    • Medical Follow-up
    • Intent Classification
 ↓
MCP Services
    • BMI
    • HLV
    • Premium
 ↓
RAG Layer
    • FAISS
    • Embeddings
    • Hybrid Search
    • Source Attribution
 ↓
Recommendation Generator
 ↓
Confidence Evaluator
 ↓
Human Review
 ↓
Output Rehydration
 ↓
Final Response

## Supporting Services

•	Mem0 + Qdrant
•	Redis
•	FAISS
•	OpenAI
•	LangSmith
•	Docker
•	GitHub Actions

# Technology Stack
Layer	Technology
Workflow	LangGraph
LLM	OpenAI
Memory	Mem0
Vector Store	FAISS
Embeddings	OpenAI Embeddings
Guardrails	Guardrails + Pydantic
Privacy	Presidio
Backend	FastAPI
UI	Streamlit
Observability	LangSmith
CI/CD	GitHub Actions
Containerization	Docker


# Installation
## Clone Repository
git clone <repo-url>
cd Project-03-Underwriter-IRDAI-Agent
## Create Virtual Environment
python -m venv venv
Activate:
Linux / Mac:
source venv/bin/activate
Windows:
venv\Scripts\activate
## Install Dependencies
pip install -r requirements.txt
________________________________________
# Environment Configuration
## Create .env
OPENAI_API_KEY=your_openai_key
 
OPENAI_MODEL_NAME=gpt-4o-mini
 
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Insurance-Underwriting-Agent
 
JWT_SECRET_KEY=your_secret
 
REDIS_HOST=localhost
REDIS_PORT=6379
 
MEM0_API_KEY=
 
MCP_BMI_URL=http://localhost:8001
MCP_HLV_URL=http://localhost:8002
MCP_PREMIUM_URL=http://localhost:8003
________________________________________
# Running MCP Services
## Terminal 1
python mcp_services/bmi_service.py
 
## Terminal 2
python mcp_services/hlv_service.py
## Terminal 3
python mcp_services/premium_service.py
## Health Check
http://localhost:8001/health
http://localhost:8002/health
http://localhost:8003/health
________________________________________
# Running Streamlit
streamlit run streamlit_app.py
________________________________________
# Running FastAPI
uvicorn api_server:app --reload
Swagger:
http://localhost:8000/docs
________________________________________
# Usage Examples
## Example 1 – HLV Underwriting
### Input
I am 34 years old.
Income 18 lakh.
Need 2.5 crore cover.
### Output
Maximum Eligible HLV: ₹3.6 crore
 
Decision:
STANDARD_RATES
________________________________________
## Example 2 – Smoker Classification
### Input
I smoke 1-2 cigarettes every weekend.
Income 18 lakh.
Need 2.5 crore cover.
### Output
Tobacco Classification:
SMOKER
 
Decision:
PREMIUM_LOADING_REQUIRED
________________________________________
## Example 3 – Family Cardiac Risk
### Input
My father underwent bypass surgery at age 52.
### Output
Family Risk:
MODERATE_CARDIAC
________________________________________
## Example 4 – Asthma Follow-Up
### Input
I have asthma.
### Output
Follow-up Questions:
 
- Hospitalization history?
- Inhaler usage?
- Steroid medication?
________________________________________
## Example 5 – ULIP Illustration
### Input
Show ULIP returns illustration for 10 lakh investment.
### Output
Investment Amount:
₹10,00,000
 
4% Illustration:
₹10,40,000
 
8% Illustration:
₹10,80,000
 
Market-linked returns are not guaranteed.
 
________________________________________
## Example 6 – Section 45
### Input
What is Section 45 of the Insurance Act?
### Output
Policies cannot normally be questioned
after 3 years except in cases of fraud.
 
Sources:
•	IRDAI-001
---
Running Tests
Run Entire Regression Suite
pytest tests/ -v
Current Status
36 Tests Passing
________________________________________
Major Automated Tests
Privacy
PAN
Aadhaar
Bank Account
Phone
IFSC
Underwriting
HLV
BMI
Premium
Smoker Logic
Memory
Memory Storage
Memory Retrieval
Memory Reuse
RAG
Section 45 Retrieval
ULIP Retrieval
Source Attribution
 
________________________________________
GitHub Actions CI/CD
Pipeline:
Code Quality & Linting
↓
Unit & Security Guardrail Tests
↓
Application Startup Validation
↓
LangSmith Evaluation
↓
Docker Build & Push
↓
Deployment Verification
________________________________________
Docker
Build
docker build -t insurance-underwriter .
Run
docker compose up --build
________________________________________
Docker Hub
Image
docker pull <dockerhub-username>/insurance-underwriter:latest
________________________________________
Functional Certification
Completed:
14 Certification Packs
Including:
•   PII Redaction
•   HLV
•   Smoker Classification
•   Family History
•   Asthma Follow-Up
•   BMI
•   Occupational Risk
•   Memory
•   ULIP
•   Mixed Intent
•   Anti-Mis-Selling
•   Section 45
•   End-to-End Underwriting
________________________________________
Future Enhancements
•   Incremental FAISS Updates
•   Direct PDF Uploads
•   Advanced Retrieval Ranking
•   Multi-Level Underwriter Review Workflow
•   Expanded Regulatory Corpus
•   Additional Actuarial Rules
________________________________________
Author
Project 03
Conversational Life Insurance Underwriter & IRDAI-Compliant Advisory Agent

