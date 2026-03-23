# Prototype D: AI Campaign Creator Agent — Multi-Step Campaign Generation Pipeline

**Brand:** RiteBite Max Protein (Naturell India / Zydus Wellness)
**Course:** AI Tooling for Product Marketing — Term 7 Elective, ISB
**Prototype Option:** Option D — AI Campaign Creator Agent

---

## 1. Objective

This prototype demonstrates how an autonomous, multi-step AI agent can compress the entire campaign creation lifecycle — from competitive research intake to final channel-specific creative output — into a single automated pipeline. The agent receives structured competitive intelligence as input (from the Competitive Intelligence Scout, Prototype A) and executes a sequential workflow across four stages: Strategic Positioning, Copy Generation, Visual Direction, and Channel Plan. The result is a ready-to-deploy campaign brief with platform-specific ad copy, creative direction, and budget allocation — produced in under 60 seconds versus the weeks-long cycle of traditional agency workflows.

## 2. AI Architecture

The Campaign Creator Agent follows a **multi-step agentic workflow** — a chained sequence of specialized LLM calls where each stage's output becomes the next stage's input. This is fundamentally different from a single-prompt chatbot because the agent maintains state across stages and applies distinct reasoning modes at each step.

### Pipeline Stages

| Stage | Input | Processing | Output |
|-------|-------|------------|--------|
| **Stage 1: Strategic Positioning** | Competitive intelligence report (from Prototype A) + campaign brief parameters (objective, target segment, product focus) | Analyzes competitor vulnerabilities, identifies white-space positioning opportunities, defines the campaign's core strategic angle | Positioning statement, key messaging pillars, competitive differentiation hooks |
| **Stage 2: Copy Generation** | Positioning output + brand voice guidelines | Generates platform-specific ad copy fine-tuned to RiteBite's energetic, culturally relevant tone across multiple formats | Headline variants, body copy, CTAs for Instagram, YouTube, Google Ads, WhatsApp, and D2C website banners |
| **Stage 3: Visual & Creative Direction** | Positioning output + copy output + brand identity parameters | Produces detailed creative briefs describing visual concepts, mood, color palette, talent direction, and shot composition for each platform | Visual direction document with platform-specific creative specs |
| **Stage 4: Channel Plan & Budget Allocation** | Full campaign package + target ICP segment data + historical channel performance benchmarks | Allocates budget across channels, defines KPIs per channel, sets A/B testing framework, and projects expected performance | Channel-wise budget split, posting cadence, KPI targets, testing matrix |

### AI Type Justification

This prototype uses a **Multi-Agent Orchestration** pattern implemented as a sequential chain. Each stage operates as a conceptually distinct "agent" with its own system prompt, reasoning constraints, and output schema. This approach is chosen over a single monolithic prompt because:

- **Separation of concerns:** Strategic positioning requires analytical reasoning; copy generation requires creative fluency; channel planning requires quantitative allocation logic. A single prompt cannot optimize for all three cognitive modes simultaneously.
- **State accumulation:** Each stage builds on the previous stage's output, creating a compounding context that produces increasingly specific and actionable deliverables.
- **Quality control checkpoints:** In production, a human reviewer could inspect and edit the output at any stage before it flows downstream, implementing the Human-in-the-Loop (HITL) principle from the GTM strategy's ethical risk framework.
- **Modularity:** Individual stages can be swapped, reordered, or parallelized without rewriting the entire pipeline.

## 3. Integration with Prototype A (Competitive Intelligence Scout)

The Campaign Creator Agent is designed to consume the structured JSON output of the Competitive Intelligence Scout as its primary input. This creates a closed-loop intelligence-to-execution pipeline:

```
Competitive Intelligence Scout (Prototype A)
    │
    ├── competitor: "The Whole Truth Foods"
    ├── threat_level: "High"
    ├── sections:
    │     ├── Product & Pricing Moves → informs positioning differentiation
    │     ├── Digital & Campaign Strategy → informs counter-messaging
    │     ├── Consumer Sentiment → informs objection pre-emption
    │     └── Distribution & Channel Expansion → informs channel prioritization
    └── strategic_recommendations → seeds the campaign's strategic angle
            │
            ▼
    Campaign Creator Agent (Prototype D)
        │
        ├── Stage 1: Positioning (uses competitor vulnerabilities + recommendations)
        ├── Stage 2: Copy (applies positioning to brand-voice-aligned creative)
        ├── Stage 3: Visual Direction (translates copy into creative specs)
        └── Stage 4: Channel Plan (allocates budget informed by competitor channel mix)
```

