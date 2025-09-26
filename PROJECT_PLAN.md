# Project Plan: World Ingestion & Systems Analysis Platform

## MermaidJS-Capable Systems Thinking Platform

**Author**: Technical Program Manager  
**Date**: 2025-09-26  
**Version**: 1.0  
**Source Documents**: PRD.md, SDD.md

---

## Document References

This project plan is derived from and implements the requirements specified in:

- **PRD.md** (Product Requirements Document): Defines the product vision, core features, user needs, and success metrics
- **SDD.md** (Software Design Document): Provides technical architecture, implementation strategy, and detailed component specifications

### Key Requirements from PRD.md

- Build MVP conversational interface for MermaidJS diagram generation (Section 2: Goals)
- Support systems thinking analysis using Donella Meadows' framework (Section 1: Purpose)
- Ingest from RSS feeds, manual links, and APIs (Section 3.1: Data Ingestion)
- Enable both chatbot and web UI interfaces (Section 3.4: Interfaces)
- 7-week MVP timeline with prototype-first approach (Section 6: Roadmap)

### Key Architecture from SDD.md

- FastAPI backend with modular microservices design (Section 2.2: Service Architecture)
- Hybrid storage: Vector database + PostgreSQL (Section 4.1: Data Architecture)
- spaCy for NLP processing and entity extraction (Section 3.2: Processing Service)
- MermaidJS validation and generation system (Section 3.3: Diagram Service)
- Gradio interface for MVP chatbot (Section 7.2: Prototype Components)

---

## 1. Overview / Milestones

### Project Vision

Build an MVP conversational interface that generates, visualizes, and troubleshoots MermaidJS diagrams for systems thinking analysis, fed by automated content ingestion from public sources.

### Key Milestones

| Milestone                        | Target Date | Success Criteria                                                      |
| -------------------------------- | ----------- | --------------------------------------------------------------------- |
| **M1: Basic Ingestion Pipeline** | Week 2      | Successfully ingest and store 50+ articles from 5 RSS feeds           |
| **M2: Core NLP Processing**      | Week 3      | Extract entities and relationships from 80% of articles               |
| **M3: MermaidJS Generation**     | Week 4      | Generate valid MermaidJS diagrams for basic causal chains             |
| **M4: Chatbot Interface**        | Week 5      | Deploy working chatbot that responds to diagram requests              |
| **M5: End-to-End Workflow**      | Week 6      | Complete user journey: article ingestion → query → diagram generation |
| **M6: MVP Deployment**           | Week 7      | Deployed system accessible to 5 beta users                            |

### Success Metrics

- **Technical**: 95% valid MermaidJS generation, <3s response time
- **User Value**: 80% of queries produce meaningful diagrams
- **Platform Health**: Process 100+ articles/week, 99% uptime

---

## 2. Detailed Plan

### Phase 1: Foundation & Core Infrastructure (Weeks 1-3)

| Step | Task Description                   | Acceptance Criteria                                                                                      | Testing Instructions                                             | Dependencies | Status |
| ---- | ---------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------ | ------ |
| 1.1  | **Set up development environment** | - Python 3.11+ virtual environment<br>- FastAPI project structure<br>- Git repository with basic CI      | Run `python --version`, `pip list`, FastAPI hello world responds | None         | ⏳     |
| 1.2  | **Implement basic data models**    | - Article, Entity, Relationship models<br>- SQLite database schema<br>- Basic CRUD operations            | Unit tests pass for all model operations                         | 1.1          | ⏳     |
| 1.3  | **Create RSS feed ingestion**      | - Process 5 RSS feeds<br>- Extract title, content, URL, date<br>- Store in database without duplicates   | Manually verify 10 articles stored correctly from each feed      | 1.2          | ⏳     |
| 1.4  | **Basic content extraction**       | - Extract clean text from URLs<br>- Handle common news site formats<br>- Store processed content         | Test with 20 diverse news URLs, 90% success rate                 | 1.3          | ⏳     |
| 1.5  | **Entity extraction with spaCy**   | - Extract PERSON, ORG, GPE entities<br>- Basic confidence scoring<br>- Store entities linked to articles | Process test article, verify entities match manual review        | 1.4          | ⏳     |

