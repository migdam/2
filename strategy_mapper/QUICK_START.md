# 🚀 Quick Start Guide

## Get Running in 3 Steps

### Step 1: Install Dependencies

```bash
cd strategy_mapper
./setup.sh
```

This will:
- Install all Python packages
- Initialize the SQLite database
- Set up default strategies (Innovation, Operational Excellence, Sustainability)

### Step 2: Set Your OpenAI API Key

**Option A: Permanent (Recommended)**

For macOS (zsh):
```bash
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc
```

For Linux (bash):
```bash
echo 'export OPENAI_API_KEY="sk-your-actual-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Option B: Temporary (For Testing)**

```bash
export OPENAI_API_KEY='sk-your-actual-key-here'
```

### Step 3: Run the App

```bash
./run.sh
```

Your browser will open to `http://localhost:8501`

## 📱 What You Can Do

### 1️⃣ Manage Strategies (Page 2)
- Add custom strategic pillars
- Edit strategy descriptions
- Delete strategies you don't need

### 2️⃣ Analyze Text (Page 3)
- Paste any text content
- Get instant AI alignment scores
- See explanations for matches
- View radar charts

### 3️⃣ Upload Documents (Page 4)
- Upload PDF, DOCX, or TXT files
- Automatic chunking and analysis
- Chunk-by-chunk scoring
- Export reports

### 4️⃣ View Analytics (Page 1)
- Dashboard with key metrics
- Strategy hit counts
- Alignment heatmaps

### 5️⃣ Semantic Maps (Page 5)
- Visualize content clusters
- See strategy relationships
- Interactive PCA plots

### 6️⃣ History & Timeline (Pages 6-7)
- Search past analyses
- Track trends over time
- Review strategic evolution

## 🎯 Example Workflow

1. **Start with default strategies** or add your own
2. **Analyze a few text snippets** to test the system
3. **Upload a strategic document** (annual report, plan, etc.)
4. **Review the dashboard** to see alignment patterns
5. **Export reports** for sharing with stakeholders
6. **Track timeline** to monitor strategic focus over time

## 💡 Pro Tips

- **Better Descriptions**: More detailed strategy descriptions = better matching
- **Clean Documents**: Well-formatted files yield better chunking
- **Regular Analysis**: Upload documents periodically to track evolution
- **Export Reports**: Use PDF/DOCX exports for presentations

## 🐛 Common Issues

**"Database not initialized"**
```bash
cd strategy_mapper
python db/init_db.py
```

**"OpenAI API error"**
- Check your API key is correct
- Verify you have credits available
- Test with: `echo $OPENAI_API_KEY`

**"Module not found"**
```bash
pip install -r requirements.txt
```

## 🐳 Docker Alternative

If you prefer Docker:

```bash
cd strategy_mapper
docker build -t strategy-mapper .
docker run -p 8501:8501 -e OPENAI_API_KEY='your-key' strategy-mapper
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore advanced features (clustering, summaries, exports)
- Customize strategies for your organization
- Integrate with your workflow

---

**Need Help?** Check the README.md or review the code comments.
