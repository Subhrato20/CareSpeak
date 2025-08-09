# Postman Testing Guide for Symptom Search Pipeline

## Overview

Your symptom search pipeline uses **HTTP endpoints**, not WebSocket connections, so you can easily test it with Postman. Here's how to test each endpoint.

## Prerequisites

1. **Local Server Running**: Start your Flask server locally
   ```bash
   cd my-vapi-tools
   python symptom_search_server.py
   ```
   Server will run on `http://localhost:5000`

2. **Environment Variables**: Make sure your `.env` file is configured with:
   - `SEARCHAPI_API_KEY`
   - `OPENAI_API_KEY`

## Endpoints to Test

### 1. Health Check Endpoint

**Request:**
- **Method**: `GET`
- **URL**: `http://localhost:5000/health`
- **Headers**: None required

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "symptom-search-pipeline"
}
```

### 2. Service Information Endpoint

**Request:**
- **Method**: `GET`
- **URL**: `http://localhost:5000/`
- **Headers**: None required

**Expected Response:**
```json
{
  "service": "Symptom Search Pipeline",
  "version": "2.0.0",
  "description": "Multi-layer GPT pipeline for symptom extraction, medicine recommendation, and natural language response generation",
  "endpoints": {
    "health": "/health",
    "process_conversation": "/process_conversation",
    "webhook": "/webhook"
  },
  "pipeline_steps": [
    "Layer 1: Extract symptoms from conversation using GPT",
    "Layer 2: Recommend medicines based on symptoms using GPT",
    "Layer 3: Search for medicines on Amazon using SearchAPI",
    "Layer 4: Extract details and format natural language response using GPT"
  ]
}
```

### 3. Process Conversation Endpoint (Main Pipeline)

**Request:**
- **Method**: `POST`
- **URL**: `http://localhost:5000/process_conversation`
- **Headers**:
  - `Content-Type: application/json`

**Body (JSON):**
```json
{
  "conversation": "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy.",
  "max_results": 3
}
```

**Expected Response:**
```json
{
  "status": "success",
  "conversation": "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy.",
  "pipeline_steps": [
    "symptom_extraction",
    "medicine_recommendation", 
    "amazon_search",
    "response_formatting"
  ],
  "symptoms": {
    "symptoms": ["headache", "fever", "fatigue", "body aches"],
    "severity": "moderate",
    "duration": "2 days",
    "context": "User has been experiencing these symptoms for the past 2 days"
  },
  "recommended_medicines": ["acetaminophen", "ibuprofen"],
  "search_results": {
    "status": "success",
    "total_results": 6,
    "results": [
      {
        "title": "Tylenol Extra Strength Acetaminophen 500mg",
        "brand": "Tylenol",
        "price": "$8.99",
        "rating": 4.7,
        "reviews": 15420,
        "link": "https://amazon.com/...",
        "thumbnail": "https://...",
        "is_prime": true,
        "medicine_name": "acetaminophen"
      }
    ]
  },
  "natural_response": "Based on your symptoms of headache and fever...",
  "voice_response": "Based on your symptoms of headache and fever..."
}
```

### 4. Webhook Endpoint (Vapi Integration)

**Request:**
- **Method**: `POST`
- **URL**: `http://localhost:5000/webhook`
- **Headers**:
  - `Content-Type: application/json`

**Body (JSON) - Vapi Format:**
```json
{
  "functionCall": {
    "name": "process_symptom_conversation",
    "arguments": {
      "conversation": "I have a sore throat and cough",
      "max_results": 3
    }
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "conversation": "I have a sore throat and cough",
  "pipeline_steps": ["symptom_extraction", "medicine_recommendation", "amazon_search", "response_formatting"],
  "symptoms": {
    "symptoms": ["sore throat", "cough"],
    "severity": "unknown",
    "duration": null,
    "context": null
  },
  "recommended_medicines": ["throat lozenges", "dextromethorphan"],
  "search_results": {
    "status": "success",
    "total_results": 4,
    "results": [...]
  },
  "natural_response": "Based on your symptoms of sore throat and cough...",
  "voice_response": "Based on your symptoms of sore throat and cough..."
}
```

