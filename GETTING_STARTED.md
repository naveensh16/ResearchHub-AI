# 🎯 ResearchHub AI - Complete Setup Guide

Welcome! This guide will have you up and running in **5 minutes**.

---

## ✅ What You're Getting

A complete AI-powered research paper generation platform with:
- ✅ Publication-quality IEEE/ACM/Springer papers
- ✅ AI-powered content generation (9 sections)
- ✅ AI improvement and review features
- ✅ Team collaboration tools
- ✅ Export to conference formats
- ✅ Free local AI (Ollama) or cloud AI (OpenAI)

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Prerequisites Check ✓

**Required:**
- ✅ Windows PC
- ✅ Python 3.10 or higher
- ✅ PowerShell

**Optional:**
- Ollama (for free local AI)
- OpenAI API key (for cloud AI)

### Step 2: Navigate to Project

```powershell
cd C:\Users\Naveen\OneDrive\Desktop\projects\ResearchHub
```

### Step 3: Run Setup Script

```powershell
.\setup.ps1
```

**This automatically:**
- Creates virtual environment
- Installs all 25+ dependencies
- Sets up configuration files
- Creates database structure
- Prepares upload folders

**Takes:** ~2-3 minutes (depending on internet speed)

### Step 4: Configure AI Provider

**Edit `.env` file** (choose one option):

#### Option A: Ollama (Free, Local) ⭐ Recommended

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

**Install Ollama:**
1. Download: https://ollama.ai/download
2. Install Ollama
3. Open PowerShell:
   ```powershell
   ollama pull mistral
   ```

**Advantages:**
- ✅ Completely FREE
- ✅ Runs on your PC
- ✅ No API costs
- ✅ Privacy-focused

#### Option B: OpenAI (Cloud, Paid)

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
```

**Get API Key:**
1. Go to: https://platform.openai.com/api-keys
2. Create account
3. Generate API key
4. Add to `.env`

**Advantages:**
- ✅ More powerful
- ✅ Faster generation
- ✅ Better quality

### Step 5: Start Application

```powershell
.\start.ps1
```

**Access at:** http://localhost:5000

---

## 🎓 First Time Usage

### 1. Create Account

Navigate to: http://localhost:5000

Click **"Register"**

Fill in:
- Name
- Email
- Password
- Institution
- Research domains (e.g., "Artificial Intelligence, Machine Learning")

### 2. Create Your First Paper

1. Click **"Papers"** in navigation
2. Click **"New Paper"**
3. Fill metadata:
   - **Title:** "AI-Powered Research Collaboration Platform"
   - **Domain:** "Artificial Intelligence"
   - **Keywords:** "AI, Collaboration, Research, NLP"
   - **Objective:** "Develop a platform for automated paper generation"
   - **Method:** "Experimental"

### 3. Generate Sections

1. Click **"Edit"** on your paper
2. For each section, click **"Generate"**
3. Wait 15-30 seconds (Ollama) or 5-10 seconds (OpenAI)
4. Content appears automatically

**Generate in order:**
1. Abstract
2. Introduction
3. Problem Statement
4. Literature Review
5. Methodology
6. Results
7. Conclusion
8. Future Work
9. References

### 4. Improve Quality

1. Select any section's text
2. Click **"AI Improve"**
3. AI enhances with 6-step process:
   - Precision
   - Rigor
   - Clarity
   - Polish
   - Formatting
   - Enhancement

### 5. Review Paper

1. Click **"AI Review"**
2. Get feedback on:
   - Structure
   - Clarity
   - Logic
   - Completeness
3. See severity ratings and suggestions

### 6. Export Paper

1. Click **"Export"** dropdown
2. Choose format:
   - IEEE (two-column)
   - ACM (single-column)
   - Springer (LNCS)
3. Opens in new tab
4. Use browser's **"Print to PDF"** or **Ctrl+P**

---

## 🔧 Troubleshooting

### Problem: "Ollama connection failed"

**Solution:**
```powershell
# Start Ollama service
ollama serve
```

Leave this running in a separate PowerShell window.

### Problem: "Port 5000 already in use"

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <process_id> /F

# Or change port in config.py
```

### Problem: "Module not found"

**Solution:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: "Database error"

**Solution:**
```powershell
# Delete old database
Remove-Item instance\researchhub.db

# Restart app (recreates DB)
.\start.ps1
```

### Problem: "WeasyPrint import error"

**Solution:**
- This is **optional** for PDF generation
- HTML + Print-to-PDF works fine without it
- To install: Download GTK runtime for Windows

---

## 📊 Features Overview

### Paper Generation
- **9 Sections:** Abstract → References
- **Word Counts:** 250-900 words per section
- **Citations:** 15-20 realistic references
- **Quality:** Publication-grade
- **Speed:** 3-4 minutes full paper (Ollama)

### Conference Formats
- **IEEE:** Two-column, Times New Roman 10pt
- **ACM:** Single-column, modern style
- **Springer:** LNCS format

### AI Features
- **Generate:** Create any section from scratch
- **Improve:** 6-step enhancement process
- **Review:** Quality assessment with feedback

### Collaboration
- **Teams:** Create team projects
- **Chat:** Real-time messaging
- **Discovery:** Find collaborators
- **Requests:** Send/receive collaboration invites