### What the Agent Extracts from the Intelligence Report

| Intelligence Report Field | How the Campaign Agent Uses It |
|---------------------------|-------------------------------|
| `executive_summary` | Sets the competitive context for the positioning stage |
| `sections[0]: Product & Pricing Moves` | Identifies competitor pricing gaps and new SKUs to counter-position against |
| `sections[1]: Digital & Campaign Strategy` | Reveals competitor messaging themes to differentiate from or directly counter |
| `sections[2]: Consumer Sentiment` | Surfaces unmet consumer needs or complaints that the campaign can address |
| `sections[3]: Distribution & Channel Expansion` | Informs geo-targeting and channel prioritization in the budget allocation |
| `threat_level` + `threat_rationale` | Determines campaign urgency and aggressiveness of competitive messaging |
| `strategic_recommendations` | Directly seeds the campaign's strategic angle and messaging pillars |

## 4. System Prompt Design

The agent uses a master system prompt that defines the full four-stage pipeline, with stage-specific instructions embedded within:

### Brand Voice Constraints (Applied Across All Stages)

The prompt encodes RiteBite's established brand personality:

- **Tone:** Energetic, motivational, never preachy or clinical
- **Cultural register:** Young urban Indian, code-switching between English and Hindi naturally (e.g., "Protein ka Punch")
- **Campaign DNA references:** "Protein Salute" (breaking procrastination), "Protein Aayega Tabhi India Khayega" (cultural embedding), Mumbai Metro activation (experiential disruption)
- **Forbidden patterns:** Generic health-food clichés, guilt-based messaging, aggressive competitor bashing (the brand educates rather than attacks)

### Output Schema

```json
{
  "campaign_name": "string",
  "competitive_context": "string (2-3 sentences summarizing the intelligence input)",
  "positioning": {
    "statement": "string (1 sentence core positioning)",
    "messaging_pillars": ["string", "string", "string"],
    "competitive_hooks": ["string (specific differentiation points vs. the competitor)"]
  },
  "creative": {
    "instagram": {
      "hook": "string (first 3 seconds / first line)",
      "body": "string",
      "cta": "string",
      "visual_direction": "string (mood, color, talent, composition)"
    },
    "youtube_pre_roll": {
      "hook": "string (first 5 seconds)",
      "script_outline": "string (15-second script structure)",
      "visual_direction": "string"
    },
    "google_search_ad": {
      "headlines": ["string (max 30 chars)", "string", "string"],
      "descriptions": ["string (max 90 chars)", "string"],
      "visual_direction": "string"
    },
    "whatsapp_broadcast": {
      "message": "string (under 160 chars)",
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
    "total_budget_allocation": "string (description of split logic)",
    "channels": [
      {
        "channel": "string",
        "budget_pct": "number",
        "objective": "string",
        "kpi": "string",
        "cadence": "string"
      }
    ],
    "ab_testing": ["string (what to test)", "string"]
  }
}
```

## 5. Campaign Configuration Parameters

Beyond the intelligence report input, the agent accepts configuration parameters that allow the marketing team to steer the campaign:

| Parameter | Options | Effect on Pipeline |
|-----------|---------|-------------------|
| **Campaign Objective** | Awareness, Consideration, Conversion, Retention | Shifts the channel mix and messaging tone (awareness = broad reach + educational; conversion = retargeting + urgency) |
| **Target Segment** | Fitness Enthusiast, Busy Professional, Mindful Snacker, New-to-Protein | Selects the psychographic framing, channel preferences, and product focus |
| **Product Focus** | Specific SKU or product line (e.g., Millet Wafer Bars, 20g Active Bars) | Anchors the creative around a specific product's nutritional claims and consumption occasion |
| **Campaign Tone** | Counter-competitive, Educational, Experiential, Promotional | Determines how aggressively the campaign references competitor weaknesses vs. focusing on RiteBite's own value proposition |
| **Budget Tier** | Low (₹5L), Medium (₹15L), High (₹40L+) | Adjusts channel diversification and production ambition in the creative direction |

## 6. Business Metrics Addressed

| Metric | Impact | Mechanism |
|--------|--------|-----------|
| **Time-to-Launch** | Reduction from 3–6 weeks to under 24 hours for campaign brief generation | Four-stage pipeline compresses research, positioning, creative, and planning into a single automated flow |
| **Creative Velocity** | 10x increase in variant generation for A/B testing | Agent produces platform-specific copy and visual direction simultaneously across 5+ channels |
| **Marketing ROI** | Improved through data-driven channel allocation | Budget split informed by competitive intelligence rather than historical inertia |
| **Click-Through Rate (CTR)** | Improved through competitive differentiation in messaging | Positioning stage explicitly identifies white-space opportunities the competitor isn't addressing |
| **Cost Reduction** | Reduced agency dependency for routine campaign ideation | Internal team uses agent output as high-quality first drafts, reserving agency budgets for flagship campaigns |

