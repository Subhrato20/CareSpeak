from flask import Flask, request, jsonify
from symptom_search_tool import search_products_for_symptoms
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
    return jsonify({"status": "healthy", "service": "symptom-search-tool"})

@app.route('/search_symptoms', methods=['POST'])
def search_symptoms():
    """
    Endpoint for Vapi to call when user reports symptoms.
    Expected JSON payload:
    {
        "symptoms": "headache and fever",
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
        
        # Extract symptoms from request
        symptoms = data.get('symptoms')
        if not symptoms:
            return jsonify({
                "status": "error",
                "message": "Symptoms parameter is required"
            }), 400
        
        # Get max_results (optional, default 5)
        max_results = data.get('max_results', 5)
        
        logger.info(f"Searching for products based on symptoms: {symptoms}")
        
        # Call the symptom search tool
        results = search_products_for_symptoms(symptoms, max_results)
        
        logger.info(f"Search completed. Found {len(results.get('results', []))} results")
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error processing symptom search request: {str(e)}")
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
        
        if function_name == 'search_products_for_symptoms':
            symptoms = arguments.get('symptoms')
            max_results = arguments.get('max_results', 5)
            
            if not symptoms:
                return jsonify({
                    "status": "error",
                    "message": "Symptoms parameter is required"
                }), 400
            
            logger.info(f"Processing function call: {function_name} with symptoms: {symptoms}")
            
            # Call the symptom search tool
            results = search_products_for_symptoms(symptoms, max_results)
            
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
        "service": "Symptom Search Tool",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "search_symptoms": "/search_symptoms",
            "webhook": "/webhook"
        },
        "description": "A tool that searches for Amazon products based on user symptoms using the Amazon Search API."
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Check if SearchAPI key is configured
    if not os.getenv('SEARCHAPI_API_KEY'):
        logger.error("SEARCHAPI_API_KEY not found in environment variables")
        logger.error("Please add SEARCHAPI_API_KEY to your .env file")
        exit(1)
    
    logger.info(f"Starting Symptom Search Tool server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
