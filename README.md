# 🎓 ResearchHub AI

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-black.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

**AI-Powered Platform for Publication-Quality Research Paper Generation**

Generate complete, conference-ready research papers in IEEE, ACM, and Springer formats with advanced AI assistance.

[✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 📊 Overview

**ResearchHub AI** revolutionizes academic writing by combining AI-powered content generation with professional conference formatting. Generate publication-quality research papers with proper structure, citations, and formatting—all powered by state-of-the-art language models.

### 🎯 Key Capabilities

- **📝 Complete Paper Generation**: 9-section structure (Abstract → References) with 250-900 words per section
- **🎨 Conference Formats**: IEEE two-column, ACM single-column, Springer LNCS templates
- **🤖 Dual AI Support**: Choose between Ollama (local, free) or OpenAI (cloud)
- **✨ AI Enhancement**: 6-step improvement process for academic rigor
- **🔍 AI Review**: Quality assessment with actionable feedback
- **📤 Export Options**: HTML with print-to-PDF or direct WeasyPrint PDF generation
- **👥 Collaboration**: Team projects with researcher matching

---

## ✨ Features

### 📚 Publication-Quality Papers

#### **AI Content Generation**
- **Abstract** (250-280 words)
  - Quantifiable results
  - Assertive academic tone
  - Clear research objectives
  
- **Introduction** (650-750 words)
  - 10-15 integrated citations
  - Logical argument building
  - Problem establishment
  


---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** 
- **pip** (Python package manager)
- **Ollama** (for local AI) OR **OpenAI API Key** (for cloud AI)

### Installation (3 Steps)

#### 1️⃣ Clone & Navigate
```powershell
cd C:\path\to\ResearchHub
```

#### 2️⃣ Run Setup Script
```powershell
.\setup.ps1
```

This automatically:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Sets up `.env` configuration
- ✅ Creates database structure

#### 3️⃣ Configure AI Provider

**Option A: Ollama (Free, Local)**
```powershell
# Install Ollama from https://ollama.ai
ollama pull mistral

# Edit .env file:
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

**Option B: OpenAI (Cloud, Paid)**
```powershell
# Edit .env file:
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
```

#### 🎉 Start Application
```powershell
.\start.ps1
```

Access at: **http://localhost:5000**

---

## 📖 Usage Guide

### Generating Your First Paper

1. **Register/Login**
   - Create account with email/password
   - Complete researcher profile

2. **Create New Paper**
   - Navigate to "Papers" section
   - Click "New Paper"
   - Fill metadata:
     - Title
     - Domain (e.g., "Artificial Intelligence")
     - Keywords (comma-separated)
     - Research objective
     - Methodology type

3. **Generate Sections**
   - Click "Generate" next to any section
   - AI produces publication-quality content
   - Sections generated with proper citations

4. **Improve Content**
   - Select text in any section
   - Click "AI Improve"
   - 6-step enhancement process applied

5. **Review Quality**
   - Click "AI Review"
   - Get detailed feedback on:
     - Structure
     - Clarity
     - Logic
     - Completeness

6. **Export Paper**
   - Choose format (IEEE/ACM/Springer)
   - Click export button
   - Opens in new tab
   - Use browser's "Print to PDF" or install WeasyPrint

### Example Workflow

```
1. Create Paper
   ↓
2. Generate Abstract
   ↓
3. Generate Introduction
   ↓
4. Generate all remaining sections
   ↓
5. AI Improve on each section
   ↓
6. AI Review for quality check
   ↓
7. Export to IEEE format
   ↓
8. Print to PDF
```

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Flask | 3.0.0 | Web framework |
| SQLAlchemy | 2.0.23 | ORM |
| Flask-Login | 0.6.3 | Authentication |
| Flask-SocketIO | 5.3.5 | Real-time chat |
| bcrypt | 4.1.2 | Password hashing |

### AI/ML
| Technology | Version | Purpose |
|-----------|---------|---------|
| OpenAI | 1.6.1 | Cloud AI |
| Ollama | Latest | Local AI |
| Langchain | 0.1.0 | AI orchestration |

### PDF Export
| Technology | Version | Purpose |
|-----------|---------|---------|
| WeasyPrint | 60.1 | PDF generation (optional) |
| ReportLab | 4.0.7 | PDF utilities |
| PyPDF2 | 3.0.1 | PDF manipulation |

### Frontend
- **Tailwind CSS** - Modern styling
- **Font Awesome** - Icons
- **JavaScript** - Interactivity
- **HTML5** - Structure

---

## 📁 Project Structure

```
ResearchHub/
├── 📂 app/
│   ├── 📄 __init__.py              # App factory
│   ├── 📄 models.py                # Database models (User, Paper, Project, etc.)
│   ├── 📂 routes/
│   │   ├── 📄 auth.py              # Login, register, logout
│   │   ├── 📄 dashboard.py         # Main dashboard
│   │   ├── 📄 profile.py           # User profiles
│   │   ├── 📄 research.py          # Researcher discovery
│   │   ├── 📄 project.py           # Project management
│   │   ├── 📄 chat.py              # Messaging system
│   │   └── 📄 ai_paper.py          # AI paper generation ⭐
│   ├── 📂 services/
│   │   └── 📄 ai_service.py        # AI integration (Ollama/OpenAI)
│   ├── 📂 templates/
│   │   ├── 📂 paper/
│   │   │   ├── 📄 paper_ieee.html  # IEEE template
│   │   │   ├── 📄 paper_acm.html   # ACM template
│   │   │   ├── 📄 paper_springer.html # Springer template
│   │   │   └── 📄 view.html        # Paper viewer
│   └── 📂 sockets/
│       └── 📄 chat_events.py       # WebSocket handlers
├── 📄 config.py                    # Configuration
├── 📄 run.py                       # Application entry point
├── 📄 requirements.txt             # Production dependencies
├── 📄 requirements-dev.txt         # Development dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 Dockerfile                   # Docker image
├── 📄 docker-compose.yml           # Docker orchestration
├── 📄 CHANGELOG.md                 # Version history
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 LICENSE                      # MIT License
├── 📄 README.md                    # This file
├── 📄 QUICKSTART.md                # Quick start guide
├── 🔧 setup.ps1                    # Windows setup script
└── 🔧 start.ps1                    # Windows start script
```

---

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-this-in-production

# AI Provider (choose one)
AI_PROVIDER=ollama  # or "openai"

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=sqlite:///researchhub.db

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### AI Model Options

**Ollama Models:**
- `mistral` (recommended) - 7B parameters, fast, good quality
- `llama2` - 7B/13B/70B variants
- `codellama` - Specialized for code
- `phi` - Microsoft's small model

**OpenAI Models:**
- `gpt-4` - Most powerful, best quality
- `gpt-4-turbo` - Faster, cheaper
- `gpt-3.5-turbo` - Fast, economical

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```powershell
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This starts:
- **Web Application** (Port 5000)
- **Ollama AI Service** (Port 11434)
- **Nginx Reverse Proxy** (Port 80/443)

### Manual Docker Build

```powershell
# Build image
docker build -t researchhub-ai .

# Run container
docker run -d -p 5000:5000 --name researchhub researchhub-ai
```

---

## 📚 Documentation

### Additional Guides
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m "Add: Amazing feature"
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Ollama Connection Failed**
```
Error: Connection refused to http://localhost:11434
```
**Solution:**
- Ensure Ollama is running: `ollama serve`
- Check firewall settings
- Verify OLLAMA_BASE_URL in `.env`

#### 2. **WeasyPrint Import Error**
```
WeasyPrint could not import some external libraries
```
**Solution:**
- WeasyPrint is optional
- HTML + Print-to-PDF works without it
- To install: Download GTK runtime for Windows

#### 3. **Database Migration Error**
```
No such column: paper.results
```
**Solution:**
```powershell
# Delete existing database
Remove-Item instance\researchhub.db

# Restart application (will recreate DB)
.\start.ps1
```

#### 4. **Port Already in Use**
```
Address already in use: 5000
```
**Solution:**
```powershell
# Change port in config.py
# Or kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

---

## 🔒 Security

### Production Deployment Checklist

- [ ] Change `SECRET_KEY` in `.env` to a strong random value
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up proper firewall rules
- [ ] Use environment-specific `.env` files
- [ ] Enable rate limiting on API endpoints
- [ ] Regular security audits
- [ ] Keep dependencies updated

### Generate Secure Secret Key

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Roadmap

### Version 1.1 (Q1 2025)
- [ ] LaTeX export support
- [ ] BibTeX integration
- [ ] Multi-domain support (beyond AI)
- [ ] Advanced citation management
- [ ] Collaborative real-time editing

### Version 1.2 (Q2 2025)
- [ ] Plagiarism detection
- [ ] Version control for papers
- [ ] Git-style diff viewer
- [ ] Paper templates library
- [ ] Custom conference formats

### Version 2.0 (Q3 2025)
- [ ] Cloud synchronization
- [ ] Mobile app (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] AI model fine-tuning
- [ ] Enterprise features

---

## 📊 Performance

### Benchmarks (i5-8250U, 8GB RAM)

| Operation | Ollama (mistral) | OpenAI (GPT-4) |
|-----------|------------------|----------------|
| Abstract Generation | ~15s | ~8s |
| Introduction Generation | ~25s | ~12s |
| Full Paper (9 sections) | ~3-4 min | ~1-2 min |
| AI Improve (single section) | ~20s | ~10s |
| AI Review | ~30s | ~15s |

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2024 ResearchHub AI

You are free to:
✅ Use commercially
✅ Modify
✅ Distribute
✅ Private use

Conditions:
📋 Include original license
📋 State changes made
```

---

## 🙏 Acknowledgments

- **Ollama** - Local AI inference
- **OpenAI** - Cloud AI services
- **Flask** - Web framework
- **Tailwind CSS** - Styling framework
- **Font Awesome** - Icon library
- **WeasyPrint** - PDF generation
- **Research Community** - Inspiration and feedback

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/researchhub/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/yourusername/researchhub/discussions)

---

## 🌟 Show Your Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🤝 Contributing code
- 📢 Sharing with colleagues

---

<div align="center">

**Built with ❤️ for the Research Community**

*Empowering researchers with AI-powered tools*

[⬆ Back to Top](#-researchhub-ai)

</div>