### Phase 2: NLP Processing & Relationship Mapping (Weeks 3-4)

| Step | Task Description                  | Acceptance Criteria                                                                                                 | Testing Instructions                                  | Dependencies | Status |
| ---- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------ | ------ |
| 2.1  | **Causal relationship detection** | - Pattern matching for causal language<br>- Extract "A causes B" relationships<br>- Basic confidence scoring        | Test with articles containing clear causal statements | 1.5          | ⏳     |
| 2.2  | **Systems thinking metadata**     | - Classify content by domain<br>- Identify feedback loops<br>- Mark leverage points candidates                      | Process 50 test articles, manual validation of 10     | 2.1          | ⏳     |
| 2.3  | **Vector embeddings for search**  | - Generate embeddings for articles<br>- Implement semantic search<br>- ChromaDB integration                         | Search for "housing crisis" returns relevant articles | 2.2          | ⏳     |
| 2.4  | **Entity relationship storage**   | - Graph-like storage of entity connections<br>- Temporal relationship tracking<br>- Confidence-weighted connections | Query relationships for specific entities             | 2.3          | ⏳     |

### Phase 3: MermaidJS Diagram Generation (Weeks 4-5)

| Step | Task Description                | Acceptance Criteria                                                                                       | Testing Instructions                                        | Dependencies | Status |
| ---- | ------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------ | ------ |
| 3.1  | **Basic flowchart generator**   | - Generate simple A→B→C flowcharts<br>- Valid MermaidJS syntax<br>- Handle 5-10 node diagrams             | Generate diagram from test data, validate in Mermaid editor | 2.4          | ⏳     |
| 3.2  | **MermaidJS syntax validation** | - Check for syntax errors<br>- Basic auto-correction<br>- Error reporting with suggestions                | Test with intentionally broken syntax                       | 3.1          | ⏳     |
| 3.3  | **Multiple diagram types**      | - Flowchart, timeline, graph support<br>- Auto-detect best type for query<br>- Template-based generation  | Test each diagram type with appropriate data                | 3.2          | ⏳     |
| 3.4  | **Query-to-diagram pipeline**   | - Parse user query intent<br>- Retrieve relevant entities/relationships<br>- Generate appropriate diagram | Test with 10 diverse query types                            | 3.3          | ⏳     |
| 3.5  | **Diagram refinement system**   | - Accept refinement requests<br>- "Make simpler", "Add detail" commands<br>- Maintain diagram context     | Test iterative refinement on sample diagrams                | 3.4          | ⏳     |

### Phase 4: Chatbot Interface & Integration (Weeks 5-6)

| Step | Task Description                     | Acceptance Criteria                                                                                                  | Testing Instructions                             | Dependencies | Status |
| ---- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------ | ------ |
| 4.1  | **FastAPI endpoints for chat**       | - WebSocket connection for real-time chat<br>- REST endpoints for diagram operations<br>- Error handling and logging | Test API endpoints with Postman/curl             | 3.5          | ⏳     |
| 4.2  | **LLM integration (OpenAI)**         | - GPT-4 API integration<br>- Prompt engineering for diagram generation<br>- Context management for conversations     | Test various query types, verify diagram quality | 4.1          | ⏳     |
| 4.3  | **Gradio chat interface**            | - Simple chat UI with message history<br>- MermaidJS diagram rendering<br>- Export functionality                     | Manual testing of complete user workflow         | 4.2          | ⏳     |
| 4.4  | **Diagram troubleshooting features** | - Syntax error detection and fixes<br>- Interactive refinement workflow<br>- Version history for diagrams            | Test error scenarios and refinement requests     | 4.3          | ⏳     |

### Phase 5: End-to-End Testing & Deployment (Weeks 6-7)

