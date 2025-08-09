# Vapi Tools

This directory contains custom tools for Vapi assistants. Each tool is designed to be deployed as a separate service and integrated with Vapi via webhooks.

## Tools Included

### 1. Symptom Search Tool

A tool that searches for Amazon products based on user symptoms using the Amazon Search API.

**Features:**
- Maps common symptoms to relevant product searches
- Returns filtered, relevant health and wellness products
- Formats results for voice communication
- Comprehensive error handling

**Files:**
- `symptom_search_tool.py` - Core tool logic
- `symptom_search_server.py` - Flask server for deployment
- `test_symptom_search.py` - Test script
- `vapi_tool_config.json` - Vapi tool configuration

## Quick Start

### 1. Set up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your credentials
nano .env
```

Required environment variables:
- `SEARCHAPI_API_KEY` - Your SearchAPI key (for symptom search tool)

### 3. Test the Tool

```bash
# Test symptom search tool
python test_symptom_search.py
```

### 4. Deploy

Choose a deployment platform from the options below:

#### Option A: Render (Recommended)

1. Add `render.yaml` to your repository root:
```yaml
services:
  - type: web
    name: symptom-search-tool
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn symptom_search_server:app
    envVars:
      - key: SEARCHAPI_API_KEY
        sync: false
```

2. Connect your repository to Render and deploy.

#### Option B: Railway

1. Connect your repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically

#### Option C: Heroku

```bash
# Install Heroku CLI
brew install heroku

# Login and create app
heroku login
heroku create your-app-name
heroku config:set SEARCHAPI_API_KEY=your-searchapi-key

# Deploy
git push heroku main
```

### 5. Integrate with Vapi

1. Get your deployed URL (e.g., `https://your-app.onrender.com`)
2. Update `vapi_tool_config.json` with your URL
3. Create the tool in Vapi dashboard or via API
4. Add the tool to your assistant

## Project Structure

```
my-vapi-tools/
├── symptom_search_tool.py      # Core symptom search logic
├── symptom_search_server.py    # Flask server for deployment
├── test_symptom_search.py      # Test script
├── vapi_tool_config.json      # Vapi tool configuration
├── requirements.txt           # Python dependencies
├── Procfile                  # Deployment configuration
├── runtime.txt               # Python version
├── env.example              # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── SYMPTOM_SEARCH_README.md # Detailed symptom search documentation
└── DEPLOYMENT_GUIDE.md     # Complete deployment guide
```

## Development

### Adding New Tools

1. Create a new Python file for your tool logic
2. Create a Flask route in `symptom_search_server.py` or create a new server file
3. Add tests in a separate test file
4. Update documentation

### Testing

```bash
# Run all tests
python test_symptom_search.py

# Test specific functionality
python -c "from symptom_search_tool import search_products_for_symptoms; print(search_products_for_symptoms('headache'))"
```

## Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions for various platforms.

## Support

- **Vapi Documentation**: https://docs.vapi.ai
- **Vapi Community**: https://discord.gg/vapi
- **SearchAPI Documentation**: https://www.searchapi.io/docs
