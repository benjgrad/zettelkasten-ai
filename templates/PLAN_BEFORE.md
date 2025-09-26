# Project Plan: World Ingestion & Systems Analysis Platform

## Overview & Milestones

### Project Vision

Build a conversational platform that ingests information from multiple sources (RSS feeds, manual links, APIs) and generates MermaidJS diagrams for systems thinking analysis. The MVP focuses on a chatbot interface that can create, visualize, and troubleshoot MermaidJS diagrams, making systems thinking accessible through publicly available APIs.

### Key Milestones

- **Milestone 1: MVP Prototype** (4-6 weeks)
  - Working chatbot interface with MermaidJS generation from ingested RSS content
  - Basic entity extraction and relationship mapping
  - SQLite + ChromaDB storage with semantic search
  - Single container deployment on Railway/Render
- **Milestone 2: Enhanced Features** (6-8 weeks)
  - Web UI dashboard with saved diagrams
  - Multiple diagram types (timeline, graph, sequence)
  - PostgreSQL + Weaviate migration
  - Export capabilities and user authentication
- **Milestone 3: Scale & Advanced Features** (8-12 weeks)
  - Real-time collaboration on diagrams
  - Advanced systems thinking analysis
  - Kubernetes deployment with microservices
  - Integration with external tools (Notion, Obsidian)

### Current Phase: Phase 1 - MVP Prototype

### Next Actionable Step

Set up FastAPI backend project structure with basic endpoint stubs and health check endpoint. Create requirements.txt with core dependencies (FastAPI, spaCy, ChromaDB, OpenAI). Verify local development environment runs successfully.

### In Progress

None - starting fresh implementation

### Immediate Todo List (Next 2-3 Steps)

1. Set up FastAPI backend project structure with health check endpoint
2. Implement basic RSS feed ingestion service for 3-5 test feeds
3. Create simple entity extraction pipeline using spaCy

### Phase Breakdown

#### Phase 1: MVP Prototype (4-6 weeks)

**Week 1-2: Core Infrastructure**

- [ ] **Step 1.1**: Set up FastAPI backend with basic endpoints and health check
  - _Acceptance Criteria_: GET /health returns 200, POST /ingest/manual endpoint exists
  - _Testing_: curl localhost:8000/health returns {"status": "ok"}
- [ ] **Step 1.2**: Implement RSS feed ingestion for 3-5 test feeds
  - _Acceptance Criteria_: Fetch 10+ articles daily from Reuters, BBC, MIT Tech Review
  - _Testing_: /ingest/rss endpoint processes feeds and stores in SQLite
- [ ] **Step 1.3**: Create basic entity extraction with spaCy
  - _Acceptance Criteria_: Extract PERSON, ORG, GPE entities with >80% accuracy on news articles
  - _Testing_: Process test article and verify entities extracted correctly
- [ ] **Step 1.4**: Set up SQLite + ChromaDB storage with basic schema
  - _Acceptance Criteria_: Store articles with metadata, embeddings generated for semantic search
  - _Testing_: Insert test article, perform similarity search, retrieve results

**Week 3-4: Diagram Generation**

- [ ] **Step 2.1**: Implement basic MermaidJS flowchart generator
  - _Acceptance Criteria_: Generate valid MermaidJS from entities/relationships
  - _Testing_: Input test entities, output renders in mermaid.live
- [ ] **Step 2.2**: Add MermaidJS syntax validation and error handling
  - _Acceptance Criteria_: Detect invalid syntax, provide specific error messages
  - _Testing_: Validate both valid and invalid MermaidJS code samples
- [ ] **Step 2.3**: Create OpenAI GPT-4 integration for diagram refinement
  - _Acceptance Criteria_: Accept user feedback like "make it simpler", update diagram
  - _Testing_: Refine test diagram through 3 iterations successfully
- [ ] **Step 2.4**: Build Gradio chatbot interface with diagram rendering
  - _Acceptance Criteria_: Chat interface displays rendered MermaidJS diagrams
  - _Testing_: Submit query, receive rendered diagram in web interface

**Week 5-6: Integration & Testing**

- [ ] **Step 3.1**: Implement end-to-end workflow from query to diagram
  - _Acceptance Criteria_: "Show housing crisis causes" generates meaningful diagram
  - _Testing_: Process 5 different domain queries successfully
- [ ] **Step 3.2**: Add basic error handling and logging throughout pipeline
  - _Acceptance Criteria_: Graceful degradation, informative error messages
  - _Testing_: Handle malformed inputs, API failures, empty results
- [ ] **Step 3.3**: Performance optimization for sub-5 second response times
  - _Acceptance Criteria_: Diagram generation completes in <5 seconds
  - _Testing_: Measure response times under normal load
- [ ] **Step 3.4**: Deploy to Railway/Render with environment configuration
  - _Acceptance Criteria_: Public URL accessible, handles 10 concurrent users
  - _Testing_: Load test with multiple simultaneous requests

#### Phase 2: Enhanced Features (6-8 weeks)

**Enhanced User Experience**

- Web UI dashboard for saving and organizing diagrams
- Multiple diagram types: timeline, graph, sequence diagrams
- User authentication and session management
- Export capabilities: PNG, SVG, PDF formats
- Improved LLM prompt engineering for better diagram quality

**Technical Infrastructure**

- Migration from SQLite to PostgreSQL + Weaviate
- Redis caching for frequently accessed data
- Comprehensive monitoring and logging
- API rate limiting and usage analytics
- Enhanced entity recognition and relationship mapping

#### Phase 3: Scale & Advanced Features (8-12 weeks)

**Advanced Capabilities**

