# Submission: Hospital AI Agent for ED Congestion and Scheduling

## Overview

Our project targets the urgent problem of emergency department (ED) congestion and nurse staffing shortages in Taiwan.  
By leveraging **Amazon Bedrock AgentCore**, we built an AI agent that can triage incoming requests, plan a workflow, call hospital systems (for example bed‑availability APIs and scheduling services) and generate actionable reports for staff.

## Problem

Taiwan’s EDs experience unprecedented overcrowding.  
Research shows that the root causes include a **shortage of nurses**, **insufficient inpatient beds**, **misallocated bed resources** and **lack of real‑time coordination**【35929458720361†L166-L178】【603959311659121†L145-L152】.  
Nurses work long hours with low pay, leading to high turnover【612233062184066†L64-L72】【612233062184066†L77-L81】.  
As wards close, ED patients wait over **48 hours** for beds【612233062184066†L96-L104】.  
Existing triage systems alone cannot resolve these issues.

## Solution

We propose an AI agent that helps hospital administrators:

1. **Real‑time Bed Coordination** – The agent queries bed availability and suggests reallocations, increasing the proportion of beds assigned to ED patients.
2. **Automated Scheduling** – It interfaces with a scheduling service (for example the Radiance AI system) to generate nurse rosters, considering preferences, legal constraints and hospital policies.
3. **Decision Support** – Using Bedrock AgentCore, the agent plans tool calls, performs reasoning and returns a concise report summarising recommendations.

## Architecture

See `docs/arch.png` for a visual overview.  
The main components are:

- **Client / Admin Interface** – A simple CLI or web interface to send tasks to the agent.
- **API Gateway** – Exposes endpoints `/run` and `/health`.
- **Lambda Function** – Hosts the FastAPI app and invokes the agent.
- **Bedrock AgentCore** – Performs reasoning and decides which tool to call.
- **Tools** – Stubs for bed queries, scheduling, ticket creation and other integrations.
- **S3** – Stores artefacts like reports or logs.

## Installation & Usage

See `README.md` for development setup.  
To run a local demo:

```sh
make demo
```

This sends a sample task that asks the agent to “assist with ED bed allocation and generate a nurse schedule”.

## Impact

By automating coordination and scheduling, hospitals can reduce waiting times, optimise staffing, and alleviate nurses’ workload.  
Our agent demonstrates how AWS AI services can address systemic healthcare challenges.  
Future work could integrate real hospital APIs, implement a full tool registry and deploy to multiple regions.

## Future Improvements

- Integrate hospital electronic medical record (EMR) APIs and scheduling services.
- Support Chinese LLMs on Bedrock to better process local language inputs.
- Implement dashboards and alerting for real‑time monitoring.