## Postman Collection Setup

### 1. Create a New Collection

1. Open Postman
2. Click "New" → "Collection"
3. Name it "Symptom Search Pipeline"

### 2. Create Environment Variables

1. Click "Environments" → "New Environment"
2. Name it "Local Development"
3. Add these variables:
   - `base_url`: `http://localhost:5000`
   - `conversation`: `I've been having headaches and fever for the past 2 days`

### 3. Create Requests

#### Request 1: Health Check
- **Name**: `Health Check`
- **Method**: `GET`
- **URL**: `{{base_url}}/health`

#### Request 2: Service Info
- **Name**: `Service Information`
- **Method**: `GET`
- **URL**: `{{base_url}}/`

#### Request 3: Process Conversation
- **Name**: `Process Conversation`
- **Method**: `POST`
- **URL**: `{{base_url}}/process_conversation`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "conversation": "{{conversation}}",
  "max_results": 3
}
```

#### Request 4: Webhook Test
- **Name**: `Webhook Test`
- **Method**: `POST`
- **URL**: `{{base_url}}/webhook`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "functionCall": {
    "name": "process_symptom_conversation",
    "arguments": {
      "conversation": "{{conversation}}",
      "max_results": 3
    }
  }
}
```

## Testing Scenarios

### Scenario 1: Basic Symptoms
```json
{
  "conversation": "I have a headache"
}
```

### Scenario 2: Complex Symptoms
```json
{
  "conversation": "I've been experiencing severe back pain for the past week, and I'm also having trouble sleeping. The pain is getting worse."
}
```

### Scenario 3: Cold/Flu Symptoms
```json
{
  "conversation": "I have a sore throat, fever, and cough. I feel really congested and can't sleep well at night."
}
```

### Scenario 4: Allergy Symptoms
```json
{
  "conversation": "My allergies are really bad right now. My nose is constantly running, my eyes are itchy, and I keep sneezing."
}
```

## Error Testing

### Test 1: Missing Conversation
```json
{
  "max_results": 3
}
```
**Expected**: 400 error with "Conversation parameter is required"

### Test 2: Invalid JSON
```json
{
  "conversation": "I have a headache",
  "max_results": "invalid"
}
```
**Expected**: 400 error or processing error

### Test 3: Empty Conversation
```json
{
  "conversation": ""
}
```
**Expected**: 400 error with "Conversation parameter is required"

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Make sure the Flask server is running
   - Check if the port is correct (default: 5000)

2. **500 Internal Server Error**
   - Check if API keys are configured in `.env`
   - Look at server logs for specific error messages

3. **Timeout Issues**
   - The pipeline can take 10-30 seconds for complex requests
   - Increase Postman timeout settings

4. **JSON Parsing Errors**
   - Ensure proper JSON format
   - Check for extra commas or invalid syntax

### Debug Mode

To enable debug logging, modify `symptom_search_server.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Performance Testing

### Load Testing
1. Use Postman's Collection Runner
2. Set up multiple iterations
3. Monitor response times
4. Check for rate limiting

### Response Time Expectations
- **Simple symptoms**: 5-10 seconds
- **Complex symptoms**: 15-30 seconds
- **Multiple medicines**: 20-40 seconds

## Next Steps

1. **Test locally** with Postman
2. **Deploy to production** (Render, Railway, etc.)
3. **Update URLs** in Postman environment
4. **Test production endpoints**
5. **Integrate with Vapi** using the webhook URL

## Support

If you encounter issues:
1. Check server logs for error messages
2. Verify API keys are configured correctly
3. Test with simpler conversations first
4. Ensure all dependencies are installed
