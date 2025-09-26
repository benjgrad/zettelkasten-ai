# Product Requirements Document (PRD)

## Project Title: **World Ingestion & Systems Analysis Platform**

## Author: Ben Grady

## Date: 2025-09-26

---

## 1. Purpose

The purpose of this project is to build a system that ingests information about the world through news articles, RSS feeds, and manual user-submitted links. It should structure, analyze, and contextualize this information using Donella Meadows' systems thinking. The platform should allow for both high-level trend analysis (social, political, economic, mental health, etc.) and personal engagement via a **MermaidJS-capable chatbot** and web-based UI.

**MVP Focus**: A conversational interface that can output, visualize, and troubleshoot MermaidJS diagrams, making systems thinking accessible through publicly available APIs and interfaces.

---

## 2. Goals

- **Ingest information seamlessly** from multiple sources (RSS feeds, direct links, manual entry).
- **Store and structure knowledge** in a way that supports both search and systems analysis.
- **Enable subject-related exploration** rather than shallow semantic similarity.
- **Provide interfaces** for both conversational querying (chatbot) and structured visual exploration (web UI).
- **Support long-term knowledge growth** by allowing insights to compound over time.
- **Generate meaningful MermaidJS diagrams** that visualize systems thinking concepts and relationships.

---

## 3. Key Features

### 3.1 Data Ingestion (Detailed Implementation Strategy)

#### **Core Ingestion Pipeline for MermaidJS Generation**

**Phase 1: MVP Data Sources**

- **RSS Feed Integration**:

  - Target: 10-15 high-quality feeds across domains (news, economics, technology, climate)
  - Implementation: `feedparser` (Python) or `rss-parser` (Node.js)
  - Frequency: Every 2-4 hours to balance freshness vs. API limits
  - Example sources: Reuters, BBC, MIT Technology Review, Climate Central

- **Manual Link Submission**:
  - Simple web form with URL input and optional tags
  - Browser bookmarklet for one-click capture: `javascript:(function(){window.open('your-domain.com/ingest?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title),'_blank');})()`
  - Mobile-friendly PWA interface for sharing from mobile browsers

**Phase 2: Enhanced Ingestion**

- **API Integrations**:
  - Reddit API for trending discussions in relevant subreddits
  - Twitter API v2 for real-time event detection
  - News API for broader source coverage
  - Academic sources: arXiv, PubMed for research papers

#### **Content Processing Pipeline**

**1. Article Extraction & Cleaning**

```
Raw URL → Content Extraction → Text Cleaning → Structure Analysis → Storage
```

- **Tools**:
  - `newspaper3k` or `Trafilatura` for article extraction
  - `spaCy` or `NLTK` for text processing
  - `BeautifulSoup` for HTML parsing fallback

**2. Systems Thinking Metadata Extraction**

- **Entity Recognition**: People, organizations, locations, concepts
- **Relationship Mapping**: Causal language detection ("leads to", "influences", "results in")
- **Temporal Markers**: Timeline extraction for cause-effect chains
- **Domain Classification**: Politics, economics, environment, technology, social

**3. MermaidJS-Specific Processing**

- **Graph Structure Detection**:

  - Hierarchical relationships → Flowcharts/org charts
  - Causal chains → Sequence diagrams
  - System feedback loops → Graph diagrams
  - Process flows → Flowcharts
  - Data relationships → ER diagrams

- **Node/Edge Extraction**:
  - Entities become nodes
  - Relationships become edges with labels
  - Temporal sequences for timeline diagrams
  - Dependency chains for dependency graphs

#### **Storage Schema for Diagram Generation**

**Document Structure**:

```json
{
  "id": "uuid",
  "source": "rss|manual|api",
  "url": "original_url",
  "title": "article_title",
  "content": "cleaned_text",
  "extracted_entities": [
    {"name": "Entity", "type": "PERSON|ORG|CONCEPT", "importance": 0.8}
  ],
  "relationships": [
    {"from": "Entity1", "to": "Entity2", "type": "CAUSES|INFLUENCES|CONTAINS", "confidence": 0.7}
  ],
  "mermaid_candidates": {
    "flowchart": {"nodes": [...], "edges": [...]},
    "timeline": {"events": [...], "sequence": [...]},
    "graph": {"entities": [...], "connections": [...]}
  },
  "systems_thinking": {
    "leverage_points": ["policy_change", "paradigm_shift"],
    "feedback_loops": [{"type": "reinforcing|balancing", "elements": [...]}],
    "domain": "economics|politics|environment|social"
  },
  "ingestion_date": "iso_timestamp",
  "tags": ["climate", "policy", "economics"]
}
```