## 7. Demonstration Flow

For the presentation, the recommended demo sequence is:

1. **Recap the Prototype A output** — show or reference the competitive intelligence report generated for The Whole Truth Foods
2. **Show the intelligence flowing in** — the Campaign Creator Agent receives the structured report as input, not raw text
3. **Configure campaign parameters** — select "Counter-competitive" tone, "Mindful Snacker" target, "Millet Wafer Bars" product focus (this is the product line most vulnerable to The Whole Truth's clean-label attack)
4. **Run the pipeline** and narrate each stage as it completes:
   - Stage 1: "The agent identified that The Whole Truth's pricing is 3x higher — this becomes a positioning hook"
   - Stage 2: "Copy is generated in RiteBite's voice, not generic marketing speak"
   - Stage 3: "Visual direction references the brand's proven experiential playbook"
   - Stage 4: "Budget allocation over-indexes on Instagram and quick-commerce where the Mindful Snacker segment is most active"
5. **Highlight the A/B testing recommendations** — the agent doesn't just create one campaign, it proposes what to test

## 8. Ethical Safeguards

### Brand Misalignment Prevention
The system prompt includes explicit "Do's and Don'ts" extracted from RiteBite's brand playbook. Every generated copy variant is constrained to the brand's established tonal register. In production, all creative output would pass through a human brand manager review before deployment — the agent generates first drafts, not final approvals.

### Competitive Ethics
The agent is explicitly instructed to never produce copy that makes false claims about competitors, uses disparaging language, or references competitor brand names directly in consumer-facing creative. Competitive differentiation is framed positively ("RiteBite's Date & Almond Bar is naturally sweetened with dates") rather than negatively ("Competitor X uses artificial sweeteners").

### Over-Automation Risk
The four-stage pipeline is designed with inspection checkpoints between each stage. The HITL architecture ensures the marketing team reviews strategic positioning before copy is generated, and reviews copy before channel allocation is computed. The agent augments human creativity rather than replacing it.

## 9. Limitations & Future Enhancements

### Current Limitations
- Single LLM call simulates the four-stage pipeline; production would use separate specialized calls per stage
- Visual direction is text-based; does not generate actual images or mockups
- Channel budget allocation uses heuristic reasoning rather than historical performance data
- No integration with ad platform APIs for direct creative deployment

### Production Enhancements
- **Stage parallelization:** Copy and visual direction stages run concurrently to reduce total pipeline latency
- **Multimodal creative generation:** Integration with image generation models (DALL-E, Midjourney API) to produce actual ad creatives alongside copy
- **Live budget optimization:** Connect to Meta Ads Manager and Google Ads APIs for real-time bid adjustment based on campaign performance
- **Feedback loop:** Post-campaign performance data (CTR, CPC, conversion rates) feeds back into the positioning stage, continuously improving the agent's strategic recommendations
- **Multi-language support:** Auto-generate Hindi, Tamil, Telugu, and Marathi variants of all copy for regional quick-commerce targeting
- **Integration with Task 4 (Influencer Agent):** Campaign output automatically triggers influencer outreach with pre-generated creator briefs and talking points

## 10. Connection to GTM Strategy

This prototype directly implements **Task 3: Automated Multimodal Campaign Creation and Velocity Testing** from the AI Opportunity Map:

> *"The creation of marketing campaigns involves highly siloed workflows across copywriting, graphic design, positioning strategy, and channel planning. This traditional methodology creates a massive bottleneck, with campaign development cycles stretching across weeks or months."*

The Campaign Creator Agent collapses these silos into a single automated pipeline. More critically, by consuming the Competitive Intelligence Scout's output as its input, it demonstrates the architectural principle from the GTM strategy — that AI agents should not operate as isolated point solutions but as interconnected nodes in a unified orchestration layer.

The agent maps to **Layer 2 (Orchestration and Intelligence Layer)** in the proposed architecture, where the Multi-Agent Orchestration Framework delegates campaign creation tasks to specialized sub-agents while maintaining strategic coherence through shared context.

---

*Prototype built with React + Anthropic Claude API. Designed for the AI Tooling for Product Marketing group project, ISB.*
