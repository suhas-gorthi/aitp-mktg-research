# Prototype A: AI Marketing Research Agent — Competitive Intelligence Scout

**Brand:** RiteBite Max Protein (Naturell India / Zydus Wellness)
**Course:** AI Tooling for Product Marketing — Term 7 Elective, ISB
**Prototype Option:** Option A — AI Marketing Research Agent

---

## 1. Objective

This prototype demonstrates how an autonomous AI research agent can replace the fragmented, manual competitive monitoring workflows currently used by RiteBite Max Protein's marketing team. The agent takes a competitor name as input, searches for market intelligence, synthesizes findings through LLM summarization, and delivers a structured, actionable report — all in under 30 seconds.

## 2. AI Architecture

The agent follows a three-stage pipeline:

| Stage | Function | Technology |
|-------|----------|------------|
| **Web Search & Data Collection** | Scrapes and retrieves recent competitor activity across product launches, pricing, campaigns, distribution, and consumer sentiment | Web search APIs, structured web scraping |
| **LLM Summarization & Analysis** | Processes raw data through a large language model with a carefully engineered system prompt that enforces structured output and RiteBite-specific analytical framing | Claude Sonnet 4 (Anthropic API) |
| **Structured Report Generation** | Outputs a JSON-structured intelligence report with defined sections, threat scoring, and strategic recommendations | JSON schema enforcement via prompt engineering |

### AI Type Justification

This prototype uses an **Autonomous Research Agent** pattern — a single-purpose agent that combines tool use (web search) with generative reasoning (LLM summarization) and structured output (JSON schema). This is distinct from a simple chatbot because:

- The agent independently decides what information to retrieve based on the competitor context
- It applies analytical reasoning to assign threat levels and generate recommendations
- It produces a standardized, machine-readable output that could feed into dashboards or CRM systems

## 3. System Prompt Design

The agent operates under a detailed system prompt that establishes:

- **Role:** AI Marketing Research Agent for RiteBite Max Protein
- **Output Format:** Strict JSON schema with predefined sections (Product & Pricing Moves, Digital & Campaign Strategy, Consumer Sentiment, Distribution & Channel Expansion)
- **Analytical Framework:** Each finding must be data-rich, specific, and actionable; threat levels are calibrated against RiteBite's specific vulnerabilities
- **Brand Context:** The agent understands RiteBite's positioning, ICP segments, pricing strategy, and competitive vulnerabilities (e.g., clean-label criticism around Maltitol usage)

### JSON Output Schema

```json
{
  "competitor": "string",
  "report_date": "string",
  "executive_summary": "string (2-3 sentences)",
  "sections": [
    {
      "title": "string",
      "icon": "emoji",
      "findings": ["string (1-2 sentences each)", "..."]
    }
  ],
  "threat_level": "High | Medium | Low",
  "threat_rationale": "string (1-2 sentences)",
  "strategic_recommendations": ["string", "string", "string"]
}
```

## 4. Competitor Coverage

The prototype includes five pre-loaded competitors from RiteBite's competitive landscape:

| Competitor | Positioning | Primary Threat Vector |
|------------|-------------|----------------------|
| The Whole Truth Foods | Clean-label, radical transparency | Ingredient scrutiny, Maltitol criticism |
| Yoga Bar | Natural, wholesome, community-driven | Mindful Snacker segment overlap |
| MuscleBlaze | Hardcore sports nutrition | High-protein bar market share |
| GetMyMettle | Energy and endurance focus | Premium energy segment |
| Epigamia | Greek yogurt / functional snacks | Adjacent healthy snacking space |

Users can also enter any custom competitor name for ad-hoc research.

## 5. Business Metrics Addressed

| Metric | How the Agent Helps |
|--------|-------------------|
| **Time-to-Insight** | Reduces competitive analysis from days of manual research to under 30 seconds |
| **Decision Cycle** | Enables real-time competitive response instead of quarterly review cycles |
| **Cost Reduction** | Eliminates need for expensive third-party market intelligence subscriptions for routine monitoring |
| **Risk Reduction** | Continuous competitor monitoring catches pricing moves, campaign launches, and distribution changes before they erode market share |

## 6. Demonstration Flow

For the presentation, the recommended demo sequence is:

1. **Show the architecture diagram** at the top of the prototype (Web Search → LLM Summarization → Structured Report)
2. **Select "The Whole Truth Foods"** as the competitor — this is the highest-threat competitor identified in the GTM document and produces the most compelling report
3. **Walk through the generated report sections** while narrating how each section maps to a specific competitive intelligence need
4. **Highlight the threat assessment bar** and strategic recommendations as the actionable output
5. **Optionally run a second query** with a custom competitor name to demonstrate flexibility

## 7. Limitations & Future Enhancements

### Current Limitations
- The prototype uses the LLM's training knowledge rather than live web scraping due to demo constraints
- Threat levels are qualitatively assigned rather than computed from quantitative market data
- Single-turn interaction — does not support follow-up queries on the same report

### Production Enhancements
- Integration with real-time web scraping APIs (SerpAPI, Firecrawl) for live data
- Scheduled automated runs with change-detection alerts (e.g., "The Whole Truth launched a new SKU")
- Dashboard integration pushing reports into Notion, Slack, or internal BI tools
- Multi-agent orchestration where the Research Agent feeds findings into the Campaign Creator Agent and Recommendation Engine

## 8. Connection to GTM Strategy

This prototype directly addresses the pain point identified in the GTM document:

> *"The current GTM model relies on traditional, labor-intensive workflows. Campaign conceptualization, influencer outreach, and digital personalization are managed through fragmented, manual processes."*

The Competitive Intelligence Scout automates the upstream research that informs all downstream marketing decisions — from campaign positioning to pricing strategy to influencer selection. In the proposed AI architecture, it feeds into **Layer 1 (Data Ingestion)** by providing real-time competitive context, and informs **Layer 2 (Orchestration)** by updating the knowledge graphs that power recommendation and campaign agents.

---

*Prototype built with React + Anthropic Claude API. Designed for the AI Tooling for Product Marketing group project, ISB.*