### 3.2 Storage & Structuring for MermaidJS Generation

#### **MVP Storage Architecture**

**Primary Storage: Vector Database + Document Store**

- **Recommended**: `Weaviate` or `Pinecone` for vector similarity
- **Document Store**: `PostgreSQL` with JSONB for structured metadata
- **Benefits**:
  - Fast semantic search for related concepts
  - Structured queries for diagram generation
  - Cost-effective for MVP scale (<10k documents)

**Alternative: Elasticsearch + Embeddings**

- **Implementation**: Elasticsearch 8.0+ with built-in vector search
- **Custom analyzers**: Domain-specific tokenization (economics, politics, etc.)
- **Benefit**: Mature ecosystem, extensive documentation

#### **Graph Structure for Systems Thinking**

**Entity-Relationship Model**:

```
Entities: [Person, Organization, Concept, Event, Policy, Technology]
Relationships: [CAUSES, INFLUENCES, CONTAINS, PRECEDES, OPPOSES, SUPPORTS]
Attributes: [confidence, temporal_context, domain, source_count]
```

**MermaidJS Template Mapping**:

1. **Causal Chains** → Flowchart LR (Left to Right)
2. **System Hierarchies** → Flowchart TD (Top Down)
3. **Timeline Events** → Timeline diagram
4. **Stakeholder Networks** → Graph diagrams
5. **Process Flows** → Sequence diagrams

#### **Indexing Strategy for Chatbot Queries**

**Multi-dimensional Indexing**:

- **Temporal**: Time-based queries ("what happened after the policy change?")
- **Causal**: Cause-effect relationships ("what led to the economic downturn?")
- **Domain**: Subject-matter filtering ("show me climate-related feedback loops")
- **Entity**: People/organization-centric views ("track decisions by this leader")
- **Geographic**: Location-based analysis ("compare policies between countries")

**Search Optimization for Diagram Generation**:

- **Graph traversal queries**: Find connected entities within N degrees
- **Pattern matching**: Identify common causal patterns across domains
- **Clustering**: Group similar events/concepts for comparative diagrams

### 3.3 Analysis

- **Systems Thinking Integration**:

  - Highlight reinforcing/balancing feedback loops.
  - Identify leverage points in ongoing topics.
  - Support categorization under Meadows' 12 leverage points.

- **Trend Aggregation**:

  - Time-series tracking of topics.
  - Compare across domains (e.g., Canadian politics vs. global geopolitics).

### 3.4 Interfaces

#### **MVP: MermaidJS Chatbot Interface**

**Core Chatbot Capabilities**:

- **Diagram Generation Commands**:

  - "Show me the causal chain for [topic]"
  - "Create a timeline of [event sequence]"
  - "Map the stakeholders involved in [issue]"
  - "Generate a systems map for [domain]"

- **Diagram Troubleshooting**:
  - Syntax validation for generated MermaidJS
  - Interactive refinement: "make the diagram simpler", "add more detail"
  - Export options: PNG, SVG, shareable links
  - Diagram versioning and iteration history

**Technical Implementation**:

- **LLM Integration**: OpenAI GPT-4 or Claude with custom prompt engineering
- **MermaidJS Generation**: Structured output format with syntax validation
- **Rendering**: `mermaid.js` library with live preview
- **Interface**: Gradio, Streamlit, or custom React/Vue.js chat UI

**Sample Conversation Flow**:

```
User: "Show me what's driving the housing crisis in Canada"
Bot: [Generates flowchart showing: Immigration → Population Growth → Housing Demand ↑ & Construction Regulations → Housing Supply ↓ → Price Increase]
User: "Add government policies to this diagram"
Bot: [Updates diagram with policy nodes and their impacts]
User: "Make it simpler for a presentation"
Bot: [Generates condensed version with key factors only]
```

#### **Phase 2: Web UI Dashboard**

**Topic Tracking System**:

- **Saved Analyses**: Bookmark and organize generated diagrams
- **Topic Evolution**: Track how topics change over time
- **Collaborative Features**: Share diagrams, add annotations
- **Export Integration**: PDF reports, presentation formats

**Advanced Visualization Options** (Phase 3):

