# Prototype B: AI Recommendation Flow — Abandoned Cart Recovery + Objection Handler

**Brand:** RiteBite Max Protein (Naturell India / Zydus Wellness)
**Course:** AI Tooling for Product Marketing — Term 7 Elective, ISB
**Prototype Option:** Option B — AI Recommendation Flow

---

## 1. Objective

This prototype demonstrates how a hybrid AI system — combining a Recommendation Engine with an Agentic RAG (Retrieval-Augmented Generation) architecture — can simultaneously handle customer objections with factual accuracy and deliver hyper-personalized product recommendations. The system recovers abandoned carts by weaving product education, personalized suggestions, and contextual incentives into a single conversational flow.

## 2. AI Architecture

The prototype implements a four-stage pipeline that mirrors the production architecture proposed in the GTM strategy document:

| Stage | Function | Technology |
|-------|----------|------------|
| **Customer Data Ingestion** | Loads the user's full behavioral profile from the CDP — demographics, purchase history, abandoned cart, session context, dietary preferences | Simulated Customer Data Platform (CSV concept) |
| **RAG Retrieval** | When the customer raises an objection or question, the system queries a vector database of approved nutritional profiles, FSSAI compliance docs, and brand guidelines to retrieve factual grounding | Agentic RAG with semantic search |
| **LLM + Recommendation Engine** | The LLM synthesizes retrieved facts with the recommendation algorithm's output (collaborative filtering on past purchases + contextual signals) to generate a personalized, brand-voice-aligned response | Claude Sonnet 4 with structured JSON output |
| **Conversational Delivery** | The response is rendered as a natural chat interaction with embedded product cards, incentive offers, and a clear call-to-action | React frontend with dynamic rendering |

### AI Type Justification

This prototype combines two AI types from the GTM strategy:

**1. Hybrid Recommendation Engine (Task 1)** — Uses collaborative filtering logic to match the customer's historical flavor preferences, purchase cadence, and browsing behavior against the product catalog. The algorithm generates high-confidence SKU recommendations that feel bespoke rather than generic.

**2. Agentic RAG (Task 2)** — Grounds all nutritional claims in verified corporate knowledge, eliminating hallucination risk. When a customer asks about artificial sweeteners, sugar content, or ingredient comparisons, the agent retrieves facts from the approved knowledge base rather than generating plausible-sounding but potentially incorrect information.

## 3. Simulated Customer Profiles

The prototype includes four customer profiles representing the ICP archetypes defined in the GTM document:

### Profile 1: Arjun Mehta — Busy Professional
| Attribute | Value |
|-----------|-------|
| Demographics | 28, Male, Mumbai |
| Past Purchases | Choco Almond Daily Bar (1 box, 45 days ago) |
| Abandoned Cart | Plant Protein Powder — Chocolate (5 days ago) |
| Session Context | Mobile, 4:30 PM, reading nutrition blog |
| Objection Theme | Skepticism about protein bars being "glorified candy bars" |
| Recommendation Logic | Time-of-day (approaching 5 PM crash) + chocolate flavor affinity → Date & Almond Bar + Chocolate Plant Protein recovery |

### Profile 2: Priya Sharma — Fitness Enthusiast
| Attribute | Value |
|-----------|-------|
| Demographics | 24, Female, Bangalore |
| Past Purchases | 20g Active Bar — Peanut Butter (2 boxes), Protein Chips — Peri Peri |
| Abandoned Cart | Millet Wafer Bar — Jowar (6-pack, 2 days ago) |
| Session Context | Desktop, 7:15 AM, searched "low sugar protein bars" |
| Objection Theme | Skepticism about millet bars — taste vs. health gimmick |
| Recommendation Logic | Pre-workout timing + low-sugar search intent + millet bar recovery |

### Profile 3: Rohit Kapoor — Mindful Snacker
| Attribute | Value |
|-----------|-------|
| Demographics | 35, Male, Delhi |
| Past Purchases | Date & Almond Daily Bar (1 box, 60 days ago) |
| Abandoned Cart | Protein Cookies — Assorted Pack (8 days ago) |
| Session Context | Mobile, 1:00 PM, viewing RiteBite vs The Whole Truth comparison |
| Objection Theme | Direct competitor comparison — why RiteBite over The Whole Truth |
| Recommendation Logic | Clean-label sensitivity + natural sweetener preference + lapsed customer re-engagement |

### Profile 4: Sneha Iyer — New-to-Protein
| Attribute | Value |
|-----------|-------|
| Demographics | 22, Female, Hyderabad |
| Past Purchases | None (first-time visitor) |
| Abandoned Cart | Max Protein Daily — Choco Classic Trial Pack (1 day ago) |
| Session Context | Mobile, 6:00 PM, landed from Instagram ad |
| Objection Theme | "Do I even need protein bars if I don't go to the gym?" |
| Recommendation Logic | First-time buyer nurturing + budget sensitivity + educational content on protein deficiency |

## 4. System Prompt Engineering

The AI agent operates under a carefully constructed system prompt that implements:

### Brand Voice Calibration
The prompt explicitly defines the tone as "energetic, motivational, authentic, and culturally relevant to young urban Indians" — mirroring the "Protein Salute" campaign ethos. This prevents the LLM from defaulting to generic, clinical language that would feel disconnected from RiteBite's brand identity.

### RAG Grounding Constraints
The prompt includes a curated set of verified product facts the agent is allowed to reference:
- Specific protein content per SKU (10g, 20g, 30g variants)
- Ingredient claims (100% vegetarian, no artificial sweeteners in Active range)
- Sustained energy duration claims (2 hours for Daily bars, 4 hours for Active bars)
- Grain composition of Protein Chips (7-grain blend)
- Millet Wafer Bar specifications (jowar-based, zero maida/palm oil/added sugar)