- Real-time collaboration on diagrams with WebSocket support
- Advanced systems thinking analysis (leverage points, feedback loops)
- Integration APIs for external tools (Notion, Obsidian, etc.)
- Mobile-responsive design with PWA capabilities
- Advanced visualization options beyond MermaidJS

**Infrastructure Scaling**

- Kubernetes deployment with microservices architecture
- Horizontal scaling with load balancing
- Advanced caching strategies and CDN integration
- Comprehensive security hardening
- Automated backup and disaster recovery

### Technical Implementation

#### Architecture Decisions

- **Storage Strategy**: Start with SQLite + ChromaDB for simplicity, migrate to PostgreSQL + Weaviate in Phase 2
- **API Design**: RESTful endpoints with WebSocket for real-time chat interface
- **LLM Integration**: OpenAI GPT-4 API with structured output for MermaidJS generation
- **Deployment**: Single container for MVP, migrate to microservices in Phase 3

#### Technology Stack

**MVP Stack:**

- Backend: Python 3.11+ with FastAPI framework
- Database: SQLite for structured data, ChromaDB for vector search
- NLP: spaCy for entity extraction, sentence-transformers for embeddings
- LLM: OpenAI GPT-4 API for diagram generation and refinement
- Frontend: Gradio for rapid chatbot interface prototyping
- Deployment: Railway/Render for simplicity

**Production Stack (Phase 2+):**

- Database: PostgreSQL + Weaviate vector database
- Cache: Redis for session management and frequent queries
- Frontend: React + TypeScript with mermaid.js for visualization
- Infrastructure: Kubernetes on DigitalOcean with CI/CD via GitHub Actions

#### Development Approach

- **Prototype-First**: Focus on working software over comprehensive documentation
- **Modular Components**: Independent services for ingestion, processing, diagram generation
- **Test-Driven**: Each step includes specific acceptance criteria and testing instructions
- **Iterative Feedback**: Early user testing to validate diagram quality and usefulness

### Success Criteria

#### Phase 1 Success Metrics

- Generate syntactically valid MermaidJS for 95%+ of requests
- Sub-5 second response time for diagram generation queries
- Successfully parse and process 90%+ of ingested RSS articles
- Users generate meaningful diagrams in 80%+ of chat sessions
- System handles 5-10 concurrent users without degradation

#### Phase 2 Success Metrics

- 10+ regular users creating 50+ diagrams per month
- Support for 4+ diagram types (flowchart, timeline, graph, sequence)
- Web dashboard with saved diagrams and export functionality
- Migration to production database with improved search performance
- 99%+ uptime with comprehensive monitoring

#### Phase 3 Success Metrics

- Platform supports 100+ concurrent users
- Real-time collaboration features with conflict resolution
- Integration with 3+ external tools (Notion, Obsidian, etc.)
- Advanced systems thinking analysis capabilities
- Professional adoption for research and decision-making workflows

## Open Questions / Unknowns

### Technical Unknowns

- **Diagram Quality**: How consistently can GPT-4 generate high-quality MermaidJS from news content?
- **Vector Search Performance**: Will ChromaDB scale adequately for 1000+ articles, or need earlier migration?
- **LLM Costs**: What will OpenAI API costs be at target usage levels (need cost modeling)?
- **Entity Recognition Accuracy**: How well will spaCy perform on domain-specific content vs news articles?

### Product Unknowns

- **User Adoption**: Will users find MermaidJS diagrams useful for systems thinking vs more advanced visualizations?
- **Content Sources**: Which RSS feeds provide the best signal-to-noise ratio for systems analysis?
- **Diagram Complexity**: What's the optimal balance between detailed vs simplified diagrams?
- **Mobile Usage**: How important is mobile-responsive design for the target user workflow?

### Implementation Unknowns

- **Deployment Complexity**: Will single container deployment scale to Phase 1 user targets?
- **Database Migration**: How complex will SQLite to PostgreSQL migration be with user data?
- **Real-time Features**: What WebSocket architecture will work best for collaborative diagram editing?
- **Export Quality**: Which export formats (PNG, SVG, PDF) will users actually use?

### Research Items

- **Benchmark OpenAI API costs** for expected usage patterns (need spike)
- **Evaluate ChromaDB performance** with 1000+ article dataset (load test needed)
- **Test MermaidJS generation quality** across different news domains (validation study)
- **Research mobile PWA requirements** for future development phases

## Next Review & Re-Prioritization Notes

### When to Review

- **After each week** of Phase 1 development to assess progress against timeline
- **After completing each milestone** to evaluate success criteria and user feedback
- **When blocked >45 minutes** due to unclear dependencies or technical issues
- **If any step exceeds 2 work sessions** to reassess scope and break down further

### Review Criteria

- **Technical Progress**: Are acceptance criteria being met objectively?
- **Timeline Adherence**: Are weekly milestones on track or need adjustment?
- **Quality Metrics**: Is diagram generation meeting 95% validity target?
- **User Feedback**: Are early testers finding the system useful and intuitive?
- **Cost Tracking**: Are OpenAI API costs within expected ranges?

### Potential Pivot Points

- **If diagram quality <80%**: Consider template-based generation vs pure LLM approach
- **If performance issues**: Migrate to production database earlier than planned
- **If user adoption low**: Focus on specific use case (research, education) vs general tool
- **If costs too high**: Evaluate local LLM options (Ollama) or reduce functionality

### Performance Indicators to Monitor

- **Diagram generation success rate** (target: 95%+ valid MermaidJS)
- **Response time distribution** (target: 95th percentile <5 seconds)
- **User engagement metrics** (session length, diagram iterations per query)
- **System reliability** (uptime, error rates, resource utilization)
- **Cost per request** (OpenAI API usage, infrastructure costs)

---

**Last Updated**: 2025-09-26
**Next Review**: After Step 1.1 completion (FastAPI setup)
