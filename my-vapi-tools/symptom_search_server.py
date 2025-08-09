from flask import Flask, request, jsonify
from symptom_search_pipeline import process_symptom_conversation
import os
from dotenv import load_dotenv
import logging



# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Vapi."""
    return jsonify({"status": "healthy", "service": "symptom-search-pipeline"})

@app.route('/process_conversation', methods=['POST'])
def process_conversation():
    """
    Endpoint for Vapi to call when user reports symptoms or health concerns.
    Expected JSON payload:
    {
        "conversation": "I've been having headaches and fever for the past 2 days",
        "max_results": 5
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        # Extract conversation from request
        conversation = data.get('conversation')
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation parameter is required"
            }), 400
        
        # Get max_results (optional, default 5)
        max_results = data.get('max_results', 5)
        
        logger.info(f"Processing conversation: {conversation[:100]}...")
        
        # Call the symptom search pipeline
        results = process_symptom_conversation(conversation, max_results)
        
        logger.info(f"Pipeline completed. Status: {results.get('status')}")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error processing conversation: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint for Vapi to call with function requests.
    This endpoint handles the Vapi function calling format.
    """
    try:
        data = request.get_json()
        logger.info(f"Received webhook request: {data}")
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        # Check if this is a function call from Vapi
        function_call = data.get('functionCall')
        if not function_call:
            return jsonify({
                "status": "error",
                "message": "No function call found in request"
            }), 400
        
        function_name = function_call.get('name')
        arguments = function_call.get('arguments', {})
        
        if function_name == 'process_symptom_conversation':
            conversation = arguments.get('conversation')
            max_results = arguments.get('max_results', 5)
            
            if not conversation:
                return jsonify({
                    "status": "error",
                    "message": "Conversation parameter is required"
                }), 400
            
            logger.info(f"Processing function call: {function_name} with conversation: {conversation[:100]}...")
            
            # Call the symptom search pipeline
            results = process_symptom_conversation(conversation, max_results)
            
            return jsonify(results)
        else:
            return jsonify({
                "status": "error",
                "message": f"Unknown function: {function_name}"
            }), 400
            
    except Exception as e:
        logger.error(f"Error processing webhook request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with service information."""
    return jsonify({
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
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # Check if required API keys are configured
    if not os.getenv('SEARCHAPI_API_KEY'):
        logger.error("SEARCHAPI_API_KEY not found in environment variables")
        logger.error("Please add SEARCHAPI_API_KEY to your .env file")
        exit(1)
    
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY not found in environment variables")
        logger.error("Please add OPENAI_API_KEY to your .env file")
        exit(1)
    
    logger.info(f"Starting Symptom Search Pipeline server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
