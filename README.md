# OnFabric MVP - Personalized Dashboard Generator

> Transform your digital footprint into beautiful, personalized dashboards

A demo application that analyzes user interaction patterns across multiple platforms (Instagram, Google, Pinterest) and generates custom dashboard interfaces with dynamically selected widgets, themes, and content.

## ✨ Features

- 🎨 **Dynamic UI Generation** - Dashboards adapt to user interests and aesthetics
- 🎭 **Persona-Driven Curation** - Content selected based on behavioral patterns
- 🌈 **Custom Theming** - Unique color schemes and typography per user
- 📊 **Multi-Provider Integration** - Instagram, Google, Pinterest data sources
- 🎯 **Smart Widget Selection** - Relevant widgets based on user activity

## 🚀 Quick Start (Mock Data Demo)

No API keys required! Run with demo data:

```bash
# Clone the repository
git clone <your-repo-url>
cd onfabric_mvp

# Install dependencies
npm install                    # Frontend dependencies
pip install -e .               # Python package in editable mode

# Start the application
npm run dev                    # Frontend → http://localhost:3000
python -m uvicorn backend.app.main:app --reload  # Backend → http://localhost:8000
```

Visit `http://localhost:3000` to see a demo dashboard generated from mock data.

## 🏗️ Architecture

```
User Data → Pattern Analysis → Dashboard Generation
   ↓              ↓                    ↓
OnFabric     Extract Topics      Select Widgets
  API        Identify Themes     Choose Colors
             Analyze Activity    Build Layout
```

**Pipeline:**
1. **Data Collection**: Fetch user interactions from OnFabric API
2. **Pattern Extraction**: Analyze behavior to identify interests and themes
3. **Content Enrichment**: Query external APIs for relevant content
4. **Dashboard Assembly**: Generate UI with widgets, theme, and layout
5. **Frontend Rendering**: Display personalized dashboard

See [docs/README.md](docs/README.md) for detailed architecture documentation.

## 🔑 Using Real Data

### Prerequisites

- OnFabric API access (sign up at [onfabric.com](https://onfabric.com))
- Optional: Weather API, Search API for content enrichment

### Setup

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys**:
   ```bash
   MOCK_MODE=false
   ONFABRIC_API_KEY=your_actual_key_here
   ```

3. **Restart the application**:
   ```bash
   # Backend will now fetch real user data
   python -m uvicorn backend.app.main:app --reload
   ```

### Data Flow

With real data enabled:
- Backend fetches user interactions from OnFabric API
- Pattern extraction runs on actual behavioral data
- Enrichment APIs provide live content recommendations
- Dashboard updates reflect real user interests

## 🧪 Development

### Project Structure

```
onfabric_mvp/
├── backend/              # FastAPI backend
│   └── app/
│       ├── main.py       # API endpoints
│       └── services/     # Business logic
├── frontend/             # React frontend
│   └── src/
│       ├── components/   # UI components
│       └── pages/        # Page layouts
├── fabric_dashboard/     # Core dashboard logic
│   ├── core/            # Data fetching, pattern analysis
│   ├── models/          # Data schemas
│   └── tests/           # Test suite
└── docs/                # Documentation
```

### Running Tests

```bash
# All tests with mock data (default)
pytest fabric_dashboard/tests/ -v

# Specific test file
pytest fabric_dashboard/tests/test_dashboard_builder.py -v

# With real API data (requires .env configuration)
MOCK_MODE=false pytest fabric_dashboard/tests/ -v
```

### Adding New Widget Types

1. Create widget component in `frontend/src/components/widgets/`
2. Define widget schema in `fabric_dashboard/models/ui_components.py`
3. Add widget selection logic in `fabric_dashboard/core/dashboard_builder.py`
4. Add tests in `fabric_dashboard/tests/test_dashboard_builder.py`

## 📚 Documentation

- [Architecture Overview](docs/README.md) - Detailed system design
- [Design Documents](docs/plans/) - Technical design decisions

## 🛠️ Tech Stack

**Backend:**
- FastAPI - REST API framework
- Pydantic - Data validation
- Python 3.11+

**Frontend:**
- React 18
- Vite - Build tool
- Tailwind CSS - Styling

**Testing:**
- pytest - Test framework
- Mock data fixtures for development

## 📄 License

MIT License - see LICENSE file for details

---

**Note**: This is a demonstration project showcasing personalized UI generation. The mock data mode allows exploration without API credentials.
