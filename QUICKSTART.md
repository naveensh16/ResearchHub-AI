# 🚀 ResearchHub AI - QUICKSTART GUIDE

## ⚡ Get Started in 5 Minutes

### Step 1: Setup (2 minutes)

Open PowerShell in the ResearchHub folder and run:

```powershell
.\setup.ps1
```

This installs everything you need!

### Step 2: Configure AI (1 minute)

**Option A: Use Ollama (Free, Local)** ✨ Recommended

1. Install Ollama: https://ollama.ai/download
2. Open terminal and run:
```powershell
ollama pull mistral
```

That's it! The `.env` file is already configured for Ollama.

**Option B: Use OpenAI (Paid)**

1. Get API key from https://platform.openai.com/api-keys
2. Edit `.env` file:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL=gpt-3.5-turbo
```

### Step 3: Run (1 minute)

```powershell
.\start.ps1
```

### Step 4: Access (30 seconds)

Open browser: **http://localhost:5000**

### Step 5: Test the MVP (1 minute)

1. **Register** - Create an account
2. **Complete Profile** - Add research domains (e.g., "AI, Machine Learning, NLP")
3. **Create Paper** - Click "Papers" → "Generate with AI"
4. **Fill Details:**
   - Title: "AI in Healthcare"
   - Domain: "Artificial Intelligence"
   - Keywords: "AI, Healthcare, Deep Learning"
   - Objective: "Improve diagnosis accuracy"
   - Method: "Deep Learning"
5. **Generate** - Select sections and click "Generate"
6. **Watch AI Work!** 🤖

## 🎯 Key Features to Test

### 1. AI Paper Generation
- Go to Papers → Create New
- Fill metadata
- Select sections to generate
- Edit generated content
- Use "Improve" button on sections

### 2. Research Discovery
- Click "Discover" in navigation
- Search for researchers
- View suggested collaborators (based on matching domains)

### 3. Project Management
- Create a new project
- Choose "Team" type
- Add members (after creating more users)

### 4. Chat System
- Click "Chat" in navigation
- Start conversation with another user
- Real-time messaging with SocketIO

### 5. AI Review
- Open any paper
- Click "Review with AI"
- Get feedback on quality, structure, gaps

## 🐛 Troubleshooting

### "Cannot connect to Ollama"
```powershell
# Check if Ollama is running
ollama serve

# In another terminal, test:
ollama run mistral "Hello"
```

### "ModuleNotFoundError"
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Reinstall
pip install -r requirements.txt
```

### Database errors
```powershell
# Delete and recreate
Remove-Item researchhub.db
python run.py  # Will auto-create
```

### Port already in use
Edit `run.py`, change port:
```python
socketio.run(app, port=5001)  # Changed from 5000
```

## 📝 Test Scenario (Demo-Ready)

**Scenario: Research Team Collaboration**

1. **Create 3 Users:**
   - Alice (AI, Machine Learning)
   - Bob (Healthcare, AI)
   - Carol (Deep Learning, Computer Vision)

2. **As Alice:**
   - Complete profile with domains
   - See Bob suggested (common: AI)
   - Send collaboration request
   - Create project "AI Healthcare System"
   - Generate paper with AI

3. **As Bob:**
   - Accept Alice's request
   - Join Alice's project
   - Chat with Alice
   - Review paper and suggest improvements

4. **As Carol:**
   - Search for "AI" researchers
   - Find Alice
   - Create own paper
   - Use AI to generate sections
   - Request AI review

## 🎨 Customization Quick Tips

### Change Colors
Edit `app/templates/base.html` - look for `indigo` classes

### Add Paper Sections
Edit `app/services/ai_service.py` - add to `section_prompts`

### Adjust Matching
Edit `config.py`:
```python
MIN_COMMON_TAGS = 2  # Require 2 matching tags
```

## 📊 MVP Checklist

- [x] Authentication (Register, Login, Logout)
- [x] User Profiles
- [x] Research Discovery
- [x] Collaboration Requests
- [x] Project Management
- [x] Team Invitations
- [x] Real-time Chat (1-to-1 & Group)
- [x] AI Paper Generator (7 sections)
- [x] AI Text Improvement
- [x] AI Paper Review
- [x] Dashboard with Stats
- [x] Responsive Design (Tailwind)

## 🚀 Next Steps After MVP

1. **Add More Paper Sections**
   - Results & Discussion
   - Experimental Setup
   - Related Work

2. **Export Features**
   - PDF generation
   - LaTeX export
   - Word document

3. **Advanced Matching**
   - ML-based recommendations
   - Collaboration history
   - Citation network analysis

4. **Notifications**
   - Email alerts
   - In-app notifications
   - Real-time updates

5. **File Uploads**
   - Supporting documents
   - Images & figures
   - Datasets

## 💡 Pro Tips

1. **AI Quality:** Longer, more detailed prompts = better output
2. **Matching:** Add 3-5 domain tags for best suggestions
3. **Chat:** Use project chat for team discussions
4. **Review:** Run AI review before finalizing papers
5. **Profile:** Complete profile increases collaborator matches

## 🎓 Demo Script (5 minutes)

"ResearchHub AI helps researchers collaborate and write papers faster.

**[Show Dashboard]** Here's your research hub - projects, collaborators, papers.

**[Discovery]** Find researchers with matching interests - AI matches based on domains.

**[Create Project]** Start a research project, invite team members.

**[Generate Paper]** Now the magic - AI generates entire paper sections.

**[Show Generation]** Just describe your research - AI writes introduction, methodology, everything.

**[Edit]** Human-in-the-loop - you control and improve every section.

**[AI Review]** Get intelligent feedback - missing sections, weak arguments, improvements.

**[Chat]** Collaborate in real-time with your team.

That's ResearchHub AI - making research collaboration smarter and faster!"

---

## ✅ You're Ready!

The MVP is complete and ready to demo. Start with:
```powershell
.\start.ps1
```

Open http://localhost:5000 and explore! 🚀