- **Interactive Network Graphs**: D3.js, Cytoscape.js, or Vis.js
- **Temporal Visualizations**: Timeline.js, custom React components
- **Geographic Mapping**: Leaflet.js for location-based analysis
- **Data Dashboards**: Observable Plot, Chart.js for metrics

**Note on Advanced Visualizations**:

- **Pros**: Much more powerful and interactive than MermaidJS
- **Cons**: Significantly harder to generate with AI, limited troubleshooting capability
- **Recommendation**: Start with MermaidJS for MVP, evaluate advanced options based on user feedback

---

## 4. Proposals & Alternatives

### 4.1 Data Ingestion Strategy (Refined)

#### **MVP Approach: Public APIs + Curated Sources**

**Option A: RSS + News APIs + Manual Links (Recommended MVP)**

- **Implementation**:
  - 10-15 high-quality RSS feeds
  - News API integration for broader coverage
  - Simple manual submission form
  - Reddit API for trending discussions
- **Pros**:
  - Reliable, consistent data format
  - Publicly available interfaces (aligns with your requirement)
  - Minimal maintenance overhead
  - Legal compliance (terms of service compliant)
- **Cons**: Limited to public sources, potential API rate limits

**Option B: Add Web Scraping (Phase 2)**

- **Implementation**: Respectful scraping with rate limiting
- **Pros**: Access to sources without APIs
- **Cons**: Legal/ethical considerations, maintenance burden

**Option C: Academic/Research Integration (Phase 3)**

- **Sources**: arXiv, Google Scholar, government databases
- **Benefits**: Higher-quality analytical content for systems thinking

#### **Detailed Source Prioritization for Systems Thinking**

**Tier 1 (MVP) - High Signal Sources**:

- **Economics**: Federal Reserve publications, World Bank, IMF
- **Policy**: Government RSS feeds, think tank publications
- **Technology**: MIT Technology Review, IEEE Spectrum
- **Environment**: Climate Central, IPCC reports
- **Social**: Pew Research, academic sociology journals

**Tier 2 (Phase 2) - Broader Coverage**:

- **News Aggregation**: AllSides, Ground News for bias detection
- **Social Media**: Twitter trends, Reddit discussions
- **Industry**: Sector-specific trade publications

**Tier 3 (Phase 3) - Specialized Sources**:

- **Academic**: Research paper databases
- **Government**: Policy documents, regulatory filings
- **Corporate**: Annual reports, earnings calls

### 4.2 Storage

- **Option A: Elasticsearch only**

  - Pros: Mature, scalable, excellent search capabilities.
  - Cons: Harder to model relationships beyond keyword matching.

- **Option B: Graph database only**

  - Pros: Excellent for relationships, good for systems thinking.
  - Cons: Weaker search and indexing performance.

- **Option C: Hybrid (Elasticsearch + Graph)**

  - Pros: Best of both worlds—search + relationships.
  - Cons: Higher complexity, more infrastructure.

### 4.3 Knowledge Structuring

- **Option A: Purely automated (topic extraction, clustering)**

  - Pros: Scalable, minimal manual work.
  - Cons: Risk of weak or misleading connections.

- **Option B: Pure Zettelkasten manual linking**

  - Pros: Deep, meaningful connections.
  - Cons: Very labor-intensive.

- **Option C: Hybrid (auto-suggested links + manual curation)**

  - Pros: Balance of scalability and accuracy.
  - Cons: Requires UI design for curation workflow.

### 4.4 Interfaces

- **Option A: Chatbot first (MVP)**

  - Pros: Fast to implement, intuitive.
  - Cons: Weak on visual/system-level exploration.

- **Option B: Web UI first (MVP)**

  - Pros: Better for exploration and visualization.
  - Cons: Slower to implement.

- **Option C: Parallel lightweight versions of both**

  - Pros: Covers both use cases from the start.
  - Cons: Higher dev cost and complexity.

---

## 5. Evaluation Criteria

- **Scalability:** Can it handle increasing amounts of data over years?
- **Accuracy:** Are subject-related connections meaningful and useful?
- **Maintainability:** How much ongoing maintenance does ingestion/storage require?
- **User Effort:** How much human-in-the-loop work is sustainable?
- **Cost:** Infrastructure and development overhead.
- **Flexibility:** Can the system evolve as goals or scope expand?

---

## 6. Roadmap (High-Level)

**Phase 1 (MVP - 3-4 months):**

