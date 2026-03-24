# RiteBite AI Marketing Co-Pilot

**Brand:** RiteBite Max Protein (Naturell India / Zydus Wellness)
**Course:** AI Tooling for Product Marketing — Term 7 Elective, ISB
**Stack:** Python · Streamlit · Anthropic Claude Sonnet 4.6 · fpdf2

---

## Overview

RiteBite AI Marketing Co-Pilot is a fully autonomous, multi-agent marketing intelligence and campaign generation system. A single button click triggers a sequential three-agent pipeline that monitors competitor activity, interprets the competitive signal, and produces a ready-to-deploy campaign package — all in under two minutes.

The system replaces a fragmented, multi-week manual workflow:

| Traditional Workflow | With AI Co-Pilot |
|---|---|
| Junior analyst monitors competitors (days) | Research Agent runs in seconds |
| Brand manager reviews and convenes strategy meeting (1–3 weeks) | Analyst Agent triages and constructs brief (seconds) |
| Agency or internal team creates campaign (2–6 weeks) | Campaign Creator Agent generates full package (seconds) |
| **Total: 4–8 weeks from signal to creative** | **Total: under 2 minutes** |

---

## Architecture

```
┌─────────────────────────┐
│      TRIGGER LAYER      │
│   "Run AI Marketing     │
│      Co-Pilot" button   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   🔬 RESEARCH AGENT      │
│                         │
│  Analyses competitor    │
│  activity across:       │
│  · Product & Pricing    │
│  · Digital Campaigns    │
│  · Consumer Sentiment   │
│  · Distribution         │
│                         │
│  Output: Structured     │
│  JSON intel report +    │
│  Threat level score     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   🧭 ANALYST AGENT       │
│                         │
│  Four internal modules: │
│  1. Signal Triage       │
│  2. Strategic Posture   │
│  3. ICP Segment Router  │
│  4. Brief Constructor   │
│                         │
│  Output: Campaign brief │
│  JSON with posture,     │
│  segment, constraints   │
└────────────┬────────────┘
             │
    ┌────────┴─────────┐
    │                  │
MONITOR_ONLY     RESPOND_NOW /
(pipeline ends)  RESPOND_SCHEDULED
                      │
                      ▼
        ┌─────────────────────────┐
        │  🎨 CAMPAIGN CREATOR     │
        │       AGENT             │
        │                         │
        │  Four pipeline stages:  │
        │  1. Strategic Position  │
        │  2. Copy Generation     │
        │  3. Visual Direction    │
        │  4. Channel Plan        │
        │                         │
        │  Output: Full campaign  │
        │  package across 5       │
        │  channels + PDF report  │
        └─────────────────────────┘
```

### Agent Details

#### Research Agent
Synthesises competitive intelligence for a selected competitor using Claude Sonnet 4.6 with an engineered system prompt. Produces a structured JSON report covering product and pricing moves, digital campaign strategy, consumer sentiment, and distribution activity. Assigns a threat level (High / Medium / Low) with rationale and three strategic recommendations.

#### Analyst Agent
Interprets the Research Agent's output through four sequential reasoning modules:

- **Signal Triage** — decides `RESPOND_NOW`, `RESPOND_SCHEDULED`, or `MONITOR_ONLY`
- **Strategic Posture Selector** — chooses Defensive Shield, Offensive Strike, Flanking Maneuver, or Thought Leadership based on competitive context
- **ICP Segment Router** — identifies which of RiteBite's four customer segments (Fitness Enthusiast, Busy Professional, Mindful Snacker, New-to-Protein) is the priority target
- **Campaign Brief Constructor** — assembles a structured brief with objective, constraints, do-not-mention list, and regulatory flags

If triage returns `MONITOR_ONLY`, the pipeline terminates here and the Campaign Creator is not triggered.

#### Campaign Creator Agent
Consumes the Analyst Agent's brief and generates a complete campaign package across five channels: Instagram, YouTube Pre-Roll, Google Search Ads, WhatsApp Broadcast, and D2C Website Banner. Each channel output includes hook, copy, CTA, and visual direction. Also produces a channel plan with budget percentage allocations, KPIs, cadence, and A/B testing recommendations.

---

## Competitor Coverage

Five pre-loaded competitors from RiteBite's competitive landscape, plus a free-text custom input:

| Competitor | Primary Threat Vector |
|---|---|
| The Whole Truth Foods | Clean-label narrative, Maltitol criticism |
| Yoga Bar | Mindful Snacker segment overlap |
| MuscleBlaze | High-protein bar market share |
| GetMyMettle | Premium energy segment |
| Epigamia | Adjacent healthy snacking space |

---

## Outputs

**Per-stage downloads:**
- Research Agent: downloadable PDF intel report
- Campaign Creator Agent: downloadable comprehensive PDF covering all three agent outputs (Research intel, Analyst brief, Campaign package)

**On-screen display:**
- Threat level badge with rationale
- Findings by category
- Strategic recommendations
- Analyst triage decision, strategic posture, ICP routing, and full brief
- Campaign positioning statement and messaging pillars
- Platform-specific copy and visual direction
- Channel plan with budget splits

---

## Setup

### Requirements

```
anthropic>=0.86.0
streamlit>=1.51.0
fpdf2>=2.8.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### API Key

The app requires an Anthropic API key. Set it as an environment variable before running:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

On Windows:

```cmd
set ANTHROPIC_API_KEY=your_key_here
```

### Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## GitHub Codespaces

This repository includes a Dev Container configuration. Open in Codespaces and the environment installs automatically. The Streamlit app starts on port 8501 and is forwarded to your browser.

---

## Project Structure

```
aitp-group-project/
├── app.py                                          # Main Streamlit application
├── requirements.txt                                # Python dependencies
├── .devcontainer/
│   └── devcontainer.json                           # Codespaces / Dev Container config
├── Prototype_A_Competitive_Intelligence_Scout.md   # Research Agent design doc
├── Orchestrator_Agent_Intelligence_to_Campaign_Pipeline.md  # Analyst Agent design doc
└── Prototype_D_AI_Campaign_Creator_Agent.md        # Campaign Creator design doc
```

---

## Design Documents

Full technical design documentation for each agent is available in the markdown files:

- **Research Agent** — `Prototype_A_Competitive_Intelligence_Scout.md`
  - System prompt design, JSON output schema, business metrics, demo flow
- **Analyst Agent** — `Orchestrator_Agent_Intelligence_to_Campaign_Pipeline.md`
  - Module architecture, triage logic, posture selection rules, ethical safeguards
- **Campaign Creator Agent** — `Prototype_D_AI_Campaign_Creator_Agent.md`
  - Four-stage pipeline design, output schema, campaign configuration parameters

---

## Ethical Safeguards

- **MONITOR_ONLY gate** — the pipeline does not generate campaigns for every competitive signal; only actionable threats (RESPOND_NOW / RESPOND_SCHEDULED) proceed to creative generation
- **Do-not-mention constraints** — the Analyst Agent injects competitor name exclusions into the brief so the Campaign Creator never produces comparative advertising
- **ASCI/FSSAI flags** — regulatory constraints are embedded in the brief before copy is generated
- **Human-in-the-loop** — all outputs are drafts for brand manager review; the agents recommend, humans approve

---

*Built for the AI Tooling for Product Marketing group project, ISB.*
