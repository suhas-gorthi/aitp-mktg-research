import json
import os
import uuid
from datetime import datetime

import anthropic
import streamlit as st
from fpdf import FPDF

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RiteBite AI Marketing Co-Pilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
  html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117; color: #e6edf3;
  }
  [data-testid="stHeader"] { background: transparent; }

  .hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 60%, #1a0a2e 100%);
    border: 1px solid #30363d; border-radius: 16px;
    padding: 36px 40px 28px; margin-bottom: 24px;
  }
  .hero h1 { font-size: 2.1rem; font-weight: 800; margin: 0 0 6px;
    background: linear-gradient(90deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .hero p { color: #8b949e; font-size: 1rem; margin: 0; }

  /* pipeline */
  .pipeline {
    display: flex; align-items: center; gap: 0;
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 18px 28px; margin-bottom: 24px; flex-wrap: wrap; justify-content: center;
  }
  .pipe-step {
    display: flex; flex-direction: column; align-items: center;
    border: 1px solid #30363d; border-radius: 10px;
    padding: 14px 22px; min-width: 155px; text-align: center;
  }
  .pipe-step.active { border-color: #58a6ff; background: #1a2332; }
  .pipe-step.done   { border-color: #3fb950; background: #0d2310; }
  .pipe-step.idle   { background: #21262d; }
  .pipe-step .icon  { font-size: 1.8rem; margin-bottom: 6px; }
  .pipe-step .label { font-weight: 700; font-size: 0.85rem; color: #e6edf3; }
  .pipe-step .sub   { font-size: 0.73rem; color: #8b949e; margin-top: 3px; }
  .pipe-arrow { font-size: 1.4rem; color: #30363d; padding: 0 10px; }

  /* stage headers */
  .stage-header {
    display: flex; align-items: center; gap: 14px;
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 18px 24px; margin: 24px 0 16px;
  }
  .stage-badge {
    background: #21262d; border: 1px solid #30363d; border-radius: 8px;
    padding: 6px 14px; font-size: 0.78rem; font-weight: 700; color: #58a6ff;
    white-space: nowrap;
  }
  .stage-title { font-size: 1.15rem; font-weight: 800; color: #e6edf3; }
  .stage-sub   { font-size: 0.82rem; color: #8b949e; margin-top: 2px; }

  /* competitor cards */
  .comp-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 10px; }
  .comp-card {
    background: #21262d; border: 1px solid #30363d; border-radius: 10px;
    padding: 14px 18px; cursor: pointer; transition: all .2s; min-width: 150px;
    text-align: center;
  }
  .comp-card:hover { border-color: #58a6ff; background: #1a2332; }

  /* report */
  .report-header {
    background: linear-gradient(135deg, #1a1f2e, #12181f);
    border: 1px solid #30363d; border-radius: 14px;
    padding: 28px 32px; margin-bottom: 20px;
  }
  .report-title { font-size: 1.5rem; font-weight: 800; color: #e6edf3; margin: 0 0 6px; }
  .report-meta  { color: #8b949e; font-size: 0.85rem; }
  .exec-summary { background: #161b22; border-left: 3px solid #58a6ff;
    border-radius: 8px; padding: 16px 20px; margin-top: 18px;
    color: #c9d1d9; font-size: 0.95rem; line-height: 1.6; }

  .section-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 22px 26px; margin-bottom: 16px;
  }
  .section-title { font-size: 1.05rem; font-weight: 700; color: #e6edf3; margin-bottom: 14px; }
  .finding { display: flex; gap: 10px; align-items: flex-start;
    padding: 10px 0; border-bottom: 1px solid #21262d; }
  .finding:last-child { border-bottom: none; }
  .finding-dot { color: #58a6ff; font-size: 0.7rem; margin-top: 5px; flex-shrink: 0; }
  .finding-text { color: #c9d1d9; font-size: 0.9rem; line-height: 1.55; }

  .threat-high   { background: #3d1010; border: 1px solid #f85149; color: #f85149; border-radius: 8px; padding: 16px 20px; }
  .threat-medium { background: #2d1e00; border: 1px solid #d29922; color: #d29922; border-radius: 8px; padding: 16px 20px; }
  .threat-low    { background: #0d2310; border: 1px solid #3fb950; color: #3fb950; border-radius: 8px; padding: 16px 20px; }
  .threat-label     { font-size: 1.3rem; font-weight: 800; }
  .threat-rationale { font-size: 0.88rem; margin-top: 6px; opacity: 0.85; }

  .rec-card {
    background: #161b22; border: 1px solid #1f3a1f; border-radius: 10px;
    padding: 16px 20px; margin-bottom: 12px; display: flex; gap: 14px; align-items: flex-start;
  }
  .rec-num { background: #238636; color: #fff; border-radius: 50%;
    width: 26px; height: 26px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; font-size: 0.8rem; flex-shrink: 0; }
  .rec-text { color: #c9d1d9; font-size: 0.9rem; line-height: 1.55; }

  /* orchestrator */
  .brief-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 20px 24px; margin-bottom: 14px;
  }
  .brief-label { font-size: 0.75rem; font-weight: 700; color: #8b949e;
    text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
  .brief-value { font-size: 0.95rem; color: #e6edf3; line-height: 1.5; }

  .posture-badge {
    display: inline-block; border-radius: 8px; padding: 8px 18px;
    font-weight: 700; font-size: 0.9rem; margin-bottom: 10px;
  }
  .posture-defensive  { background: #1a0a2e; border: 1px solid #bc8cff; color: #bc8cff; }
  .posture-offensive  { background: #3d1010; border: 1px solid #f85149; color: #f85149; }
  .posture-flanking   { background: #2d1e00; border: 1px solid #d29922; color: #d29922; }
  .posture-leadership { background: #0d2310; border: 1px solid #3fb950; color: #3fb950; }

  .triage-now       { background: #3d1010; border: 1px solid #f85149; color: #f85149; border-radius: 8px; padding: 12px 18px; font-weight: 700; }
  .triage-scheduled { background: #2d1e00; border: 1px solid #d29922; color: #d29922; border-radius: 8px; padding: 12px 18px; font-weight: 700; }
  .triage-monitor   { background: #161b22; border: 1px solid #30363d; color: #8b949e; border-radius: 8px; padding: 12px 18px; font-weight: 700; }

  /* campaign */
  .campaign-card {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 22px 26px; margin-bottom: 16px;
  }
  .campaign-card-title {
    font-size: 0.88rem; font-weight: 700; color: #58a6ff;
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
  }
  .copy-field { margin-bottom: 12px; }
  .copy-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase;
    letter-spacing: 0.05em; margin-bottom: 4px; }
  .copy-value { background: #21262d; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; font-size: 0.9rem; color: #c9d1d9; line-height: 1.55; }

  .channel-row {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 0; border-bottom: 1px solid #21262d;
  }
  .channel-row:last-child { border-bottom: none; }
  .channel-pct { font-size: 1.3rem; font-weight: 800; color: #58a6ff; min-width: 56px; }
  .channel-info .ch-name { font-weight: 700; font-size: 0.9rem; color: #e6edf3; }
  .channel-info .ch-kpi  { font-size: 0.8rem; color: #8b949e; margin-top: 2px; }

  /* loading */
  .loading-box {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 40px; text-align: center; margin: 20px 0;
  }
  .loading-title { font-size: 1.1rem; font-weight: 700; color: #58a6ff; margin-bottom: 8px; }
  .loading-sub   { color: #8b949e; font-size: 0.88rem; }

  /* buttons */
  div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1f6feb, #1a56c4) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 12px 32px !important; font-weight: 700 !important; font-size: 1rem !important;
    cursor: pointer !important; width: 100% !important; transition: opacity .2s !important;
  }
  div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Constants ─────────────────────────────────────────────────────────────────
COMPETITORS = [
    {"name": "The Whole Truth Foods", "icon": "🌿", "tag": "Clean-label / Transparency", "threat": "High"},
    {"name": "Yoga Bar",              "icon": "🧘", "tag": "Natural / Community",         "threat": "Medium"},
    {"name": "MuscleBlaze",           "icon": "💪", "tag": "Sports Nutrition",             "threat": "Medium"},
    {"name": "GetMyMettle",           "icon": "⚡", "tag": "Energy / Endurance",           "threat": "Low"},
    {"name": "Epigamia",              "icon": "🥛", "tag": "Functional Snacks",            "threat": "Low"},
]

# ── System Prompts ────────────────────────────────────────────────────────────
INTEL_SYSTEM_PROMPT = """You are a Competitive Intelligence Agent for RiteBite Max Protein (by Zydus Wellness / Naturell India).

## Your Role
Generate a structured, data-rich competitive intelligence report on the competitor provided.

## RiteBite Brand Context
- Product: High-protein bars (20g protein / bar), positioned as India's #1 protein bar
- Price: ₹60–100/bar — premium tier
- ICP: Urban fitness-conscious millennials (Fitness Enthusiast, Mindful Snacker, Health-Curious Mainstream)
- Key vulnerability: Clean-label criticism due to Maltitol and artificial sweetener use
- Strength: Superior taste, wide distribution, trusted Zydus Wellness parentage

## Output Format
Return ONLY a valid JSON object matching this exact schema — no commentary, no markdown fences:

{
  "competitor": "string",
  "report_date": "ISO8601 datetime string",
  "executive_summary": "2-3 sentence strategic overview",
  "sections": [
    {"title": "Product & Pricing Moves",       "icon": "💰", "findings": ["finding 1", "finding 2", "finding 3"]},
    {"title": "Digital & Campaign Strategy",   "icon": "📱", "findings": ["finding 1", "finding 2"]},
    {"title": "Distribution & Channel Expansion","icon": "🚚","findings": ["finding 1", "finding 2"]},
    {"title": "Consumer Sentiment",            "icon": "🗣️", "findings": ["finding 1", "finding 2"]}
  ],
  "threat_level": "High | Medium | Low",
  "threat_rationale": "1-2 sentence explanation calibrated to RiteBite's specific vulnerabilities",
  "strategic_recommendations": ["rec 1", "rec 2", "rec 3"]
}

## Quality Rules
- Each finding must be specific, data-rich, and actionable — not generic
- Threat level must be calibrated against RiteBite's positioning and vulnerabilities
- Recommendations must directly counter identified threats or exploit competitor weaknesses"""

ORCHESTRATOR_SYSTEM_PROMPT = """You are the Orchestrator Agent for RiteBite Max Protein's AI Marketing Pipeline.

## Your Role
You sit between the Competitive Intelligence Scout (Prototype A) and the Campaign Creator Agent (Prototype D).
You receive a structured intelligence report and decide:
1. Whether a campaign response is warranted (Signal Triage)
2. What strategic posture to adopt (Strategic Posture Selector)
3. Which ICP segment to target (ICP Segment Router)
4. Construct a structured campaign brief (Campaign Brief Constructor)

## RiteBite Brand Context
- Product: High-protein bars (20g protein / bar), India's #1 protein bar
- Price: ₹60–100/bar — premium tier
- ICP Segments: Fitness Enthusiast | Busy Professional | Mindful Snacker | New-to-Protein
- Key vulnerability: Clean-label criticism (Maltitol, artificial sweeteners)
- Key strength: Taste, distribution, Zydus Wellness parentage, naturally sweetened variants (Date & Almond, Millet Wafer)

## Triage Logic
- High threat + action keywords (launched, viral, campaign, pricing change, gained market share) = RESPOND_NOW
- Medium threat + specific recommendations = RESPOND_SCHEDULED
- Low threat + vague signals = MONITOR_ONLY (no campaign triggered)

## Strategic Posture Options
- Defensive Shield: Competitor attacking RiteBite's vulnerabilities → lead with naturally sweetened range, transparency
- Offensive Strike: Competitor showing weakness → aggressively capture their vulnerable segment
- Flanking Maneuver: Competitor dominating one segment but neglecting another → target underserved segment
- Thought Leadership: No immediate threat → own category narrative, educational content

## ICP Routing
- Clean-label / ingredient attack → Mindful Snacker + New-to-Protein
- High-protein sports nutrition → Fitness Enthusiast
- Convenience / quick-commerce → Busy Professional
- Price undercutting → New-to-Protein

## Output Format
Return ONLY a valid JSON object — no commentary, no markdown fences:

{
  "brief_id": "auto-generate a UUID-style string",
  "generated_at": "ISO8601 datetime string",
  "source_report": {
    "competitor": "string",
    "threat_level": "High | Medium | Low",
    "report_summary": "2-3 sentence summary of the intelligence report"
  },
  "orchestrator_decisions": {
    "triage_result": "RESPOND_NOW | RESPOND_SCHEDULED | MONITOR_ONLY",
    "triage_rationale": "1-2 sentences explaining triage decision",
    "strategic_posture": "Defensive Shield | Offensive Strike | Flanking Maneuver | Thought Leadership",
    "posture_rationale": "2-3 sentences explaining the strategic choice",
    "primary_icp_segment": "Fitness Enthusiast | Busy Professional | Mindful Snacker | New-to-Protein",
    "segment_rationale": "1-2 sentences explaining why this segment is the priority"
  },
  "campaign_parameters": {
    "objective": "string — specific campaign objective",
    "key_competitive_gap": "string — the specific vulnerability or opportunity to exploit",
    "mandatory_product_focus": ["SKU 1", "SKU 2"],
    "brand_voice_emphasis": "string — specific tone calibration for this campaign",
    "budget_tier": "High | Medium | Low",
    "urgency": "Immediate | This Week | This Month",
    "channels_recommended": ["Instagram", "YouTube", "Google Search"]
  },
  "constraints": {
    "do_not_mention": ["list of competitors or topics to avoid"],
    "regulatory_flags": ["any ASCI or FSSAI constraints relevant to claims"],
    "must_include": ["mandatory elements — taglines, disclaimers, product shots"]
  }
}"""

CAMPAIGN_SYSTEM_PROMPT = """You are the Campaign Creator Agent for RiteBite Max Protein (by Zydus Wellness / Naturell India).

## Your Role
You receive a structured campaign brief from the Orchestrator Agent and generate a complete, ready-to-execute campaign package across four stages:
1. Strategic Positioning
2. Platform-Specific Copy Generation
3. Visual & Creative Direction
4. Channel Plan & Budget Allocation

## RiteBite Brand Voice (ALWAYS apply)
- Tone: Energetic, motivational, never preachy or clinical
- Cultural register: Young urban Indian, code-switch English-Hindi naturally (e.g., "Protein ka Punch")
- Campaign DNA: "Protein Salute" (breaking procrastination), "Protein Aayega Tabhi India Khayega" (cultural embedding)
- FORBIDDEN: Generic health-food clichés, guilt-based messaging, naming competitors directly in consumer copy

## Output Format
Return ONLY a valid JSON object — no commentary, no markdown fences:

{
  "campaign_name": "string — a memorable campaign name",
  "competitive_context": "string — 2-3 sentences summarizing the intelligence that triggered this",
  "positioning": {
    "statement": "string — 1 sentence core positioning",
    "messaging_pillars": ["pillar 1", "pillar 2", "pillar 3"],
    "competitive_hooks": ["specific differentiation point 1", "specific differentiation point 2"]
  },
  "creative": {
    "instagram": {
      "hook": "string — first 3 seconds or first line",
      "body": "string — main copy",
      "cta": "string",
      "visual_direction": "string — mood, color, talent, composition"
    },
    "youtube_pre_roll": {
      "hook": "string — first 5 seconds",
      "script_outline": "string — 15-second script structure",
      "visual_direction": "string"
    },
    "google_search_ad": {
      "headlines": ["max 30 chars", "max 30 chars", "max 30 chars"],
      "descriptions": ["max 90 chars", "max 90 chars"],
      "visual_direction": "string"
    },
    "whatsapp_broadcast": {
      "message": "string — under 160 chars",
      "cta_button": "string"
    },
    "d2c_website_banner": {
      "headline": "string",
      "subhead": "string",
      "cta": "string",
      "visual_direction": "string"
    }
  },
  "channel_plan": {
    "total_budget_allocation": "string — description of split logic",
    "channels": [
      {
        "channel": "string",
        "budget_pct": 30,
        "objective": "string",
        "kpi": "string",
        "cadence": "string"
      }
    ],
    "ab_testing": ["what to test variant A vs B", "second test"]
  }
}"""


# ── API client ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client(api_key: str):
    return anthropic.Anthropic(api_key=api_key)


def _parse_json_response(response) -> dict:
    for block in response.content:
        if block.type == "text":
            raw = block.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.rsplit("```", 1)[0]
            return json.loads(raw.strip())
    raise ValueError("No text block in response")


def run_intel_agent(competitor_name: str, api_key: str) -> dict:
    client = get_client(api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=INTEL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Generate a competitive intelligence report for: {competitor_name}"}],
    )
    return _parse_json_response(response)


def run_orchestrator(intel_report: dict, api_key: str) -> dict:
    client = get_client(api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=ORCHESTRATOR_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Process this competitive intelligence report and generate a campaign brief:\n\n{json.dumps(intel_report, indent=2)}"
        }],
    )
    return _parse_json_response(response)


def run_campaign_creator(brief: dict, api_key: str) -> dict:
    client = get_client(api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        system=CAMPAIGN_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Generate a complete campaign package based on this brief:\n\n{json.dumps(brief, indent=2)}"
        }],
    )
    return _parse_json_response(response)


# ── PDF helpers ───────────────────────────────────────────────────────────────
def _s(text: str) -> str:
    return "".join(c if ord(c) < 256 else "?" for c in (
        str(text)
        .replace("\u2014", "-").replace("\u2013", "-")
        .replace("\u2018", "'").replace("\u2019", "'")
        .replace("\u201c", '"').replace("\u201d", '"')
        .replace("\u2022", "-").replace("\u2026", "...")
        .replace("\u00a0", " ").replace("\u20b9", "Rs.")
    ))


def generate_intel_pdf(report: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    W = pdf.epw  # effective page width — always use this for multi_cell

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Competitive Intelligence Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, _s(report["competitor"]), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generated {report['report_date'][:10]}  |  Research Agent  |  Claude Sonnet 4.6", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    threat = report.get("threat_level", "Medium")
    tc = {"High": (220, 50, 50), "Medium": (200, 140, 30), "Low": (40, 160, 80)}
    r, g, b = tc.get(threat, (120, 120, 120))
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 7, f"Threat Level: {threat}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 6, _s(report.get("threat_rationale", "")))
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(88, 166, 255)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(W, 6, _s(report.get("executive_summary", "")))
    pdf.ln(5)

    for section in report.get("sections", []):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 7, _s(section["title"]), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(48, 54, 61)
        pdf.set_line_width(0.3)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        for finding in section.get("findings", []):
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(W, 6, f"*  {_s(finding)}")
            pdf.ln(1)
        pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, "Strategic Recommendations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(35, 134, 54)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
    pdf.ln(2)
    for i, rec in enumerate(report.get("strategic_recommendations", []), 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(pdf.l_margin)
        pdf.cell(8, 6, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        # multi_cell width = remaining space after the numbering cell
        pdf.multi_cell(W - 8, 6, _s(rec))
        pdf.ln(1)

    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "RiteBite Max Protein  |  Competitive Intelligence Research Agent", align="C")
    return bytes(pdf.output())


def generate_full_report_pdf(intel: dict, brief: dict, campaign: dict) -> bytes:
    """Comprehensive PDF with all three agent outputs: Research Agent + Analyst Agent + Campaign Creator Agent."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    W = pdf.epw

    def mc(text: str, h: float = 6, indent: float = 0):
        pdf.set_x(pdf.l_margin + indent)
        pdf.multi_cell(W - indent, h, _s(text))

    def rule(color=(48, 54, 61), lw=0.3):
        pdf.set_draw_color(*color)
        pdf.set_line_width(lw)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + W, pdf.get_y())
        pdf.ln(2)

    def section_heading(title: str, color=(30, 30, 30)):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*color)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")

    def part_divider(part_num: int, part_title: str):
        pdf.ln(4)
        pdf.set_fill_color(30, 30, 40)
        pdf.set_draw_color(88, 166, 255)
        pdf.set_line_width(0.8)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(88, 166, 255)
        pdf.cell(0, 10, _s(f"  Part {part_num}: {part_title}"), new_x="LMARGIN", new_y="NEXT", fill=True, border="LB")
        pdf.ln(4)

    # ── Cover ─────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, "RiteBite Max Protein", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 9, "AI Marketing Pipeline - Full Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Competitor: {intel.get('competitor','')}  |  Generated: {datetime.now().strftime('%Y-%m-%d')}  |  Claude Sonnet 4.6", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    rule((88, 166, 255), 1.0)
    pdf.ln(2)

    # ── PART 1: Research Agent ─────────────────────────────────────────────────
    part_divider(1, "Research Agent - Competitive Intelligence Report")

    threat = intel.get("threat_level", "Medium")
    tc = {"High": (220, 50, 50), "Medium": (200, 140, 30), "Low": (40, 160, 80)}
    r, g, b = tc.get(threat, (120, 120, 120))
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 7, f"Threat Level: {threat}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    mc(intel.get("threat_rationale", ""))
    pdf.ln(4)

    section_heading("Executive Summary")
    rule((88, 166, 255), 0.8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(intel.get("executive_summary", ""))
    pdf.ln(5)

    for sec in intel.get("sections", []):
        section_heading(_s(sec["title"]))
        rule()
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        for finding in sec.get("findings", []):
            mc(f"*  {finding}")
            pdf.ln(1)
        pdf.ln(3)

    section_heading("Strategic Recommendations")
    rule((35, 134, 54), 0.8)
    for i, rec in enumerate(intel.get("strategic_recommendations", []), 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(pdf.l_margin)
        pdf.cell(8, 6, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(W - 8, 6, _s(rec))
        pdf.ln(1)

    # ── PART 2: Analyst Agent ──────────────────────────────────────────────────
    pdf.add_page()
    part_divider(2, "Analyst Agent - Strategic Brief")

    decisions = brief.get("orchestrator_decisions", {})
    cp = brief.get("campaign_parameters", {})
    constraints = brief.get("constraints", {})

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(60, 60, 60)
    mc(f"Brief ID: {brief.get('brief_id', '')}  |  Generated: {brief.get('generated_at', '')[:10]}")
    pdf.ln(3)

    section_heading("Triage & Posture Decisions")
    rule((188, 140, 255), 0.8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(f"Triage Result: {decisions.get('triage_result', '')}")
    mc(f"Triage Rationale: {decisions.get('triage_rationale', '')}")
    pdf.ln(2)
    mc(f"Strategic Posture: {decisions.get('strategic_posture', '')}")
    mc(f"Posture Rationale: {decisions.get('posture_rationale', '')}")
    pdf.ln(2)
    mc(f"Primary ICP Segment: {decisions.get('primary_icp_segment', '')}")
    mc(f"Segment Rationale: {decisions.get('segment_rationale', '')}")
    pdf.ln(5)

    section_heading("Campaign Parameters")
    rule()
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(f"Objective: {cp.get('objective', '')}")
    pdf.ln(1)
    mc(f"Key Competitive Gap: {cp.get('key_competitive_gap', '')}")
    pdf.ln(1)
    mc(f"Mandatory Product Focus: {', '.join(cp.get('mandatory_product_focus', []))}")
    pdf.ln(1)
    mc(f"Brand Voice Emphasis: {cp.get('brand_voice_emphasis', '')}")
    pdf.ln(1)
    mc(f"Budget Tier: {cp.get('budget_tier', '')}  |  Urgency: {cp.get('urgency', '')}")
    pdf.ln(1)
    mc(f"Recommended Channels: {', '.join(cp.get('channels_recommended', []))}")
    pdf.ln(5)

    section_heading("Constraints & Guardrails")
    rule((35, 134, 54), 0.8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(f"Do Not Mention: {', '.join(constraints.get('do_not_mention', []))}")
    pdf.ln(1)
    mc(f"Regulatory Flags: {', '.join(constraints.get('regulatory_flags', []))}")
    pdf.ln(1)
    mc(f"Must Include: {', '.join(constraints.get('must_include', []))}")

    # ── PART 3: Campaign Creator Agent ────────────────────────────────────────
    pdf.add_page()
    part_divider(3, f"Campaign Creator Agent - {_s(campaign.get('campaign_name', 'Campaign Package'))}")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(campaign.get("competitive_context", ""))
    pdf.ln(5)

    pos = campaign.get("positioning", {})
    section_heading("Strategic Positioning")
    rule()
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(60, 60, 60)
    mc(pos.get("statement", ""))
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for pillar in pos.get("messaging_pillars", []):
        mc(f"*  {pillar}")
    pdf.ln(2)
    for hook in pos.get("competitive_hooks", []):
        mc(f"-  {hook}")
    pdf.ln(5)

    section_heading("Platform Creative Executions")
    rule()
    creative = campaign.get("creative", {})
    platforms = [
        ("Instagram",          creative.get("instagram", {})),
        ("YouTube Pre-Roll",   creative.get("youtube_pre_roll", {})),
        ("Google Search Ad",   creative.get("google_search_ad", {})),
        ("WhatsApp Broadcast", creative.get("whatsapp_broadcast", {})),
        ("D2C Website Banner", creative.get("d2c_website_banner", {})),
    ]
    for platform_name, data in platforms:
        if data:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(88, 166, 255)
            pdf.set_x(pdf.l_margin)
            pdf.cell(0, 6, platform_name, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(60, 60, 60)
            for k, v in data.items():
                if isinstance(v, list):
                    v = " | ".join(str(x) for x in v)
                mc(f"{k}: {v}", h=5.5, indent=4)
            pdf.ln(2)
    pdf.ln(3)

    ch_plan = campaign.get("channel_plan", {})
    section_heading("Channel Plan & Budget Allocation")
    rule()
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    mc(ch_plan.get("total_budget_allocation", ""))
    pdf.ln(2)
    for ch in ch_plan.get("channels", []):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 6, _s(f"{ch.get('channel','')} — {ch.get('budget_pct','')}%"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        mc(f"Objective: {ch.get('objective','')} | KPI: {ch.get('kpi','')} | Cadence: {ch.get('cadence','')}", h=5.5, indent=4)
        pdf.ln(1)

    ab_tests = ch_plan.get("ab_testing", [])
    if ab_tests:
        pdf.ln(3)
        section_heading("A/B Testing Recommendations")
        rule()
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        for test in ab_tests:
            mc(f"*  {test}")
            pdf.ln(1)

    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "RiteBite Max Protein  |  AI Marketing Pipeline  |  Research Agent + Analyst Agent + Campaign Creator Agent", align="C")
    return bytes(pdf.output())


# ── UI helpers ────────────────────────────────────────────────────────────────
def render_pipeline_header(stage: str):
    """stage: 'idle' | 'intel_done' | 'orch_done' | 'complete'"""
    intel_done = stage in ("intel_done", "orch_done", "complete")
    orch_done  = stage in ("orch_done", "complete")
    camp_done  = stage == "complete"

    def step(base_icon, label, done):
        cls  = "done" if done else "idle"
        icon = "✅" if done else base_icon
        return (
            f'<div class="pipe-step {cls}">'
            f'<div class="icon">{icon}</div>'
            f'<div class="label">{label}</div></div>'
        )

    st.markdown(f"""
<div class="pipeline">
  {step("🔬", "Research Agent<br><small>Intelligence Report</small>", intel_done)}
  <div class="pipe-arrow">→</div>
  {step("🧭", "Analyst Agent<br><small>Strategic Brief</small>", orch_done)}
  <div class="pipe-arrow">→</div>
  {step("🎨", "Campaign Creator Agent<br><small>Campaign Package</small>", camp_done)}
</div>""", unsafe_allow_html=True)


def render_intel_report(report: dict):
    threat = report.get("threat_level", "Medium")
    icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    st.markdown(f"""
<div class="report-header">
  <div class="report-title">🔍 {report['competitor']}</div>
  <div class="report-meta">Generated {report['report_date'][:10]} &nbsp;·&nbsp; Research Agent &nbsp;·&nbsp; Claude Sonnet 4.6</div>
  <div class="exec-summary">{report['executive_summary']}</div>
</div>""", unsafe_allow_html=True)

    tc = f"threat-{threat.lower()}"
    st.markdown(f"""
<div class="{tc}">
  <div class="threat-label">{icons.get(threat,'🟡')} Threat Level: {threat}</div>
  <div class="threat-rationale">{report['threat_rationale']}</div>
</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, section in enumerate(report.get("sections", [])):
        with cols[i % 2]:
            fh = "".join(
                f'<div class="finding"><span class="finding-dot">●</span>'
                f'<span class="finding-text">{f}</span></div>'
                for f in section["findings"]
            )
            st.markdown(f'<div class="section-card"><div class="section-title">{section["icon"]} {section["title"]}</div>{fh}</div>', unsafe_allow_html=True)

    st.markdown("### 🎯 Strategic Recommendations")
    for i, rec in enumerate(report.get("strategic_recommendations", []), 1):
        st.markdown(f'<div class="rec-card"><div class="rec-num">{i}</div><div class="rec-text">{rec}</div></div>', unsafe_allow_html=True)


def render_orchestrator_brief(brief: dict):
    decisions = brief.get("orchestrator_decisions", {})
    params    = brief.get("campaign_parameters", {})
    triage    = decisions.get("triage_result", "")
    posture   = decisions.get("strategic_posture", "")

    triage_class = {"RESPOND_NOW": "triage-now", "RESPOND_SCHEDULED": "triage-scheduled", "MONITOR_ONLY": "triage-monitor"}.get(triage, "triage-monitor")
    triage_icon  = {"RESPOND_NOW": "🚨", "RESPOND_SCHEDULED": "📅", "MONITOR_ONLY": "👁️"}.get(triage, "")

    posture_class = {
        "Defensive Shield":  "posture-defensive",
        "Offensive Strike":  "posture-offensive",
        "Flanking Maneuver": "posture-flanking",
        "Thought Leadership":"posture-leadership",
    }.get(posture, "posture-defensive")

    st.markdown(f"""
<div style="display:flex;gap:14px;margin-bottom:18px;flex-wrap:wrap;">
  <div class="{triage_class}">{triage_icon} {triage}</div>
  <div class="{posture_class}">{posture}</div>
</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
<div class="brief-card">
  <div class="brief-label">Triage Rationale</div>
  <div class="brief-value">{decisions.get('triage_rationale','')}</div>
</div>
<div class="brief-card">
  <div class="brief-label">Strategic Posture Rationale</div>
  <div class="brief-value">{decisions.get('posture_rationale','')}</div>
</div>
<div class="brief-card">
  <div class="brief-label">Primary ICP Segment</div>
  <div class="brief-value">👥 {decisions.get('primary_icp_segment','')}<br>
  <small style="color:#8b949e">{decisions.get('segment_rationale','')}</small></div>
</div>""", unsafe_allow_html=True)

    with col2:
        channels = ", ".join(params.get("channels_recommended", []))
        products = ", ".join(params.get("mandatory_product_focus", []))
        st.markdown(f"""
<div class="brief-card">
  <div class="brief-label">Campaign Objective</div>
  <div class="brief-value">{params.get('objective','')}</div>
</div>
<div class="brief-card">
  <div class="brief-label">Key Competitive Gap</div>
  <div class="brief-value">{params.get('key_competitive_gap','')}</div>
</div>
<div class="brief-card">
  <div class="brief-label">Mandatory Product Focus</div>
  <div class="brief-value">{products}</div>
</div>
<div class="brief-card">
  <div class="brief-label">Budget Tier · Urgency · Channels</div>
  <div class="brief-value">{params.get('budget_tier','')} budget · {params.get('urgency','')} · {channels}</div>
</div>""", unsafe_allow_html=True)

    # Constraints
    constraints = brief.get("constraints", {})
    st.markdown("#### 🚦 Constraints & Guardrails")
    c1, c2, c3 = st.columns(3)
    with c1:
        items = "\n".join(f"• {x}" for x in constraints.get("do_not_mention", []))
        st.markdown(f'<div class="brief-card"><div class="brief-label">Do Not Mention</div><div class="brief-value">{items}</div></div>', unsafe_allow_html=True)
    with c2:
        items = "\n".join(f"• {x}" for x in constraints.get("regulatory_flags", []))
        st.markdown(f'<div class="brief-card"><div class="brief-label">Regulatory Flags</div><div class="brief-value">{items}</div></div>', unsafe_allow_html=True)
    with c3:
        items = "\n".join(f"• {x}" for x in constraints.get("must_include", []))
        st.markdown(f'<div class="brief-card"><div class="brief-label">Must Include</div><div class="brief-value">{items}</div></div>', unsafe_allow_html=True)


def render_campaign(campaign: dict):
    pos = campaign.get("positioning", {})
    st.markdown(f"""
<div class="campaign-card">
  <div class="campaign-card-title">🎯 Core Positioning</div>
  <div style="font-size:1.05rem;font-weight:700;color:#e6edf3;margin-bottom:12px">{pos.get('statement','')}</div>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">
    {''.join(f'<span style="background:#21262d;border:1px solid #30363d;border-radius:6px;padding:6px 12px;font-size:0.85rem;color:#c9d1d9">{p}</span>' for p in pos.get('messaging_pillars',[]))}
  </div>
  <div style="font-size:0.8rem;color:#8b949e">Competitive hooks: {" · ".join(pos.get('competitive_hooks',[]))}</div>
</div>""", unsafe_allow_html=True)

    creative = campaign.get("creative", {})
    st.markdown("#### ✍️ Platform Creative")

    platform_configs = [
        ("📸 Instagram",         creative.get("instagram", {}),        ["hook", "body", "cta", "visual_direction"]),
        ("▶️ YouTube Pre-Roll",   creative.get("youtube_pre_roll", {}), ["hook", "script_outline", "visual_direction"]),
        ("🔍 Google Search Ad",   creative.get("google_search_ad", {}), ["headlines", "descriptions", "visual_direction"]),
        ("💬 WhatsApp Broadcast", creative.get("whatsapp_broadcast",{}),["message", "cta_button"]),
        ("🌐 D2C Website Banner", creative.get("d2c_website_banner",{}),["headline", "subhead", "cta", "visual_direction"]),
    ]

    for i in range(0, len(platform_configs), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(platform_configs):
                pname, pdata, pkeys = platform_configs[i + j]
                with col:
                    fields_html = ""
                    for k in pkeys:
                        val = pdata.get(k, "")
                        if isinstance(val, list):
                            val = " | ".join(val)
                        fields_html += f'<div class="copy-field"><div class="copy-label">{k.replace("_"," ").title()}</div><div class="copy-value">{val}</div></div>'
                    st.markdown(f'<div class="campaign-card"><div class="campaign-card-title">{pname}</div>{fields_html}</div>', unsafe_allow_html=True)

    # Channel plan
    ch = campaign.get("channel_plan", {})
    st.markdown("#### 📊 Channel Plan & Budget")
    st.markdown(f'<div class="brief-card"><div class="brief-label">Budget Logic</div><div class="brief-value">{ch.get("total_budget_allocation","")}</div></div>', unsafe_allow_html=True)

    channels_html = "".join(
        f'<div class="channel-row">'
        f'<div class="channel-pct">{c.get("budget_pct",0)}%</div>'
        f'<div class="channel-info"><div class="ch-name">{c.get("channel","")}</div>'
        f'<div class="ch-kpi">KPI: {c.get("kpi","")} · {c.get("cadence","")}</div></div>'
        f'</div>'
        for c in ch.get("channels", [])
    )
    st.markdown(f'<div class="campaign-card">{channels_html}</div>', unsafe_allow_html=True)

    ab_tests = ch.get("ab_testing", [])
    if ab_tests:
        st.markdown("#### 🧪 A/B Testing Recommendations")
        for test in ab_tests:
            st.markdown(f'<div class="brief-card"><div class="brief-value">🔬 {test}</div></div>', unsafe_allow_html=True)


# ── Main Layout ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🚀 RiteBite AI Marketing Co-Pilot</h1>
  <p>End-to-end autonomous pipeline: Research Agent → Analyst Agent → Campaign Creator Agent</p>
</div>""", unsafe_allow_html=True)

# Determine pipeline display state
has_intel    = "report" in st.session_state and st.session_state.report
has_brief    = "brief" in st.session_state and st.session_state.brief
has_campaign = "campaign" in st.session_state and st.session_state.campaign

if has_campaign:
    render_pipeline_header("complete")
elif has_brief:
    render_pipeline_header("orch_done")
elif has_intel:
    render_pipeline_header("intel_done")
else:
    render_pipeline_header("idle")

api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Competitor Selection ───────────────────────────────────────────────────────
st.markdown("""
<div class="stage-header">
  <div class="stage-badge">SELECT COMPETITOR</div>
  <div>
    <div class="stage-title">🎯 Choose a Competitor to Analyse</div>
    <div class="stage-sub">The full pipeline — Research Agent → Analyst Agent → Campaign Creator Agent — runs automatically</div>
  </div>
</div>""", unsafe_allow_html=True)

if "selected_competitor" not in st.session_state:
    st.session_state.selected_competitor = COMPETITORS[0]["name"]

cols = st.columns(len(COMPETITORS))
for col, comp in zip(cols, COMPETITORS):
    with col:
        if st.button(f"{comp['icon']}\n{comp['name']}\n{comp['tag']}", key=f"btn_{comp['name']}", use_container_width=True):
            st.session_state.selected_competitor = comp["name"]
            st.session_state.pop("report", None)
            st.session_state.pop("brief", None)
            st.session_state.pop("campaign", None)
            st.rerun()

selected_info = next((c for c in COMPETITORS if c["name"] == st.session_state.selected_competitor), None)
if selected_info:
    tc = {"High": "#f85149", "Medium": "#d29922", "Low": "#3fb950"}
    color = tc.get(selected_info["threat"], "#8b949e")
    st.markdown(
        f"**Selected:** {selected_info['icon']} {selected_info['name']} &nbsp;"
        f"<span style='color:{color};font-weight:700'>▲ {selected_info['threat']} threat</span>",
        unsafe_allow_html=True,
    )

with st.expander("🔎 Or enter a custom competitor"):
    custom = st.text_input("Custom competitor", placeholder="e.g., Fast&Up, KIND Bars")
    if custom and st.button("Use this competitor", key="use_custom"):
        st.session_state.selected_competitor = custom.strip()
        for k in ("report", "brief", "campaign"):
            st.session_state.pop(k, None)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
competitor = st.session_state.selected_competitor

# ── Single Pipeline Button ─────────────────────────────────────────────────────
col_btn, col_info = st.columns([2, 3])
with col_btn:
    run_pipeline = st.button(
        f"🚀 Run AI Marketing Co-Pilot — {competitor}",
        key="run_pipeline",
        use_container_width=True,
    )
with col_info:
    st.markdown("""
<div style='background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 18px;font-size:0.85rem;color:#8b949e;'>
  <strong style='color:#e6edf3;'>Autonomous pipeline:</strong><br>
  🔬 Research Agent &nbsp;→&nbsp; 🧭 Analyst Agent &nbsp;→&nbsp; 🎨 Campaign Creator Agent<br>
  <strong style='color:#e6edf3;'>Model:</strong> Claude Sonnet 4.6 &nbsp;·&nbsp;
  <strong style='color:#e6edf3;'>Agents:</strong> 3 &nbsp;·&nbsp;
  <strong style='color:#e6edf3;'>Outputs:</strong> Intel report · Strategic brief · Full campaign package
</div>""", unsafe_allow_html=True)

# ── Pipeline Execution ─────────────────────────────────────────────────────────
if run_pipeline:
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY environment variable is not set.")
    else:
        for k in ("report", "brief", "campaign"):
            st.session_state.pop(k, None)

        pipeline_ok = True
        with st.status("🚀 Running AI Marketing Co-Pilot...", expanded=True) as status:

            # Stage 1: Research Agent
            st.write(f"🔬 **Research Agent** — analysing *{competitor}*...")
            try:
                st.session_state.report = run_intel_agent(competitor, api_key)
                threat = st.session_state.report.get("threat_level", "")
                st.write(f"✅ Research Agent complete — Threat level: **{threat}**")
            except Exception as e:
                st.error(f"❌ Research Agent error: {e}")
                status.update(label="Pipeline failed at Research Agent", state="error")
                pipeline_ok = False

            # Stage 2: Analyst Agent
            if pipeline_ok:
                st.write("🧭 **Analyst Agent** — triaging signal and building strategic brief...")
                try:
                    st.session_state.brief = run_orchestrator(st.session_state.report, api_key)
                    triage = st.session_state.brief.get("orchestrator_decisions", {}).get("triage_result", "")
                    posture = st.session_state.brief.get("orchestrator_decisions", {}).get("strategic_posture", "")
                    st.write(f"✅ Analyst Agent complete — Triage: **{triage}** · Posture: **{posture}**")
                except Exception as e:
                    st.error(f"❌ Analyst Agent error: {e}")
                    status.update(label="Pipeline failed at Analyst Agent", state="error")
                    pipeline_ok = False

            # Stage 3: Campaign Creator Agent (skipped if MONITOR_ONLY)
            if pipeline_ok:
                triage = st.session_state.brief.get("orchestrator_decisions", {}).get("triage_result", "")
                if triage == "MONITOR_ONLY":
                    st.write("👁️ **Campaign Creator Agent** — skipped (triage result: MONITOR ONLY)")
                    status.update(
                        label="Pipeline complete — no campaign warranted (Monitor Only)",
                        state="complete",
                    )
                else:
                    st.write("🎨 **Campaign Creator Agent** — generating full campaign package...")
                    try:
                        st.session_state.campaign = run_campaign_creator(st.session_state.brief, api_key)
                        campaign_name = st.session_state.campaign.get("campaign_name", "")
                        st.write(f"✅ Campaign Creator Agent complete — *{campaign_name}*")
                        status.update(
                            label=f"✅ Pipeline complete — full campaign package ready",
                            state="complete",
                        )
                    except Exception as e:
                        st.error(f"❌ Campaign Creator Agent error: {e}")
                        status.update(label="Pipeline failed at Campaign Creator Agent", state="error")

        # Refresh state flags after execution
        has_intel    = "report" in st.session_state and st.session_state.report
        has_brief    = "brief" in st.session_state and st.session_state.brief
        has_campaign = "campaign" in st.session_state and st.session_state.campaign

# ── Results: idle placeholder ──────────────────────────────────────────────────
if not has_intel and not run_pipeline:
    st.markdown("""
<div class="loading-box">
  <div class="loading-title">Ready to run</div>
  <div class="loading-sub">Select a competitor above and click <strong>Run AI Marketing Co-Pilot</strong>.</div>
</div>""", unsafe_allow_html=True)

# ── STAGE 1 Results: Research Agent ───────────────────────────────────────────
if has_intel:
    st.markdown("""
<div class="stage-header">
  <div class="stage-badge">RESEARCH AGENT</div>
  <div>
    <div class="stage-title">🔍 Competitive Intelligence Research Agent</div>
    <div class="stage-sub">Structured intelligence report</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("## 📄 Intelligence Report")
    render_intel_report(st.session_state.report)

    pdf_bytes = generate_intel_pdf(st.session_state.report)
    st.download_button(
        label="⬇️ Download Intelligence Report PDF",
        data=pdf_bytes,
        file_name=f"intel_{competitor.replace(' ','_').lower()}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        key="dl_intel",
    )

# ── STAGE 2 Results: Analyst Agent ────────────────────────────────────────────
if has_brief:
    st.markdown("""
<div class="stage-header">
  <div class="stage-badge">ANALYST AGENT</div>
  <div>
    <div class="stage-title">🧭 Strategic Analyst Agent</div>
    <div class="stage-sub">Signal triage · Strategic posture · ICP routing · Campaign brief</div>
  </div>
</div>""", unsafe_allow_html=True)

    brief = st.session_state.brief
    triage = brief.get("orchestrator_decisions", {}).get("triage_result", "")

    st.markdown("## 🧭 Analyst Agent Brief")
    render_orchestrator_brief(brief)

    if triage == "MONITOR_ONLY":
        st.markdown("""
<div class="triage-monitor" style="text-align:center;padding:24px;margin-top:16px">
  <div style="font-size:1.2rem;font-weight:700;margin-bottom:8px">👁️ MONITOR ONLY</div>
  <div style="font-size:0.9rem">This signal does not warrant a campaign response.
  The report has been logged for future reference. No campaign will be generated.</div>
</div>""", unsafe_allow_html=True)

# ── STAGE 3 Results: Campaign Creator Agent ───────────────────────────────────
if has_campaign:
    st.markdown("""
<div class="stage-header">
  <div class="stage-badge">CAMPAIGN CREATOR AGENT</div>
  <div>
    <div class="stage-title">🎨 Campaign Creator Agent</div>
    <div class="stage-sub">Full campaign package: positioning · copy · visual direction · channel plan</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"## 🎯 Campaign Package: *{st.session_state.campaign.get('campaign_name','')}*")
    st.markdown(f"<div style='color:#8b949e;font-size:0.9rem;margin-bottom:20px'>{st.session_state.campaign.get('competitive_context','')}</div>", unsafe_allow_html=True)
    render_campaign(st.session_state.campaign)

    # Full pipeline PDF — all three agents
    st.markdown("<br>", unsafe_allow_html=True)
    full_pdf = generate_full_report_pdf(st.session_state.report, st.session_state.brief, st.session_state.campaign)
    st.download_button(
        label="⬇️ Download Full Report PDF (Research Agent + Analyst Agent + Campaign Creator Agent)",
        data=full_pdf,
        file_name=f"ritebite_full_report_{competitor.replace(' ','_').lower()}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        key="dl_campaign",
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#30363d;margin-top:48px'>
<p style='text-align:center;color:#484f58;font-size:0.8rem;'>
  RiteBite Max Protein · AI Marketing Pipeline · Research Agent + Analyst Agent + Campaign Creator Agent ·
  AI Tooling for Product Marketing · ISB Term 7
</p>""", unsafe_allow_html=True)
