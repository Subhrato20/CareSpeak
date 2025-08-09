# Symptom Search Tool for Vapi

This tool allows Vapi assistants to search for Amazon products based on user symptoms using the Amazon Search API. When users report symptoms or health concerns, the tool will automatically search for relevant health and wellness products and provide recommendations.

## Features

- **Symptom-based Product Search**: Automatically maps common symptoms to relevant product searches
- **Smart Query Building**: Optimizes search queries based on symptom patterns
- **Filtered Results**: Only returns relevant health and wellness products
- **Voice-Optimized Responses**: Formats results for natural voice communication
- **Error Handling**: Robust error handling and fallback mechanisms

## Prerequisites

1. **SearchAPI Account**: You need a SearchAPI account to access the Amazon Search API
   - Sign up at [https://www.searchapi.io/](https://www.searchapi.io/)
   - Get your API key from the dashboard

2. **Vapi Account**: You need a Vapi account to use this tool
   - Sign up at [https://vapi.ai/](https://vapi.ai/)
   - Get your API key and assistant ID

3. **Python Environment**: Python 3.7+ with the required dependencies

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate your virtual environment (if using one)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual credentials
nano .env
```

Your `.env` file should contain:

```env
# Vapi Configuration
VAPI_PUBLIC_KEY=your-actual-vapi-public-key
ASSISTANT_ID=your-actual-assistant-id

# SearchAPI Configuration
SEARCHAPI_API_KEY=your-actual-searchapi-key
```

### 3. Deploy the Tool Server

You need to deploy the symptom search server so Vapi can call it. You have several options:

#### Option A: Local Development (using ngrok)

1. **Install ngrok** (for exposing local server):
   ```bash
   # Install ngrok (if not already installed)
   brew install ngrok  # macOS
   # or download from https://ngrok.com/
   ```

2. **Start the symptom search server**:
   ```bash
   python symptom_search_server.py
   ```

3. **Expose the server with ngrok**:
   ```bash
   ngrok http 5000
   ```

4. **Note the ngrok URL** (e.g., `https://abc123.ngrok.io`)

#### Option B: Deploy to Cloud Platform

Deploy to platforms like:
- **Heroku**: Use the provided `Procfile`
- **Railway**: Connect your GitHub repository
- **Render**: Deploy as a web service
- **Google Cloud Run**: Containerized deployment

### 4. Create the Tool in Vapi

#### Method A: Using Vapi Dashboard

1. Go to [Vapi Dashboard](https://dashboard.vapi.ai)
2. Navigate to **Tools** section
3. Click **Create Tool**
4. Select **Function** as the tool type
5. Configure the tool with these settings:
   - **Tool Name**: `symptom_search_tool`
   - **Description**: `Search for Amazon products based on user symptoms`
   - **Server URL**: `https://your-deployed-server.com/webhook`
   - **Function Name**: `search_products_for_symptoms`
   - **Parameters**: 
     - `symptoms` (required, string)
     - `max_results` (optional, integer, default: 5)

#### Method B: Using Vapi API

You can create the tool programmatically using the Vapi API:

```bash
curl -X POST https://api.vapi.ai/tool \
  -H "Authorization: Bearer YOUR_VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @vapi_tool_config.json
```

*Note: Update the `url` field in `vapi_tool_config.json` with your actual server URL before making the API call.*

### 5. Add Tool to Your Assistant

1. Go to your **Assistant** in the Vapi dashboard
2. Navigate to the **Tools** section
3. Add the `symptom_search_tool` to your assistant
4. Configure the tool messages as needed

## Usage Examples

### Example 1: Basic Symptom Search

**User**: "I have a headache and fever"

**Assistant**: "I'm searching for products that might help with your symptoms. Please wait a moment..."

**Tool Response**: 
```json
{
  "status": "success",
  "symptoms": "headache and fever",
  "search_query": "headache relief medicine fever reducer medicine",
  "results": [
    {
      "title": "Tylenol Extra Strength Acetaminophen 500mg",
      "brand": "Tylenol",
      "price": "$8.99",
      "rating": 4.7,
      "reviews": 15420,
      "description": "Tylenol Extra Strength Acetaminophen 500mg (Rated 4.7 out of 5 stars with 15420 reviews) - Prime eligible"
    }
  ],
  "voice_response": "Based on your symptoms of headache and fever, I found 1 product recommendations: 1. Tylenol Extra Strength Acetaminophen 500mg with a 4.7 star rating from 15420 reviews for $8.99. These are general recommendations. Please consult with a healthcare professional for medical advice, especially if symptoms persist or worsen."
}
```

### Example 2: Complex Symptoms

**User**: "I'm experiencing back pain and trouble sleeping"

**Assistant**: "I'm searching for products that might help with your symptoms. Please wait a moment..."

**Tool Response**: Will search for both back pain relief products and sleep aids.

## Supported Symptoms

The tool includes mappings for common symptoms:

### Pain-Related
- Headache, migraine, back pain, joint pain, muscle pain, toothache

### Cold and Flu
- Fever, cough, sore throat, congestion, runny nose

### Digestive
- Nausea, upset stomach, indigestion, heartburn

### Skin-Related
- Rash, itching, dry skin, acne

### Sleep-Related
- Insomnia, trouble sleeping

### Allergies
- Allergies, seasonal allergies

### General Wellness
- Stress, anxiety, vitamins, supplements

## API Endpoints

The symptom search server provides these endpoints:

- `GET /` - Service information
- `GET /health` - Health check
- `POST /search_symptoms` - Direct symptom search
- `POST /webhook` - Vapi function calling webhook

## Error Handling

The tool includes comprehensive error handling:

- **API Errors**: Handles SearchAPI connection issues
- **Invalid Symptoms**: Graceful handling of unclear symptom descriptions
- **No Results**: Provides helpful fallback responses
- **Server Errors**: Proper error logging and user-friendly messages

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files for local development
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Consider implementing rate limiting for the server
5. **Input Validation**: All user inputs are validated and sanitized

## Troubleshooting

### Common Issues

1. **SearchAPI Key Not Found**
   - Ensure `SEARCHAPI_API_KEY` is set in your `.env` file
   - Verify the key is valid and active

2. **Server Not Accessible**
   - Check if the server is running on the correct port
   - Verify ngrok is running and the URL is correct
   - Test the `/health` endpoint

3. **Tool Not Working in Vapi**
   - Verify the tool is properly configured in Vapi dashboard
   - Check the webhook URL is accessible
   - Review Vapi logs for any errors

4. **No Search Results**
   - Check if the symptoms are too vague
   - Verify the SearchAPI is returning results
   - Review the symptom mappings in `symptom_search_tool.py`

### Debug Mode

To enable debug logging, set the logging level in `symptom_search_server.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the [Vapi Documentation](https://docs.vapi.ai)
- Join the [Vapi Discord Community](https://discord.gg/vapi)
- Review the [SearchAPI Documentation](https://www.searchapi.io/docs)
