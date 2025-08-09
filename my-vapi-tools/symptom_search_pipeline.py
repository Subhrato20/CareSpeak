import os
import json
import requests
import httpx
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI

# Create a clean session without proxies to avoid issues
session = requests.Session()
session.proxies = {}

# Load environment variables
load_dotenv()

class SymptomSearchPipeline:
    """
    Multi-layer GPT pipeline for symptom search and medicine recommendations.
    
    Flow:
    1. User conversation → GPT extracts symptoms
    2. Symptoms → GPT recommends specific medicines
    3. Medicine names → SearchAPI finds products on Amazon
    4. SearchAPI JSON → GPT extracts details and formats natural language response
    """
    
    def __init__(self):
        self.searchapi_key = os.getenv('SEARCHAPI_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.base_search_url = "https://www.searchapi.io/api/v1/search"
        
        if not self.searchapi_key:
            raise ValueError("SEARCHAPI_API_KEY not found in environment variables")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client with a custom HTTPX client that ignores env proxies
        try:
            http_client = httpx.Client(trust_env=False)
            self.client = OpenAI(api_key=self.openai_api_key, http_client=http_client)
        except TypeError as e:
            if "proxies" in str(e):
                # Fallback: clear proxies from env and try again
                proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']
                for var in proxy_vars:
                    if var in os.environ:
                        del os.environ[var]
                http_client = httpx.Client(trust_env=False)
                self.client = OpenAI(api_key=self.openai_api_key, http_client=http_client)
            else:
                raise e
    
    def extract_symptoms_from_conversation(self, conversation: str) -> Dict:
        """
        Layer 1: Extract symptoms from user conversation using GPT.
        
        Args:
            conversation (str): User's conversation or description of their condition
            
        Returns:
            Dict: Extracted symptoms and context
        """
        try:
            system_prompt = """
            You are a medical symptom extraction expert. Your job is to extract relevant symptoms and health concerns from user conversations.
            
            IMPORTANT GUIDELINES:
            - Focus only on symptoms and health-related information
            - Ignore casual conversation, greetings, or unrelated topics
            - Extract specific symptoms (e.g., "headache", "fever", "sore throat")
            - Include severity if mentioned (e.g., "severe headache", "mild fever")
            - Include duration if mentioned (e.g., "headache for 3 days")
            - Be precise and avoid vague terms
            
            Return your response as a JSON object with these fields:
            - symptoms: list of extracted symptoms
            - severity: overall severity (mild, moderate, severe)
            - duration: if mentioned, otherwise null
            - context: any additional relevant context
            
            Example response:
            {
                "symptoms": ["headache", "fever", "fatigue"],
                "severity": "moderate",
                "duration": "2 days",
                "context": "User has been experiencing these symptoms for the past 2 days"
            }
            
            IMPORTANT: Return ONLY valid JSON, no additional text or explanations.
            """
            
            response = self._chat_completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation}
                ],
                temperature=1.0,
                max_tokens=300
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content.strip()
            
            # Clean up the content - remove markdown code blocks if present
            if content.startswith('```json'):
                content = content[7:-3]  # Remove ```json and ``` markers
            elif content.startswith('```'):
                content = content[3:-3]  # Remove ``` markers
            
            # Remove any leading/trailing whitespace
            content = content.strip()
            
            # Try to parse the JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError as e:
                # If JSON parsing fails, try to extract symptoms manually
                print(f"JSON parsing failed: {e}. Content: {content}")
                
                # Fallback: try to extract symptoms using a simpler approach
                fallback_symptoms = self._extract_symptoms_fallback(conversation)
                result = {
                    "symptoms": fallback_symptoms,
                    "severity": "moderate",
                    "duration": None,
                    "context": "Extracted using fallback method"
                }
            
            # Ensure the result has the required fields
            if not isinstance(result, dict):
                result = {}
            
            # Ensure symptoms is always a list
            if 'symptoms' not in result or not isinstance(result['symptoms'], list):
                result['symptoms'] = []
            
            # Ensure other fields exist
            result.setdefault('severity', 'unknown')
            result.setdefault('duration', None)
            result.setdefault('context', None)
            
            return result
            
        except Exception as e:
            print(f"Error in extract_symptoms_from_conversation: {str(e)}")
            # Fallback: try to extract symptoms manually
            fallback_symptoms = self._extract_symptoms_fallback(conversation)
            return {
                "symptoms": fallback_symptoms,
                "severity": "unknown",
                "duration": None,
                "context": f"Error extracting symptoms: {str(e)}"
            }
    
    def _extract_symptoms_fallback(self, conversation: str) -> List[str]:
        """
        Fallback method to extract symptoms when GPT parsing fails.
        
        Args:
            conversation (str): User's conversation
            
        Returns:
            List[str]: List of extracted symptoms
        """
        conversation_lower = conversation.lower()
        symptoms = []
        
        # Common symptom keywords
        symptom_keywords = {
            'headache': ['headache', 'head pain', 'migraine'],
            'fever': ['fever', 'temperature', 'hot'],
            'sore throat': ['sore throat', 'throat pain', 'throat sore'],
            'cough': ['cough', 'coughing', 'dry cough'],
            'fatigue': ['fatigue', 'tired', 'exhausted', 'weak'],
            'body aches': ['body aches', 'muscle pain', 'joint pain', 'achy'],
            'nausea': ['nausea', 'sick', 'queasy'],
            'congestion': ['congestion', 'stuffy nose', 'blocked nose'],
            'runny nose': ['runny nose', 'dripping nose'],
            'sneezing': ['sneezing', 'sneeze'],
            'itchy eyes': ['itchy eyes', 'eye irritation'],
            'back pain': ['back pain', 'backache'],
            'stomach pain': ['stomach pain', 'abdominal pain', 'belly ache'],
            'insomnia': ['insomnia', 'trouble sleeping', 'can\'t sleep'],
            'anxiety': ['anxiety', 'anxious', 'worried'],
            'stress': ['stress', 'stressed'],
            'allergies': ['allergies', 'allergic']
        }
        
        # Check for each symptom
        for symptom, keywords in symptom_keywords.items():
            for keyword in keywords:
                if keyword in conversation_lower:
                    if symptom not in symptoms:
                        symptoms.append(symptom)
                    break
        
        return symptoms
    
    def recommend_medicines_from_symptoms(self, symptoms_data: Dict) -> List[str]:
        """
        Layer 2: Convert symptoms to specific medicine names using GPT.
        
        Args:
            symptoms_data (Dict): Output from extract_symptoms_from_conversation
            
        Returns:
            List[str]: List of recommended medicine names
        """
        try:
            symptoms = symptoms_data.get('symptoms', [])
            if not symptoms:
                return []
            
            system_prompt = """
            You are a medical expert who recommends over-the-counter medicines based on symptoms.
            
            IMPORTANT GUIDELINES:
            - Recommend only common, over-the-counter medicines
            - Focus on FDA-approved medications
            - Be specific with medicine names and types
            - Consider generic names when appropriate
            - Avoid prescription medications
            - Include common brand names when helpful
            
            Examples:
            - headache → ["acetaminophen", "ibuprofen", "aspirin"]
            - fever → ["acetaminophen", "ibuprofen"]
            - sore throat → ["throat lozenges", "acetaminophen", "ibuprofen"]
            - cough → ["dextromethorphan", "guaifenesin", "cough syrup"]
            - allergies → ["cetirizine", "loratadine", "diphenhydramine"]
            
            Return only a JSON array of medicine names (strings), no explanations.
            Example: ["acetaminophen", "ibuprofen", "throat lozenges"]
            
            IMPORTANT: Return ONLY valid JSON array, no additional text or explanations.
            """
            
            user_prompt = f"Symptoms: {', '.join(symptoms)}\nSeverity: {symptoms_data.get('severity', 'unknown')}\nDuration: {symptoms_data.get('duration', 'unknown')}"
            
            response = self._chat_completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.0,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up the content - remove markdown code blocks if present
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            # Remove any leading/trailing whitespace
            content = content.strip()
            
            try:
                medicines = json.loads(content)
                if isinstance(medicines, list):
                    return medicines
                else:
                    print(f"Invalid medicine format: {medicines}")
                    return self._recommend_medicines_fallback(symptoms)
            except json.JSONDecodeError as e:
                print(f"Medicine JSON parsing failed: {e}. Content: {content}")
                return self._recommend_medicines_fallback(symptoms)
            
        except Exception as e:
            print(f"Error in recommend_medicines_from_symptoms: {str(e)}")
            return self._recommend_medicines_fallback(symptoms)
    
    def _recommend_medicines_fallback(self, symptoms: List[str]) -> List[str]:
        """
        Fallback method to recommend medicines when GPT parsing fails.
        
        Args:
            symptoms (List[str]): List of symptoms
            
        Returns:
            List[str]: List of recommended medicines
        """
        medicine_mappings = {
            'headache': ['acetaminophen', 'ibuprofen', 'aspirin'],
            'fever': ['acetaminophen', 'ibuprofen'],
            'sore throat': ['throat lozenges', 'acetaminophen', 'ibuprofen'],
            'cough': ['dextromethorphan', 'guaifenesin', 'cough syrup'],
            'fatigue': ['caffeine', 'vitamin b12'],
            'body aches': ['ibuprofen', 'acetaminophen'],
            'nausea': ['pepto-bismol', 'ginger'],
            'congestion': ['pseudoephedrine', 'saline nasal spray'],
            'runny nose': ['antihistamines', 'saline nasal spray'],
            'sneezing': ['antihistamines', 'cetirizine'],
            'itchy eyes': ['antihistamine eye drops', 'cetirizine'],
            'back pain': ['ibuprofen', 'acetaminophen', 'topical analgesics'],
            'stomach pain': ['pepto-bismol', 'antacids'],
            'insomnia': ['diphenhydramine', 'melatonin'],
            'anxiety': ['valerian root', 'chamomile'],
            'stress': ['b vitamins', 'magnesium'],
            'allergies': ['cetirizine', 'loratadine', 'diphenhydramine']
        }
        
        recommended_medicines = []
        for symptom in symptoms:
            if symptom in medicine_mappings:
                recommended_medicines.extend(medicine_mappings[symptom])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_medicines = []
        for medicine in recommended_medicines:
            if medicine not in seen:
                seen.add(medicine)
                unique_medicines.append(medicine)
        
        return unique_medicines
    
    def search_medicines_on_amazon(self, medicine_names: List[str], max_results: int = 5) -> Dict:
        """
        Layer 3: Search for medicines on Amazon using SearchAPI.
        
        Args:
            medicine_names (List[str]): List of medicine names to search for
            max_results (int): Maximum number of results per medicine
            
        Returns:
            Dict: Search results for all medicines
        """
        try:
            all_results = []
            
            for medicine in medicine_names:
                # Prepare search parameters
                params = {
                    "engine": "amazon_search",
                    "q": medicine,
                    "api_key": self.searchapi_key,
                    "amazon_domain": "amazon.com",
                    "sort_by": "featured"
                }
                
                # Make API request using clean session
                response = session.get(self.base_search_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                # Process results
                if "organic_results" in data:
                    medicine_results = []
                    for result in data["organic_results"][:max_results]:
                        processed_result = {
                            "title": result.get("title", ""),
                            "brand": result.get("brand", ""),
                            "price": result.get("price", "Price not available"),
                            "rating": result.get("rating", 0),
                            "reviews": result.get("reviews", 0),
                            "link": result.get("link", ""),
                            "thumbnail": result.get("thumbnail", ""),
                            "is_prime": result.get("is_prime", False),
                            "medicine_name": medicine
                        }
                        if processed_result["rating"] > 0 and processed_result["reviews"] > 0:
                            medicine_results.append(processed_result)
                    
                    all_results.extend(medicine_results)
            
            return {
                "status": "success",
                "total_results": len(all_results),
                "results": all_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Search failed: {str(e)}",
                "results": []
            }
    
    def extract_medicine_details_and_format_response(self, search_results: Dict, original_symptoms: Dict) -> str:
        """
        Layer 4: Extract medicine details from SearchAPI JSON and format natural language response.
        
        Args:
            search_results (Dict): Results from search_medicines_on_amazon
            original_symptoms (Dict): Original symptoms data from Layer 1
            
        Returns:
            str: Natural language response formatted for voice
        """
        try:
            if search_results.get("status") != "success" or not search_results.get("results"):
                return f"I couldn't find specific products for your symptoms of {', '.join(original_symptoms.get('symptoms', []))}. Please consult with a healthcare professional for medical advice."
            
            system_prompt = """
            You are a helpful medical assistant who provides natural, conversational responses about medicine recommendations.
            
            Your task is to extract key information from Amazon search results and create a natural language response for voice communication.
            
            GUIDELINES:
            - Be conversational and friendly
            - Mention the symptoms the user reported
            - Include medicine names, prices, and ratings when available
            - Organize by medicine type/category
            - Include safety disclaimers
            - Keep it concise but informative
            - Use natural speech patterns
            - Avoid medical jargon
            - Always recommend consulting a healthcare professional
            
            Format the response as a natural, conversational paragraph suitable for voice communication.
            """
            
            # Prepare context for GPT
            context = {
                "symptoms": original_symptoms.get("symptoms", []),
                "severity": original_symptoms.get("severity", "unknown"),
                "duration": original_symptoms.get("duration"),
                "search_results": search_results.get("results", [])
            }
            
            user_prompt = f"""
            Based on these symptoms: {', '.join(context['symptoms'])} (severity: {context['severity']}, duration: {context['duration'] or 'unknown'})
            
            Here are the Amazon search results:
            {json.dumps(context['search_results'], indent=2)}
            
            Please create a natural, conversational response for voice communication that summarizes the recommended medicines and products.
            """
            
            response = self._chat_completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.0,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I found some products for your symptoms, but I encountered an issue formatting the details. Please consult with a healthcare professional for personalized advice."

    def _chat_completion(self, model: str, messages: List[Dict[str, str]], temperature: float, max_tokens: int):
        """
        Compatibility wrapper for chat.completions.create across SDK/model variants.
        Tries 'max_completion_tokens' first, falls back to 'max_tokens', and vice versa.
        """
        # Try with max_completion_tokens first
        try:
            return self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )
        except Exception as first_error:
            error_text = str(first_error)
            # If max_completion_tokens is unsupported, try max_tokens
            try:
                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except Exception as second_error:
                # Final attempt: omit token parameter entirely
                try:
                    return self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                    )
                except Exception as third_error:
                    # Raise combined error info
                    raise Exception(
                        f"First attempt failed with max_completion_tokens: {error_text}; "
                        f"Second attempt with max_tokens failed: {second_error}; "
                        f"Third attempt without token param failed: {third_error}"
                    )
    
    def process_conversation(self, conversation: str, max_results: int = 5) -> Dict:
        """
        Main pipeline method that processes the entire conversation through all layers.
        
        Args:
            conversation (str): User's conversation or description
            max_results (int): Maximum results per medicine
            
        Returns:
            Dict: Complete pipeline results including natural language response
        """
        try:
            # Layer 1: Extract symptoms
            print("🔍 Layer 1: Extracting symptoms from conversation...")
            symptoms_data = self.extract_symptoms_from_conversation(conversation)
            
            if not symptoms_data.get("symptoms"):
                return {
                    "status": "error",
                    "message": "No symptoms could be extracted from the conversation",
                    "conversation": conversation,
                    "pipeline_steps": ["symptom_extraction"]
                }
            
            # Layer 2: Recommend medicines
            print("💊 Layer 2: Recommending medicines based on symptoms...")
            medicine_names = self.recommend_medicines_from_symptoms(symptoms_data)
            
            if not medicine_names:
                return {
                    "status": "error",
                    "message": "No medicines could be recommended for the symptoms",
                    "conversation": conversation,
                    "symptoms": symptoms_data,
                    "pipeline_steps": ["symptom_extraction", "medicine_recommendation"]
                }
            
            # Layer 3: Search on Amazon
            print("🛒 Layer 3: Searching for medicines on Amazon...")
            search_results = self.search_medicines_on_amazon(medicine_names, max_results)
            
            # Layer 4: Extract details and format response
            print("📝 Layer 4: Extracting details and formatting response...")
            natural_response = self.extract_medicine_details_and_format_response(search_results, symptoms_data)
            
            return {
                "status": "success",
                "conversation": conversation,
                "pipeline_steps": ["symptom_extraction", "medicine_recommendation", "amazon_search", "response_formatting"],
                "symptoms": symptoms_data,
                "recommended_medicines": medicine_names,
                "search_results": search_results,
                "natural_response": natural_response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Pipeline failed: {str(e)}",
                "conversation": conversation,
                "pipeline_steps": []
            }

