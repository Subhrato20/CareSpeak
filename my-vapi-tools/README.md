# Vapi Tools - Multi-Layer GPT Pipeline

This directory contains custom tools for Vapi assistants. The main tool is a sophisticated multi-layer GPT pipeline that processes user conversations to extract symptoms, recommend medicines, search Amazon, and provide natural language responses.

## Tools Included

### 1. Symptom Search Pipeline (Multi-Layer GPT)

A sophisticated pipeline that processes user conversations through multiple GPT layers to provide personalized medicine recommendations.

**Pipeline Flow:**
1. **Layer 1**: User conversation → GPT extracts symptoms
2. **Layer 2**: Symptoms → GPT recommends specific medicines  
3. **Layer 3**: Medicine names → SearchAPI finds products on Amazon
4. **Layer 4**: SearchAPI JSON → GPT extracts details and formats natural language response

**Features:**
- Intelligent symptom extraction from natural conversation
- Smart medicine recommendation based on symptoms
- Real-time Amazon product search
- Natural language response generation
- Comprehensive error handling

**Files:**
- `symptom_search_pipeline.py` - Core pipeline logic
- `symptom_search_server.py` - Flask server for deployment
- `test_pipeline.py` - Comprehensive test script
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

# Start the server
python symptom_search_server.py
# Server will run on http://localhost:8080
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your credentials
nano .env
```

Required environment variables:
- `SEARCHAPI_API_KEY` - Your SearchAPI key (for Amazon searches)
- `OPENAI_API_KEY` - Your OpenAI API key (for GPT processing)

### 3. Test the Pipeline

```bash
# Test the complete pipeline
python test_pipeline.py
```

### 4. Deploy

Choose a deployment platform from the options below:

#### Option A: Render (Recommended)

1. **Add `render.yaml` to your repository root**:
```yaml
services:
  - type: web
    name: symptom-search-pipeline
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn symptom_search_server:app
    envVars:
      - key: SEARCHAPI_API_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
```

2. **Connect your repository to Render and deploy**.

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

# Add environment variables
heroku config:set SEARCHAPI_API_KEY=your-searchapi-key
heroku config:set OPENAI_API_KEY=your-openai-key

# Deploy
git push heroku main
```

### 5. Integrate with Vapi

1. Get your deployed URL (e.g., `https://your-app.onrender.com`)
2. Update `vapi_tool_config.json` with your URL
3. Create the tool in Vapi dashboard or via API
4. Add the tool to your assistant

## Pipeline Architecture

### Layer 1: Symptom Extraction
- **Input**: User conversation (e.g., "I've been having headaches and fever for 2 days")
- **Process**: GPT analyzes conversation to extract specific symptoms
- **Output**: Structured symptom data (symptoms list, severity, duration)

### Layer 2: Medicine Recommendation  
- **Input**: Extracted symptoms
- **Process**: GPT recommends appropriate over-the-counter medicines
- **Output**: List of specific medicine names (e.g., ["acetaminophen", "ibuprofen"])

### Layer 3: Amazon Search
- **Input**: Medicine names
- **Process**: SearchAPI searches Amazon for each medicine
- **Output**: Product listings with prices, ratings, reviews

### Layer 4: Response Formatting
- **Input**: Amazon search results + original symptoms
- **Process**: GPT extracts key details and formats natural language response
- **Output**: Conversational response ready for voice communication

## Usage Examples

### Example 1: Basic Symptom Conversation

**User**: "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy."

**Pipeline Process**:
1. **Layer 1**: Extracts symptoms: ["headache", "fever", "fatigue", "body aches"]
2. **Layer 2**: Recommends medicines: ["acetaminophen", "ibuprofen"]
3. **Layer 3**: Searches Amazon for these medicines
4. **Layer 4**: Formats natural response: "Based on your symptoms of headache and fever, I found some recommendations including Tylenol Extra Strength for $8.99 with 4.7 stars from 15,420 reviews..."

### Example 2: Complex Health Concerns

**User**: "My throat is really sore and I have a cough that won't go away. It's been bothering me for about a week now."

**Pipeline Process**:
1. **Layer 1**: Extracts symptoms: ["sore throat", "persistent cough"]
2. **Layer 2**: Recommends medicines: ["throat lozenges", "dextromethorphan", "acetaminophen"]
3. **Layer 3**: Searches Amazon for these medicines
4. **Layer 4**: Formats natural response with product recommendations

## API Endpoints

The symptom search pipeline server provides these endpoints:

- `GET /` - Service information and pipeline details
- `GET /health` - Health check
- `POST /process_conversation` - Direct conversation processing
- `POST /webhook` - Vapi function calling webhook

## Testing

### Complete Pipeline Testing

```bash
# Test all pipeline layers and functionality
python test_pipeline.py
```

### Individual Layer Testing

```bash
# Test specific layers
python -c "from symptom_search_pipeline import SymptomSearchPipeline; pipeline = SymptomSearchPipeline(); print(pipeline.extract_symptoms_from_conversation('I have a headache'))"
```

## Project Structure

```
my-vapi-tools/
├── symptom_search_pipeline.py    # Multi-layer GPT pipeline logic
├── symptom_search_server.py      # Flask server for deployment
├── test_pipeline.py             # Comprehensive test script
├── vapi_tool_config.json        # Vapi tool configuration
├── requirements.txt             # Python dependencies
├── Procfile                    # Deployment configuration
├── runtime.txt                 # Python version
├── render.yaml                 # Render deployment config
├── .gitignore                 # Git ignore rules
├── env.example                # Environment variables template
├── quick_start.sh             # Automated setup script
├── README.md                  # This file
├── DEPLOYMENT_GUIDE.md        # Complete deployment instructions
└── DEPLOY_QUICK.md           # Quick deployment guide
```

## Development

### Adding New Layers

1. Create a new method in `SymptomSearchPipeline` class
2. Add the layer to the `process_conversation` method
3. Update tests in `test_pipeline.py`
4. Update documentation

### Customizing Prompts

Each layer uses specific GPT prompts that can be customized:
- **Layer 1**: `extract_symptoms_from_conversation` method
- **Layer 2**: `recommend_medicines_from_symptoms` method  
- **Layer 4**: `extract_medicine_details_and_format_response` method

## Error Handling

The pipeline includes comprehensive error handling:
- **API Errors**: Handles OpenAI and SearchAPI connection issues
- **Invalid Inputs**: Graceful handling of unclear conversations
- **No Results**: Provides helpful fallback responses
- **Server Errors**: Proper error logging and user-friendly messages

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files for local development
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Consider implementing rate limiting for production use
5. **Input Validation**: All user inputs are validated and sanitized

## Troubleshooting

### Common Issues

1. **OpenAI API Key Not Found**
   - Ensure `OPENAI_API_KEY` is set in your `.env` file
   - Verify the key is valid and has sufficient credits

2. **SearchAPI Key Not Found**
   - Ensure `SEARCHAPI_API_KEY` is set in your `.env` file
   - Verify the key is valid and has sufficient credits

3. **Pipeline Failing**
   - Check individual layer logs
   - Verify all API keys are working
   - Test with simpler conversations first

4. **Response Quality Issues**
   - Customize GPT prompts for better results
   - Adjust temperature and max_tokens parameters
   - Add more context to prompts

## Support

- **Vapi Documentation**: https://docs.vapi.ai
- **Vapi Community**: https://discord.gg/vapi
- **OpenAI Documentation**: https://platform.openai.com/docs
- **SearchAPI Documentation**: https://www.searchapi.io/docs