### Structured Output Schema

```json
{
  "greeting": "Personalized opening acknowledging the customer's context",
  "objection_response": "Factual response grounded in RAG-retrieved data",
  "recommendation": {
    "product": "Specific SKU name",
    "reason": "Contextual justification tied to profile data",
    "nutrition_highlight": "Key nutritional fact from knowledge base"
  },
  "cart_recovery": "Natural segue to the abandoned cart item",
  "incentive": "Personalized discount or bundle offer",
  "cta": "Action-oriented closing in brand voice",
  "rag_sources_used": ["Knowledge base sources the system retrieved"]
}
```

## 5. Business Metrics Addressed

| Metric | Impact | Mechanism |
|--------|--------|-----------|
| **Cart Recovery Rate** | Targeted improvement over generic email follow-ups | Contextual, real-time conversational recovery vs. delayed batch emails |
| **Customer Lifetime Value (LTV)** | Increased through intelligent cross-selling | Recommendation engine surfaces complementary SKUs based on flavor/category affinity |
| **Add-to-Cart Conversion** | 20–40% among clicked recommended products (industry benchmark) | Personalized product cards with nutritional highlights reduce decision friction |
| **Support Cost Reduction** | 63–71% of standard queries auto-resolved | RAG-powered objection handling eliminates the need for human nutritionist escalation on common questions |
| **Consumer Trust** | Measurable through session duration and return visit rate | Factually grounded responses prevent brand-damaging misinformation |

## 6. Demonstration Flow

For the presentation, the recommended demo sequence is:

1. **Show the architecture flow** at the top (Customer Profile → RAG Retrieval → LLM + Rec Engine → Personalized Response)
2. **Select Profile 1 (Arjun Mehta)** — the Busy Professional archetype matches the simulated flow already detailed in the GTM document
3. **Point out the CDP data panel** that populates automatically — session time, device, last purchase, abandoned cart age
4. **Show the pre-loaded customer message** expressing skepticism about artificial ingredients
5. **Run the agent** and walk through the response:
   - Greeting that references the customer by context (not just name)
   - Objection response citing specific product facts (zero artificial sweeteners, Date & Almond natural sweetener)
   - Product recommendation card with nutritional highlight
   - Seamless abandoned cart recovery woven into the conversation
   - Personalized incentive offer
   - Brand-voice CTA
6. **Scroll to the RAG Sources panel** — emphasize that every claim is traceable to a verified corporate knowledge source, demonstrating zero hallucination risk
7. **Optionally switch to Profile 3 (Rohit Kapoor)** — the Mindful Snacker who is comparing RiteBite to The Whole Truth. This demonstrates how the same system handles the brand's most sensitive competitive objection

## 7. Ethical Safeguards Demonstrated

This prototype directly addresses three of the five ethical risks identified in the GTM document:

### Hallucination Mitigation
The RAG Sources panel at the bottom of every response transparently shows which internal knowledge base documents were retrieved. In production, any query with a confidence score below 85% would trigger automatic escalation to a human nutritionist.

### Brand Voice Consistency
The system prompt includes explicit brand tone guidelines, ensuring every response maintains the energetic, culturally relevant voice established by campaigns like "Protein Salute" and "Protein Aayega Tabhi India Khayega." The prototype demonstrates this through the conversational warmth and motivational cadence of the AI output.

### Data Privacy Awareness
The CDP data panel shows exactly what customer data is being used to personalize the response. In production, all PII would be tokenized before reaching the LLM, and the system would operate on anonymized behavioral signals rather than raw personal data.

## 8. Limitations & Future Enhancements

### Current Limitations
- Customer profiles are simulated rather than pulled from a live CDP
- RAG retrieval is simulated through prompt engineering rather than actual vector database queries
- Single-turn interaction — production system would maintain multi-turn conversation history
- No live recommendation algorithm — collaborative filtering is simulated through LLM reasoning

### Production Enhancements
- Integration with Shopify CDP for real-time customer profile hydration
- Pinecone/Weaviate vector database storing 500+ approved product documents, FSSAI certifications, and clinical studies
- Multi-turn conversation memory with session state management
- Real-time A/B testing of incentive offers using reinforcement learning (connecting to Task 6: Dynamic Cohort Pricing)
- Automated handoff to human agents when confidence drops below threshold
- WhatsApp and SMS delivery channels via Klaviyo integration

## 9. Connection to GTM Strategy

This prototype serves as the downstream execution layer in the proposed AI ecosystem. While Prototype A (Competitive Intelligence Scout) feeds upstream market intelligence into the system, Prototype B translates that intelligence into personalized consumer interactions.

The prototype directly implements two of the six tasks from the AI Opportunity Map:

- **Task 1 (Hyper-Personalized Recommendation Engine):** The product recommendation card demonstrates how collaborative filtering logic surfaces the exact SKU a customer is most likely to purchase, based on flavor affinity, purchase timing, and contextual signals.

- **Task 2 (Agentic RAG for Education & Objection Handling):** The objection response demonstrates how RAG-grounded generation provides factually accurate, brand-aligned answers to the skepticism that is the primary barrier for the Mindful Snacker and New-to-Protein segments.

Together, the two prototypes show the complete intelligence loop: **Market Intelligence (A) → Consumer Personalization (B)**.

---

*Prototype built with React + Anthropic Claude API. Designed for the AI Tooling for Product Marketing group project, ISB.*