| Step | Task Description             | Acceptance Criteria                                                                                         | Testing Instructions                            | Dependencies | Status |
| ---- | ---------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------ | ------ |
| 5.1  | **Integration testing**      | - Complete workflow: ingestion→search→generation<br>- Performance benchmarks<br>- Error handling edge cases | Automated test suite covering main scenarios    | 4.4          | ⏳     |
| 5.2  | **Data pipeline automation** | - Scheduled RSS feed processing<br>- Automatic content processing<br>- Health monitoring and alerts         | Verify system runs unattended for 48 hours      | 5.1          | ⏳     |
| 5.3  | **MVP deployment setup**     | - Docker containerization<br>- Railway/Render deployment<br>- Environment configuration                     | Deploy to staging, verify accessibility         | 5.2          | ⏳     |
| 5.4  | **Beta user testing**        | - 5 beta users testing core workflows<br>- Feedback collection system<br>- Performance monitoring           | Beta users complete 10 diagram generations each | 5.3          | ⏳     |
| 5.5  | **Production deployment**    | - Stable production environment<br>- Monitoring and logging<br>- User documentation                         | System stable under concurrent usage            | 5.4          | ⏳     |

---

## 3. Open Questions / Unknowns

### Technical Unknowns

1. **MermaidJS Generation Quality**:

   - Will LLM-generated diagrams be consistently valid and useful?
   - What's the optimal prompt engineering approach?
   - How to handle complex system relationships in simple diagrams?

2. **Performance at Scale**:

   - Can ChromaDB handle semantic search at target scale (1000+ articles)?
   - What's the latency impact of real-time diagram generation?
   - Memory requirements for keeping embeddings in memory?

3. **Entity Relationship Accuracy**:
   - How accurate will spaCy entity extraction be across diverse content?
   - Can pattern matching reliably identify causal relationships?
   - What confidence thresholds work best for relationship filtering?

### Product Unknowns

4. **User Interaction Patterns**:

   - What types of queries will users actually ask?
   - How often will users need diagram refinement?
   - What level of diagram complexity is optimal?

5. **Content Quality & Relevance**:
   - Which RSS feeds provide the best signal-to-noise ratio?
   - How to prevent information overload while maintaining comprehensiveness?
   - What domains should be prioritized for MVP?

### Infrastructure Unknowns

6. **Deployment & Scaling**:
   - Will single-container deployment handle initial user load?
   - What are the actual OpenAI API costs for diagram generation?
   - How to handle API rate limits during peak usage?

### Data Quality Unknowns

7. **Content Processing**:
   - Success rate of content extraction across different news sites?
   - How to handle paywalled or JavaScript-heavy content?
   - Quality of automatic domain classification?

---

## 4. Next Review / Re-prioritization Notes

### Weekly Review Process

- **Every Monday**: Review previous week's progress, update status, identify blockers
- **Dependencies**: Re-evaluate if any dependencies are blocking progress
- **Scope Adjustments**: Consider scope reduction if behind schedule
- **User Feedback Integration**: Incorporate learnings from any early testing

### Key Decision Points

1. **Week 3 Review**: Evaluate NLP processing quality

   - If entity extraction <70% accurate → Consider simpler approach or different models
   - If relationship detection fails → Fall back to keyword-based connections

2. **Week 4 Review**: Assess MermaidJS generation feasibility

   - If syntax validation <90% → Implement more robust error correction
   - If diagrams aren't meaningful → Revise prompt engineering approach

3. **Week 5 Review**: Validate complete user workflow
   - If end-to-end latency >5s → Optimize processing pipeline
   - If user experience poor → Consider interface redesign

### Risk Mitigation Checkpoints

- **Technical Risk**: LLM costs exceeding budget → Implement caching, consider local models
- **Product Risk**: Low user engagement → Gather feedback, adjust query types supported
- **Operational Risk**: Deployment complexity → Simplify to basic hosting if needed

