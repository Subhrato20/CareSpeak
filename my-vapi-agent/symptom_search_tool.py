import os
import json
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SymptomSearchTool:
    """
    A tool that searches for products on Amazon based on user symptoms.
    Uses the Amazon Search API to find relevant health and wellness products.
    """
    
    def __init__(self):
        self.api_key = os.getenv('SEARCHAPI_API_KEY')
        self.base_url = "https://www.searchapi.io/api/v1/search"
        
        if not self.api_key:
            raise ValueError("SEARCHAPI_API_KEY not found in environment variables")
    
    def search_products_by_symptoms(self, symptoms: str, max_results: int = 5) -> Dict:
        """
        Search for products on Amazon based on user symptoms.
        
        Args:
            symptoms (str): User's symptoms or health concerns
            max_results (int): Maximum number of results to return (default: 5)
            
        Returns:
            Dict: Search results with product information
        """
        try:
            # Construct search query based on symptoms
            search_query = self._build_search_query(symptoms)
            
            # Prepare API request parameters
            params = {
                "engine": "amazon_search",
                "q": search_query,
                "api_key": self.api_key,
                "amazon_domain": "amazon.com",
                "sort_by": "featured"  # Default sort order
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Process and filter results
            processed_results = self._process_results(data, symptoms)
            
            # Limit results
            if len(processed_results) > max_results:
                processed_results = processed_results[:max_results]
            
            return {
                "status": "success",
                "symptoms": symptoms,
                "search_query": search_query,
                "results": processed_results,
                "total_results": len(processed_results)
            }
            
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"API request failed: {str(e)}",
                "symptoms": symptoms
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Search failed: {str(e)}",
                "symptoms": symptoms
            }
    
    def _build_search_query(self, symptoms: str) -> str:
        """
        Build an optimized search query based on symptoms.
        
        Args:
            symptoms (str): User's symptoms
            
        Returns:
            str: Optimized search query
        """
        # Common symptom to product mappings
        symptom_mappings = {
            # Pain-related symptoms
            "headache": "headache relief medicine",
            "migraine": "migraine relief medicine",
            "back pain": "back pain relief",
            "joint pain": "joint pain relief",
            "muscle pain": "muscle pain relief",
            "toothache": "toothache relief",
            
            # Cold and flu symptoms
            "fever": "fever reducer medicine",
            "cough": "cough medicine",
            "sore throat": "sore throat relief",
            "congestion": "nasal congestion relief",
            "runny nose": "runny nose relief",
            
            # Digestive symptoms
            "nausea": "nausea relief",
            "upset stomach": "upset stomach relief",
            "indigestion": "indigestion relief",
            "heartburn": "heartburn relief",
            
            # Skin-related symptoms
            "rash": "rash treatment",
            "itching": "itching relief",
            "dry skin": "dry skin treatment",
            "acne": "acne treatment",
            
            # Sleep-related symptoms
            "insomnia": "sleep aid",
            "trouble sleeping": "sleep aid",
            
            # Allergy symptoms
            "allergies": "allergy medicine",
            "seasonal allergies": "seasonal allergy medicine",
            
            # General wellness
            "stress": "stress relief",
            "anxiety": "anxiety relief",
            "vitamins": "vitamins",
            "supplements": "health supplements"
        }
        
        # Convert symptoms to lowercase for matching
        symptoms_lower = symptoms.lower()
        
        # Check for exact matches in symptom mappings
        for symptom, product_query in symptom_mappings.items():
            if symptom in symptoms_lower:
                return product_query
        
        # If no exact match, create a general health product search
        # Remove common words that don't help with search
        common_words = ["i", "have", "am", "feeling", "experiencing", "suffering", "from", "with", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]
        
        words = symptoms_lower.split()
        filtered_words = [word for word in words if word not in common_words and len(word) > 2]
        
        if filtered_words:
            # Combine meaningful words with "relief" or "medicine"
            base_query = " ".join(filtered_words[:3])  # Limit to first 3 words
            return f"{base_query} relief medicine"
        else:
            # Fallback to general health products
            return "health wellness products"
    
    def _process_results(self, data: Dict, symptoms: str) -> List[Dict]:
        """
        Process and filter search results to make them more relevant.
        
        Args:
            data (Dict): Raw API response data
            symptoms (str): Original symptoms for context
            
        Returns:
            List[Dict]: Processed and filtered results
        """
        processed_results = []
        
        if "organic_results" not in data:
            return processed_results
        
        for result in data["organic_results"]:
            # Skip results that are not relevant (e.g., books, videos)
            if self._is_relevant_result(result, symptoms):
                processed_result = {
                    "title": result.get("title", ""),
                    "brand": result.get("brand", ""),
                    "price": result.get("price", "Price not available"),
                    "rating": result.get("rating", 0),
                    "reviews": result.get("reviews", 0),
                    "link": result.get("link", ""),
                    "thumbnail": result.get("thumbnail", ""),
                    "is_prime": result.get("is_prime", False),
                    "description": self._extract_description(result)
                }
                
                # Only include results with ratings and reviews
                if processed_result["rating"] > 0 and processed_result["reviews"] > 0:
                    processed_results.append(processed_result)
        
        # Sort by rating (highest first)
        processed_results.sort(key=lambda x: x["rating"], reverse=True)
        
        return processed_results
    
    def _is_relevant_result(self, result: Dict, symptoms: str) -> bool:
        """
        Check if a search result is relevant to the symptoms.
        
        Args:
            result (Dict): Search result
            symptoms (str): User symptoms
            
        Returns:
            bool: True if relevant, False otherwise
        """
        title = result.get("title", "").lower()
        symptoms_lower = symptoms.lower()
        
        # Skip books, videos, and other non-product items
        irrelevant_keywords = ["book", "dvd", "video", "movie", "kindle", "audio", "cd"]
        for keyword in irrelevant_keywords:
            if keyword in title:
                return False
        
        # Check if any symptom-related words appear in the title
        symptom_words = symptoms_lower.split()
        for word in symptom_words:
            if len(word) > 3 and word in title:  # Only check words longer than 3 characters
                return True
        
        return True  # Default to True if no clear indicators
    
    def _extract_description(self, result: Dict) -> str:
        """
        Extract a meaningful description from the search result.
        
        Args:
            result (Dict): Search result
            
        Returns:
            str: Extracted description
        """
        description = result.get("title", "")
        
        # Add rating information if available
        rating = result.get("rating", 0)
        reviews = result.get("reviews", 0)
        
        if rating > 0 and reviews > 0:
            description += f" (Rated {rating} out of 5 stars with {reviews} reviews)"
        
        # Add Prime information if available
        if result.get("is_prime", False):
            description += " - Prime eligible"
        
        return description

