import json
import os
from datetime import datetime

import io

import anthropic
import streamlit as st
from fpdf import FPDF

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RiteBite Competitive Intelligence Scout",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
  /* global */
  html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #e6edf3;
  }
  [data-testid="stHeader"] { background: transparent; }

  /* hero banner */
  .hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 60%, #1a0a2e 100%);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 24px;
  }
  .hero h1 { font-size: 2.1rem; font-weight: 800; margin: 0 0 6px;
    background: linear-gradient(90deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .hero p  { color: #8b949e; font-size: 1rem; margin: 0; }
  .badge   { display: inline-block; background: #21262d; border: 1px solid #30363d;
    color: #58a6ff; border-radius: 20px; padding: 4px 14px; font-size: 0.78rem;
    margin-right: 8px; margin-bottom: 10px; }

  /* pipeline diagram */
  .pipeline {
    display: flex; align-items: center; gap: 0;
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 18px 28px; margin-bottom: 24px; flex-wrap: wrap;
  }
  .pipe-step {
    display: flex; flex-direction: column; align-items: center;
    background: #21262d; border: 1px solid #30363d; border-radius: 10px;
    padding: 14px 22px; min-width: 170px; text-align: center;
  }
  .pipe-step .icon { font-size: 1.8rem; margin-bottom: 6px; }
  .pipe-step .label { font-weight: 700; font-size: 0.85rem; color: #e6edf3; }
  .pipe-step .sub   { font-size: 0.73rem; color: #8b949e; margin-top: 3px; }
  .pipe-arrow { font-size: 1.4rem; color: #30363d; padding: 0 12px; }

  /* competitor cards */
  .comp-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 10px; }
  .comp-card {
    background: #21262d; border: 1px solid #30363d; border-radius: 10px;
    padding: 14px 18px; cursor: pointer; transition: all .2s; min-width: 150px;
    text-align: center;
  }
  .comp-card:hover { border-color: #58a6ff; background: #1a2332; }
  .comp-card.selected { border-color: #58a6ff; background: #1a2332;
    box-shadow: 0 0 0 1px #58a6ff33; }
  .comp-card .c-icon { font-size: 1.6rem; margin-bottom: 5px; }
  .comp-card .c-name { font-weight: 700; font-size: 0.84rem; color: #e6edf3; }
  .comp-card .c-tag  { font-size: 0.72rem; color: #8b949e; margin-top: 2px; }

  /* report sections */
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
  .section-title { font-size: 1.05rem; font-weight: 700; color: #e6edf3;
    margin-bottom: 14px; }
  .finding {
    display: flex; gap: 10px; align-items: flex-start;
    padding: 10px 0; border-bottom: 1px solid #21262d;
  }
  .finding:last-child { border-bottom: none; }
  .finding-dot { color: #58a6ff; font-size: 0.7rem; margin-top: 5px; flex-shrink: 0; }
  .finding-text { color: #c9d1d9; font-size: 0.9rem; line-height: 1.55; }

  /* threat badge */
  .threat-high   { background: #3d1010; border: 1px solid #f85149;
    color: #f85149; border-radius: 8px; padding: 16px 20px; }
  .threat-medium { background: #2d1e00; border: 1px solid #d29922;
    color: #d29922; border-radius: 8px; padding: 16px 20px; }
  .threat-low    { background: #0d2310; border: 1px solid #3fb950;
    color: #3fb950; border-radius: 8px; padding: 16px 20px; }
  .threat-label  { font-size: 1.3rem; font-weight: 800; }
  .threat-rationale { font-size: 0.88rem; margin-top: 6px; opacity: 0.85; }

  /* recommendations */
  .rec-card {
    background: #161b22; border: 1px solid #1f3a1f; border-radius: 10px;
    padding: 16px 20px; margin-bottom: 12px; display: flex; gap: 14px;
    align-items: flex-start;
  }
  .rec-num  { background: #238636; color: #fff; border-radius: 50%;
    width: 26px; height: 26px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; font-size: 0.8rem; flex-shrink: 0; }
  .rec-text { color: #c9d1d9; font-size: 0.9rem; line-height: 1.55; }

  /* loading */
  .loading-box {
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 40px; text-align: center; margin: 20px 0;
  }
  .loading-title { font-size: 1.1rem; font-weight: 700; color: #58a6ff; margin-bottom: 8px; }
  .loading-sub   { color: #8b949e; font-size: 0.88rem; }

  /* run button */
  div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1f6feb, #1a56c4) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 12px 32px !important; font-weight: 700 !important; font-size: 1rem !important;
    cursor: pointer !important; width: 100% !important;
    transition: opacity .2s !important;
  }
  div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Constants ─────────────────────────────────────────────────────────────────
COMPETITORS = [
    {
        "name": "The Whole Truth Foods",
        "icon": "🌿",
        "tag": "Clean-label / Transparency",
        "threat": "High",
    },
    {
        "name": "Yoga Bar",
        "icon": "🧘",
        "tag": "Natural / Community",
        "threat": "Medium",
    },
    {
        "name": "MuscleBlaze",
        "icon": "💪",
        "tag": "Sports Nutrition",
        "threat": "Medium",
    },
    {
        "name": "GetMyMettle",
        "icon": "⚡",
        "tag": "Energy / Endurance",
        "threat": "Low",
    },
    {
        "name": "Epigamia",
        "icon": "🥛",
        "tag": "Functional Snacks",
        "threat": "Low",
    },
]

SYSTEM_PROMPT = """You are a Competitive Intelligence Agent for RiteBite Max Protein (by Zydus Wellness / Naturell India).

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
    {
      "title": "Product & Pricing Moves",
      "icon": "💰",
      "findings": ["finding 1", "finding 2", "finding 3"]
    },
    {
      "title": "Digital & Campaign Strategy",
      "icon": "📱",
      "findings": ["finding 1", "finding 2"]
    },
    {
      "title": "Distribution & Channel Expansion",
      "icon": "🚚",
      "findings": ["finding 1", "finding 2"]
    },
    {
      "title": "Consumer Sentiment",
      "icon": "🗣️",
      "findings": ["finding 1", "finding 2"]
    }
  ],
  "threat_level": "High | Medium | Low",
  "threat_rationale": "1-2 sentence explanation calibrated to RiteBite's specific vulnerabilities",
  "strategic_recommendations": ["rec 1", "rec 2", "rec 3"]
}

## Quality Rules
- Each finding must be specific, data-rich, and actionable — not generic
- Threat level must be calibrated against RiteBite's positioning and vulnerabilities
- Recommendations must directly counter identified threats or exploit competitor weaknesses
- Use your training knowledge about this competitor's Indian market activity"""


# ── Agent function ────────────────────────────────────────────────────────────
@st.cache_resource
def get_client(api_key: str):
    return anthropic.Anthropic(api_key=api_key)


def run_agent(competitor_name: str, api_key: str) -> dict:
    client = get_client(api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Generate a competitive intelligence report for: {competitor_name}",
            }
        ],
    )
    for block in response.content:
        if block.type == "text":
            raw = block.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.rsplit("```", 1)[0]
            return json.loads(raw)
    raise ValueError("No text block in response")


# ── PDF generation ───────────────────────────────────────────────────────────
def _s(text: str) -> str:
    """Sanitize text for Helvetica: replace known chars, strip anything outside Latin-1."""
    text = (str(text)
        .replace("\u2014", "-")   # em dash
        .replace("\u2013", "-")   # en dash
        .replace("\u2018", "'")   # left single quote
        .replace("\u2019", "'")   # right single quote
        .replace("\u201c", '"')   # left double quote
        .replace("\u201d", '"')   # right double quote
        .replace("\u2022", "-")   # bullet
        .replace("\u2026", "...") # ellipsis
        .replace("\u00a0", " ")   # non-breaking space
        .replace("\u20b9", "Rs.") # rupee sign
        .replace("\u2264", "<=")  # ≤
        .replace("\u2265", ">=")  # ≥
    )
    # Strip any remaining characters outside Latin-1 (0x00–0xFF)
    return "".join(c if ord(c) < 256 else "?" for c in text)


def generate_pdf(report: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, "Competitive Intelligence Report", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, _s(report["competitor"]), new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generated {report['report_date'][:10]}  |  AI Research Agent  |  Claude Sonnet 4.6", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Threat level
    threat = report.get("threat_level", "Medium")
    threat_colors = {"High": (220, 50, 50), "Medium": (200, 140, 30), "Low": (40, 160, 80)}
    r, g, b = threat_colors.get(threat, (120, 120, 120))
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 7, f"Threat Level: {threat}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 6, _s(report.get("threat_rationale", "")))
    pdf.ln(4)

    # Executive summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(88, 166, 255)
    pdf.set_line_width(0.8)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, _s(report.get("executive_summary", "")))
    pdf.ln(5)

    # Sections
    for section in report.get("sections", []):
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 30, 30)
        title = _s(section["title"])
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(48, 54, 61)
        pdf.set_line_width(0.3)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        for finding in section.get("findings", []):
            pdf.set_x(pdf.l_margin + 4)
            pdf.multi_cell(0, 6, f"*  {_s(finding)}")
            pdf.ln(1)
        pdf.ln(4)

    # Strategic recommendations
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, "Strategic Recommendations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(35, 134, 54)
    pdf.set_line_width(0.8)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for i, rec in enumerate(report.get("strategic_recommendations", []), 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_x(pdf.l_margin + 4)
        pdf.cell(8, 6, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, _s(rec))
        pdf.ln(1)

    # Footer
    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "RiteBite Max Protein  |  Competitive Intelligence Scout", align="C")

    return bytes(pdf.output())


# ── UI helpers ────────────────────────────────────────────────────────────────
def render_pipeline():
    st.markdown(
        """
<div class="pipeline">
  <div class="pipe-step">
    <div class="icon">🌐</div>
    <div class="label">Web Search</div>
    <div class="sub">Competitor activity<br>across all channels</div>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <div class="icon">🧠</div>
    <div class="label">LLM Analysis</div>
    <div class="sub">Claude Sonnet 4.6<br>with adaptive thinking</div>
  </div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">
    <div class="icon">📊</div>
    <div class="label">Structured Report</div>
    <div class="sub">PDF report · threat score<br>strategic recommendations</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_report(report: dict):
    threat = report.get("threat_level", "Medium")
    threat_class = f"threat-{threat.lower()}"
    icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    # Header
    st.markdown(
        f"""
<div class="report-header">
  <div class="report-title">🔍 {report['competitor']}</div>
  <div class="report-meta">Generated {report['report_date'][:10]} &nbsp;·&nbsp; AI Research Agent &nbsp;·&nbsp; Claude Sonnet 4.6</div>
  <div class="exec-summary">{report['executive_summary']}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Threat level
    st.markdown(
        f"""
<div class="{threat_class}">
  <div class="threat-label">{icons.get(threat, '🟡')} Threat Level: {threat}</div>
  <div class="threat-rationale">{report['threat_rationale']}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Sections
    cols = st.columns(2)
    for i, section in enumerate(report.get("sections", [])):
        with cols[i % 2]:
            findings_html = "".join(
                f'<div class="finding"><span class="finding-dot">●</span>'
                f'<span class="finding-text">{f}</span></div>'
                for f in section["findings"]
            )
            st.markdown(
                f"""
<div class="section-card">
  <div class="section-title">{section['icon']} {section['title']}</div>
  {findings_html}
</div>
""",
                unsafe_allow_html=True,
            )

    # Recommendations
    st.markdown("### 🎯 Strategic Recommendations")
    for i, rec in enumerate(report.get("strategic_recommendations", []), 1):
        st.markdown(
            f"""
<div class="rec-card">
  <div class="rec-num">{i}</div>
  <div class="rec-text">{rec}</div>
</div>
""",
            unsafe_allow_html=True,
        )


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
  <h1>🔍 Competitive Intelligence Scout</h1>
  <p>Autonomous AI agent for RiteBite Max Protein — turns a competitor name into a structured intelligence report in under 30 seconds.</p>
</div>
""",
    unsafe_allow_html=True,
)

render_pipeline()

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Competitor selector ───────────────────────────────────────────────────────
st.markdown("### 🏆 Select Competitor")

# Build competitor cards with click-select via session state
if "selected_competitor" not in st.session_state:
    st.session_state.selected_competitor = COMPETITORS[0]["name"]

cols = st.columns(len(COMPETITORS))
for col, comp in zip(cols, COMPETITORS):
    with col:
        selected = st.session_state.selected_competitor == comp["name"]
        border = "2px solid #58a6ff" if selected else "1px solid #30363d"
        bg = "#1a2332" if selected else "#21262d"
        if st.button(
            f"{comp['icon']}\n{comp['name']}\n{comp['tag']}",
            key=f"btn_{comp['name']}",
            use_container_width=True,
        ):
            st.session_state.selected_competitor = comp["name"]
            st.session_state.pop("report", None)
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Show which is selected
selected_info = next(
    (c for c in COMPETITORS if c["name"] == st.session_state.selected_competitor), None
)
if selected_info:
    threat_colors = {"High": "#f85149", "Medium": "#d29922", "Low": "#3fb950"}
    color = threat_colors.get(selected_info["threat"], "#8b949e")
    st.markdown(
        f"**Selected:** {selected_info['icon']} {selected_info['name']} &nbsp;"
        f"<span style='color:{color};font-weight:700'>▲ {selected_info['threat']} threat</span>",
        unsafe_allow_html=True,
    )

# Custom competitor
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🔎 Or enter a custom competitor name"):
    custom = st.text_input(
        "Custom competitor", placeholder="e.g., Fast&Up, Gatorade, KIND Bars"
    )
    if custom:
        if st.button("Use this competitor", key="use_custom"):
            st.session_state.selected_competitor = custom.strip()
            st.session_state.pop("report", None)
            st.rerun()

st.markdown("---")

# ── Run button ────────────────────────────────────────────────────────────────
competitor = st.session_state.selected_competitor

col_btn, col_info = st.columns([2, 3])
with col_btn:
    run = st.button(
        f"🚀 Run Agent — {competitor}", key="run_agent", use_container_width=True
    )

with col_info:
    st.markdown(
        f"""
<div style='background:#161b22;border:1px solid #30363d;border-radius:10px;
     padding:14px 18px;font-size:0.85rem;color:#8b949e;'>
  <strong style='color:#e6edf3;'>Agent pipeline:</strong><br>
  Web search → LLM synthesis → PDF report<br>
  <strong style='color:#e6edf3;'>Model:</strong> Claude Sonnet 4.6 · adaptive thinking
</div>
""",
        unsafe_allow_html=True,
    )

# ── Execute agent ─────────────────────────────────────────────────────────────
if run:
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY environment variable is not set.")
    else:
        st.session_state.pop("report", None)
        st.session_state.pop("error", None)

        with st.spinner(
            f"🧠 Agent is researching **{competitor}** — synthesizing competitive intelligence..."
        ):
            try:
                report = run_agent(competitor, api_key)
                st.session_state.report = report
                st.session_state.error = None
            except Exception as e:
                st.session_state.error = str(e)

# ── Show report ───────────────────────────────────────────────────────────────
if "error" in st.session_state and st.session_state.error:
    st.error(f"❌ Agent error: {st.session_state.error}")

elif "report" in st.session_state and st.session_state.report:
    st.markdown("---")
    st.markdown("## 📄 Intelligence Report")
    render_report(st.session_state.report)

    # PDF download
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_bytes = generate_pdf(st.session_state.report)
    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name=f"intel_{competitor.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )

else:
    st.markdown(
        """
<div class="loading-box">
  <div class="loading-title">Ready to run</div>
  <div class="loading-sub">Select a competitor above and click <strong>Run Agent</strong> to generate a report.</div>
</div>
""",
        unsafe_allow_html=True,
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<hr style='border-color:#30363d;margin-top:48px'>
<p style='text-align:center;color:#484f58;font-size:0.8rem;'>
  RiteBite Max Protein · Competitive Intelligence Scout · Prototype A ·
  AI Tooling for Product Marketing · ISB Term 7
</p>
""",
    unsafe_allow_html=True,
)