### Success Gate Criteria

Each phase must meet minimum criteria before proceeding:

- **Phase 1**: 50+ articles successfully processed and stored
- **Phase 2**: Entity extraction working on 80% of content
- **Phase 3**: Valid MermaidJS generation for basic queries
- **Phase 4**: Complete chatbot workflow functional
- **Phase 5**: System deployable and stable

### Iteration Strategy

- **Daily standups**: Progress check and blocker identification
- **Bi-weekly demos**: Working software demonstration to stakeholders
- **User feedback loops**: Early and frequent validation with target users
- **Technical debt tracking**: Document shortcuts taken for later improvement

---

## 5. Requirements Traceability

### PRD Requirements → Plan Implementation

| PRD Requirement                        | PRD Section               | Implemented in Plan Steps                |
| -------------------------------------- | ------------------------- | ---------------------------------------- |
| **Data Ingestion from RSS feeds**      | 3.1 Data Ingestion        | Steps 1.3, 2.3, 5.2                      |
| **MermaidJS diagram generation**       | 3.4 Interfaces (MVP)      | Steps 3.1-3.5, 4.2                       |
| **Chatbot interface**                  | 3.4 Interfaces            | Steps 4.1-4.4                            |
| **Systems thinking analysis**          | 1 Purpose, 3.3 Analysis   | Steps 2.2, 2.4                           |
| **Entity and relationship extraction** | 3.2 Storage & Structuring | Steps 1.5, 2.1, 2.4                      |
| **7-week MVP timeline**                | 6 Roadmap (Phase 1)       | Overall plan structure                   |
| **Prototype-first approach**           | 6 Roadmap                 | All phases prioritize working prototypes |

### SDD Architecture → Plan Implementation

| SDD Component                   | SDD Section                    | Implemented in Plan Steps |
| ------------------------------- | ------------------------------ | ------------------------- |
| **FastAPI backend**             | 2.2 Service Architecture       | Steps 1.1, 4.1            |
| **SQLite + ChromaDB storage**   | 7.1 MVP Prototype Architecture | Steps 1.2, 2.3            |
| **spaCy NLP processing**        | 3.2 Processing Service         | Steps 1.5, 2.1            |
| **MermaidJS validation system** | 3.3 Diagram Service            | Steps 3.1, 3.2            |
| **Gradio chat interface**       | 7.2 Prototype Components       | Step 4.3                  |
| **Docker deployment**           | 7.3 Prototype Deployment       | Step 5.3                  |
| **RSS ingestion pipeline**      | 7.2 Prototype Components       | Steps 1.3, 5.2            |

### Success Metrics Alignment

| Metric Source        | Requirement                       | Plan Validation                  |
| -------------------- | --------------------------------- | -------------------------------- |
| **PRD Section 8**    | 95% article parsing success       | Step 5.1 integration testing     |
| **PRD Section 8**    | User satisfaction with chatbot    | Step 5.4 beta user testing       |
| **SDD Section 11.1** | 80% meaningful diagram generation | Milestone M3 success criteria    |
| **SDD Section 11.1** | Sub-5s response time              | Phase 3-4 performance benchmarks |
| **SDD Section 11.1** | 99% uptime                        | Step 5.5 production deployment   |

---

## Appendix: Implementation Priorities

### Must-Have for MVP

1. Basic RSS ingestion (5 feeds minimum)
2. Simple entity extraction (person, organization, location)
3. Causal relationship detection (pattern-based)
4. Flowchart generation (single diagram type)
5. Chat interface with diagram display
6. Export functionality (PNG/SVG)

### Nice-to-Have for MVP

1. Multiple diagram types (timeline, graph)
2. Advanced relationship detection
3. Domain classification
4. Diagram refinement commands
5. Manual link submission

### Post-MVP Features

1. Web dashboard
2. Advanced visualizations
3. Collaboration features
4. API integrations beyond RSS
5. Mobile interface

---

**End of Plan - Ready for Implementation**