# Function to be called by Vapi
def search_products_for_symptoms(symptoms: str, max_results: int = 5) -> Dict:
    """
    Main function to be called by Vapi when user reports symptoms.
    
    Args:
        symptoms (str): User's symptoms or health concerns
        max_results (int): Maximum number of results to return
        
    Returns:
        Dict: Search results with product recommendations
    """
    try:
        tool = SymptomSearchTool()
        results = tool.search_products_by_symptoms(symptoms, max_results)
        
        if results["status"] == "success":
            # Format results for voice response
            formatted_results = format_results_for_voice(results)
            results["voice_response"] = formatted_results
        
        return results
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search for products: {str(e)}",
            "symptoms": symptoms
        }

def format_results_for_voice(results: Dict) -> str:
    """
    Format search results into a natural language response for voice.
    
    Args:
        results (Dict): Search results
        
    Returns:
        str: Formatted voice response
    """
    if results["status"] != "success" or not results["results"]:
        return f"I couldn't find any products specifically for {results['symptoms']}. You might want to consult with a healthcare professional for medical advice."
    
    response_parts = [f"Based on your symptoms of {results['symptoms']}, I found {len(results['results'])} product recommendations:"]
    
    for i, product in enumerate(results["results"], 1):
        rating_text = f" with a {product['rating']} star rating from {product['reviews']} reviews" if product['rating'] > 0 else ""
        price_text = f" for {product['price']}" if product['price'] != "Price not available" else ""
        
        response_parts.append(
            f"{i}. {product['title']}{rating_text}{price_text}."
        )
    
    response_parts.append("These are general recommendations. Please consult with a healthcare professional for medical advice, especially if symptoms persist or worsen.")
    
    return " ".join(response_parts)

if __name__ == "__main__":
    # Test the tool
    test_symptoms = "headache and fever"
    results = search_products_for_symptoms(test_symptoms)
    print(json.dumps(results, indent=2))
