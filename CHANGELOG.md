# Changelog

All notable changes to ResearchHub AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-14

### Added
- Publication-quality research paper generation with IEEE/ACM/Springer formats
- AI-powered content generation for 9 paper sections
  - Abstract (250-280 words with quantifiable results)
  - Introduction (650-750 words with 10-15 citations)
  - Problem Statement (experimental investigation)
  - Literature Review (750-850 words with 15-20 citations)
  - Methodology (800-900 words with reproducible detail)
  - Results (750-850 words with specific metrics)
  - Conclusion (400-450 words)
  - Future Work (300-350 words)
  - References (15-20 realistic citations)
- AI Improve feature with 6-step enhancement process
- AI Review feature for quality assessment
- Export to IEEE/ACM/Springer conference formats
- HTML export with print-to-PDF functionality
- Dual AI provider support (Ollama and OpenAI)
- User authentication and authorization
- Dashboard with paper management
- Real-time collaboration requests
- Project management system
- Researcher matching algorithm
- Messaging system for collaborators

### Features
- **Conference Templates**
  - IEEE two-column format (Times New Roman 10pt)
  - ACM single-column format
  - Springer LNCS format

- **AI Generation**
  - Context-aware prompts for each section
  - Technical depth with formal academic style
  - Integrated citations and references
  - Token limits: 800-1500 per section

- **Export Options**
  - HTML rendering with conference styling
  - Print-to-PDF button overlay
  - Optional WeasyPrint PDF generation
  - Format selection (IEEE/ACM/Springer)

### Technical
- Flask 3.0.0 web framework
- SQLAlchemy 2.0.23 ORM with SQLite
- OpenAI 1.6.1 API integration
- Ollama local AI support (mistral model)
- WeasyPrint 60.1 (optional PDF generation)
- Flask-Login authentication
- Flask-SocketIO for real-time features

### Documentation
- Comprehensive README with quick start guide
- QUICKSTART.md for rapid setup
- API documentation
- Contribution guidelines
- Installation guides

## [Unreleased]

### Planned
- Multi-domain support beyond AI
- Advanced citation management
- Collaborative editing
- Version control for papers
- Plagiarism detection
- LaTeX export
- BibTeX integration
- Docker compose for production deployment
- CI/CD pipeline