# Function to be called by Vapi
def process_symptom_conversation(conversation: str, max_results: int = 5) -> Dict:
    """
    Main function to be called by Vapi when user reports symptoms or health concerns.
    
    Args:
        conversation (str): User's conversation or description of their condition
        max_results (int): Maximum number of results per medicine
        
    Returns:
        Dict: Complete pipeline results with natural language response
    """
    try:
        # Clear any proxy-related environment variables that might be causing issues
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']
        for var in proxy_vars:
            if var in os.environ:
                del os.environ[var]

        # Clear any Vapi-related environment variables that might be causing issues
        vapi_vars = ['VAPI_INSTALL', 'VAPI_CONFIG', 'VAPI_ENV']
        for var in vapi_vars:
            if var in os.environ:
                del os.environ[var]
        
        # Clear any requests-related environment variables that might cause issues
        requests_vars = ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE']
        for var in requests_vars:
            if var in os.environ:
                del os.environ[var]
        
        pipeline = SymptomSearchPipeline()
        results = pipeline.process_conversation(conversation, max_results)
        
        # Ensure the natural response is always available
        if results["status"] == "success":
            results["voice_response"] = results.get("natural_response", "I couldn't process your request. Please try again.")
        else:
            results["voice_response"] = f"I'm sorry, but I couldn't process your symptoms. {results.get('message', 'Please consult with a healthcare professional.')}"
        
        return results
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process conversation: {str(e)}",
            "conversation": conversation,
            "voice_response": "I'm sorry, but I encountered an error processing your request. Please try again or consult with a healthcare professional."
        }

if __name__ == "__main__":
    # Test the pipeline
    test_conversation = "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy."
    results = process_symptom_conversation(test_conversation)
    print(json.dumps(results, indent=2))