- **Data Pipeline**: RSS feeds + News API + manual links (target: 100-500 articles/week)
- **Storage**: Vector database (Weaviate/Pinecone) + PostgreSQL for metadata
- **Chatbot**: MermaidJS-capable conversation interface with basic diagram types
- **Core Diagrams**: Flowcharts, timelines, simple system maps
- **Success Metric**: Generate meaningful diagrams for 80% of systems thinking queries

**Phase 2 (6-8 months):**

- **Enhanced Ingestion**: Reddit API, Twitter integration, academic sources
- **Web UI**: Topic tracking dashboard, saved analyses, diagram export
- **Advanced Diagrams**: Feedback loop visualization, leverage point mapping
- **Collaboration**: Shareable diagrams, annotation system
- **Success Metric**: 10+ regular users creating 50+ diagrams/month

**Phase 3 (12+ months):**

- **Advanced Visualizations**: D3.js interactive networks, temporal analysis
- **Intelligence**: Pattern recognition across topics, predictive modeling
- **Integration**: Export to presentation tools, research platforms
- **Scaling**: Handle 10k+ articles, support team collaboration
- **Success Metric**: Platform used for professional research and decision-making

#### **MVP Technical Stack Recommendation**

**Backend**:

- **Language**: Python (rich ecosystem for NLP/ML)
- **Framework**: FastAPI or Flask for API development
- **Database**: PostgreSQL + Weaviate vector DB
- **Processing**: spaCy for NLP, sentence-transformers for embeddings

**Frontend (Chatbot)**:

- **Framework**: Gradio for rapid prototyping, or React for custom UI
- **Visualization**: mermaid.js for diagram rendering
- **Deployment**: Streamlit Community Cloud or Vercel for MVP

**Infrastructure**:

- **Hosting**: Railway, Render, or Heroku for MVP simplicity
- **Scaling**: Kubernetes on DigitalOcean for Phase 2+
- **Monitoring**: Simple logging with Sentry for error tracking

---

## 7. Risks & Mitigations

- **Risk: Data overload** → Mitigation: filtering, prioritization, curation workflows.
- **Risk: Complexity creep** → Mitigation: strict MVP scoping, phased rollout.
- **Risk: Misleading connections** → Mitigation: hybrid approach (auto + manual curation).
- **Risk: Maintenance burden** → Mitigation: modular architecture, use of mature tools.

---

## 8. Success Metrics

- % of ingested articles properly parsed and indexed.
- Average retrieval time for queries.
- Number of meaningful Zettelkasten connections created per week.
- User satisfaction with chatbot answers.
- Frequency of system usage (daily/weekly active use).

---

## 9. Technical Decisions & Implementation Questions

### **Resolved Recommendations**

**Visualization Strategy**:

- **MVP**: MermaidJS for AI-generatable, troubleshootable diagrams
- **Phase 2**: Selective integration of D3.js/Cytoscape for advanced use cases
- **Rationale**: MermaidJS provides the best balance of AI compatibility and functionality

**LLM Architecture**:

- **Approach**: RAG (Retrieval-Augmented Generation) over fine-tuning
- **Rationale**: More flexible, easier to update, cost-effective for MVP scale
- **Implementation**: Vector similarity search + prompt engineering

### **Open Questions for Implementation**

**Mobile Workflow**:

- Should we build a PWA or focus on browser bookmarklet initially?
- How to integrate with iOS/Android share sheets for seamless capture?

**Data Quality & Curation**:

- What's the optimal balance between automated processing and human curation?
- How to implement feedback loops for improving diagram quality?

**Scalability Considerations**:

- At what data volume should we transition from vector DB to graph database?
- How to implement intelligent article filtering to prevent information overload?

**User Experience**:

- Should diagram generation be real-time or batch-processed for complex queries?
- How to design progressive disclosure for diagram complexity (simple → detailed)?

**Integration Roadmap**:

- Which third-party tools should we prioritize for export (Notion, Obsidian, etc.)?
- How to design APIs for potential integration with research tools?

### **Success Criteria for MVP Validation**

**Technical Metrics**:

- Generate syntactically valid MermaidJS for 95%+ of requests
- Sub-3 second response time for diagram generation
- Successfully parse and process 90%+ of ingested articles

**User Value Metrics**:

- Users generate meaningful diagrams in 80%+ of sessions
- 70%+ of generated diagrams require minimal troubleshooting
- Users return to refine/build upon previous analyses

**Platform Health**:

- Ingest and process 100+ articles/week sustainably
- Maintain system uptime >99% for core functionality
- Support concurrent usage by 5-10 beta users

---

**End of Document**
