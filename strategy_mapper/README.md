# 📊 Strategy Mapper

An AI-powered strategic alignment analyzer that uses OpenAI embeddings and GPT to map content against organizational strategies.

## 🌟 Features

- **AI-Powered Analysis**: Uses OpenAI's latest embedding models for semantic understanding
- **Multi-Strategy Mapping**: Define and manage multiple strategic pillars
- **Document Processing**: Upload PDF, DOCX, or TXT files for automatic chunking and analysis
- **Visual Analytics**:
  - PCA semantic maps
  - Radar charts
  - Heatmaps
  - Timeline views
- **Export Capabilities**: Generate PDF and DOCX reports
- **Executive Summaries**: AI-generated strategic insights and recommendations
- **Strategy Clustering**: Visualize relationships between strategies

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**

```bash
cd strategy_mapper
```

2. **Run the setup script**

```bash
./setup.sh
```

3. **Set your OpenAI API key**

For macOS (zsh):
```bash
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.zshrc
source ~/.zshrc
```

For Linux (bash):
```bash
echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
source ~/.bashrc
```

Or set it temporarily:
```bash
export OPENAI_API_KEY='sk-your-key'
```

4. **Run the application**

```bash
./run.sh
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
strategy_mapper/
├── app.py                      # Main Streamlit application
├── db/
│   ├── schema.sql             # Database schema
│   ├── init_db.py             # Database initialization
│   └── db_utils.py            # Database utilities
├── ai/
│   ├── embeddings.py          # OpenAI embedding functions
│   ├── scorer.py              # Similarity scoring
│   ├── reasoning.py           # GPT-powered explanations
│   └── summary_agent.py       # Executive summary generation
├── utils/
│   ├── file_loader.py         # PDF/DOCX/TXT loading
│   ├── chunker.py             # Smart text chunking
│   ├── viz.py                 # Visualization utilities
│   ├── clustering.py          # Strategy clustering
│   ├── report_export.py       # PDF export
│   └── docx_export.py         # DOCX export
├── pages/
│   ├── 01_Dashboard.py        # Analytics dashboard
│   ├── 02_Strategies.py       # Strategy management
│   ├── 03_Analyze_Text.py     # Text analysis
│   ├── 04_Upload_Document.py  # Document upload
│   ├── 05_Semantic_Map.py     # PCA visualization
│   ├── 06_History.py          # Analysis history
│   └── 07_Timeline.py         # Timeline view
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script
├── run.sh                     # Run script
└── README.md                  # This file
```

## 🎯 Usage

### 1. Manage Strategies

Navigate to **Strategies** page to:
- View existing strategic pillars
- Add new strategies with descriptions
- Delete strategies you no longer need

### 2. Analyze Text

Go to **Analyze Text** to:
- Paste any text content
- Get instant AI-powered alignment scoring
- See explanations for why content matches specific strategies
- View radar charts showing alignment across all strategies

### 3. Upload Documents

Use **Upload Document** to:
- Upload PDF, DOCX, or TXT files
- Automatically chunk documents into meaningful segments
- Analyze each chunk against all strategies
- Get detailed explanations for each chunk

### 4. View Analytics

Explore the **Dashboard** to:
- See recent analyses
- View strategy hit counts
- Analyze heatmaps of alignments

### 5. Semantic Mapping

Visit **Semantic Map** to:
- Visualize how your content clusters semantically
- See relationships between different pieces of content
- Identify patterns in strategic alignment

### 6. Timeline Analysis

Check **Timeline** to:
- Track how strategy alignments evolve over time
- Identify trends in your strategic focus

### 7. Review History

Use **History** to:
- Search past analyses
- Filter by strategy or content
- Review historical patterns

## 🔧 Advanced Features

### Embedding Cache

The system automatically caches embeddings to:
- Reduce API costs
- Speed up repeated analyses
- Maintain consistency across analyses

### Agentic Chunking

Smart document chunking that:
- Splits on paragraph boundaries
- Merges short segments for better context
- Handles various document formats

### Multi-Model Fallback

Automatic fallback from:
- `text-embedding-3-large` (primary, high quality)
- `text-embedding-3-small` (fallback, faster/cheaper)

## 📊 Export Options

### PDF Reports

Generate professional PDF reports with:
- Full analysis results
- Chunk-by-chunk breakdowns
- Strategy alignments
- AI explanations

### DOCX Reports

Create editable Word documents with:
- Formatted analysis results
- Easy sharing and collaboration
- Professional styling

### Executive Summaries

AI-generated summaries including:
- Overall strategic alignment
- Key insights
- Missed opportunities
- Risk identification
- Actionable recommendations

## 🐳 Docker Deployment (Optional)

Build and run with Docker:

```bash
docker build -t strategy-mapper .
docker run -p 8501:8501 -e OPENAI_API_KEY='your-key' strategy-mapper
```

## 💡 Tips

1. **Strategy Descriptions**: Make strategy descriptions clear and detailed for better matching
2. **Document Quality**: Clean, well-formatted documents yield better results
3. **Chunk Size**: The system automatically optimizes chunk sizes for embedding quality
4. **Regular Analysis**: Use timeline view to track strategic evolution over time

## 🔒 Security

- Never commit your OpenAI API key to version control
- Use environment variables for API keys
- The local SQLite database stores embeddings locally
- No data is sent to external services except OpenAI's API

## 🧪 Testing

### Running Tests

The project includes comprehensive automated tests:

```bash
# Run all tests
./run_tests.sh

# Run unit tests only
./run_tests.sh unit

# Run integration tests only
./run_tests.sh integration

# Run with coverage report
./run_tests.sh coverage
```

### Test Coverage

- **Unit Tests**: 40+ tests covering database, AI, and utils layers
- **Integration Tests**: 15+ tests for end-to-end workflows
- **Mocked APIs**: All OpenAI calls are mocked for fast, cost-free testing
- **Coverage Target**: 80%+

### CI/CD

Tests run automatically via GitHub Actions on:
- Push to main/develop branches
- Pull requests
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Multiple OS (Ubuntu, macOS)

See [TESTING.md](TESTING.md) for detailed testing documentation.

## 🐛 Troubleshooting

**Database not initialized?**
```bash
python db/init_db.py
```

**OpenAI API errors?**
- Check your API key is set correctly
- Verify you have API credits available
- Ensure you're using a valid key format

**Import errors?**
```bash
pip install -r requirements.txt
```

**Test failures?**
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests with verbose output
./run_tests.sh all -vv
```

## 📝 License

This project is provided as-is for educational and business use.

## 🤝 Contributing

Feel free to extend this system with:
- Additional visualization types
- New export formats
- Custom strategy models
- Integration with other AI providers

## 📧 Support

For issues or questions, please refer to the documentation or create an issue in your repository.

---

Built with ❤️ using Streamlit, OpenAI, and Python