---

## 📁 Project Files Explained

| File | Purpose |
|------|---------|
| `setup.ps1` | One-time setup script |
| `start.ps1` | Start application |
| `run.py` | Application entry point |
| `config.py` | Configuration settings |
| `.env` | Environment variables (AI config) |
| `requirements.txt` | Python dependencies |
| `README.md` | Main documentation |
| `QUICKSTART.md` | This file |
| `PROJECT_SUMMARY.md` | Complete project overview |

---

## 🎯 Common Use Cases

### Use Case 1: Generate IEEE Conference Paper

1. Create paper with metadata
2. Generate all 9 sections
3. AI Improve on each section
4. Export → IEEE format
5. Print to PDF

**Time:** ~5-10 minutes

### Use Case 2: Improve Existing Draft

1. Create paper
2. Paste existing content in sections
3. Click "AI Improve" on each
4. Export to desired format

**Time:** ~2-5 minutes

### Use Case 3: Team Collaboration

1. Create team project
2. Invite team members
3. Generate paper together
4. Use chat for discussions
5. Export final version

**Time:** Collaborative workflow

---

## 💡 Tips & Best Practices

### For Best Results:

1. **Metadata Matters:**
   - Detailed objective → better generation
   - Specific keywords → relevant content
   - Clear methodology → focused results

2. **Generate in Order:**
   - Abstract first
   - Then Introduction
   - Follow logical sequence

3. **Use AI Improve:**
   - Run on every section
   - Significantly enhances quality
   - Makes content publication-ready

4. **Review Before Export:**
   - Use AI Review feature
   - Check all sections complete
   - Verify citations

5. **Choose Right Format:**
   - IEEE for most conferences
   - ACM for computing research
   - Springer for workshops

---

## 🔐 Security Notes

### For Development:
- ✅ Default settings are fine
- ✅ SQLite database is local
- ✅ No public exposure

### For Production:
- ⚠️ Change `SECRET_KEY` in `.env`
- ⚠️ Use PostgreSQL instead of SQLite
- ⚠️ Enable HTTPS
- ⚠️ Set up firewall
- ⚠️ Use strong passwords

---

## 🐳 Docker Alternative

If you prefer Docker:

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📚 Additional Resources

- **Full Documentation:** [README.md](README.md)
- **Project Overview:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Version History:** [CHANGELOG.md](CHANGELOG.md)

---

## 🆘 Getting Help

### If you get stuck:

1. **Check this guide** - Most common issues covered
2. **Read README.md** - Comprehensive documentation
3. **Review code comments** - Well-documented code
4. **GitHub Issues** - Report bugs or ask questions

---

## 🎉 Success Checklist

After completing setup, you should be able to:

- [ ] Access http://localhost:5000
- [ ] Register new account
- [ ] Create new paper
- [ ] Generate abstract successfully
- [ ] See generated content
- [ ] Use AI Improve
- [ ] Export to IEEE format
- [ ] View formatted paper

If all checked ✅ **You're ready!**

---

## 🚀 Next Steps

Now that you're set up:

1. **Generate your first paper**
2. **Experiment with different sections**
3. **Try all three export formats**
4. **Invite team members** (if working in a team)
5. **Explore collaboration features**

---

## 🌟 Key Features to Try

### Must-Try Features:
1. ⭐ **AI Generate** - Creates entire sections
2. ⭐ **AI Improve** - Enhances quality dramatically
3. ⭐ **AI Review** - Provides actionable feedback
4. ⭐ **IEEE Export** - Professional formatting
5. ⭐ **Team Chat** - Real-time collaboration

---

## 💪 Power User Tips

### Speed Up Generation:
- Use OpenAI (8x faster than Ollama)
- Generate multiple papers simultaneously
- Save templates for reuse

### Improve Quality:
- Run AI Improve twice on important sections
- Use AI Review between improvements
- Manually refine citations

### Collaboration:
- Create project before paper
- Invite team members early
- Use chat for instant feedback

---

## 📊 Performance Expectations

### With Ollama (mistral):
- Abstract: 15 seconds
- Introduction: 25 seconds
- Full paper: 3-4 minutes
- Very good quality ⭐⭐⭐⭐

### With OpenAI (GPT-4):
- Abstract: 8 seconds
- Introduction: 12 seconds
- Full paper: 1-2 minutes
- Excellent quality ⭐⭐⭐⭐⭐

---

## 🎯 Common Questions

**Q: Is this really free?**  
A: Yes! With Ollama, completely free. OpenAI costs ~$0.50-$2 per paper.

**Q: How good is the quality?**  
A: Publication-grade with proper citations, structure, and formatting.

**Q: Can I edit generated content?**  
A: Yes! Edit directly in the web interface.

**Q: Does it work offline?**  
A: Yes with Ollama (local AI). No with OpenAI (requires internet).

**Q: Can I export to Word?**  
A: Currently HTML + Print-to-PDF. Copy content to Word if needed.

**Q: How many papers can I generate?**  
A: Unlimited with Ollama. Limited by API costs with OpenAI.

---

<div align="center">

**🎓 Ready to Generate Your First Paper? 🎓**

**Start the application:**
```powershell
.\start.ps1
```

**Then visit:** http://localhost:5000

---

**Happy Researching! 🚀**

</div>
