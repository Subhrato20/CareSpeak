#!/usr/bin/env python3
"""
Test script for the multi-layer GPT symptom search pipeline.
This script tests the complete pipeline functionality.
"""

import os
import json
from dotenv import load_dotenv
from symptom_search_pipeline import process_symptom_conversation

# Load environment variables
load_dotenv()

def test_pipeline():
    """Test the complete symptom search pipeline."""
    
    # Check if required API keys are configured
    if not os.getenv('SEARCHAPI_API_KEY'):
        print("❌ SEARCHAPI_API_KEY not found in environment variables")
        print("Please add SEARCHAPI_API_KEY to your .env file")
        return False
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please add OPENAI_API_KEY to your .env file")
        return False
    
    # Test cases
    test_cases = [
        {
            "conversation": "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy.",
            "description": "Common cold symptoms with headache and fever"
        },
        {
            "conversation": "My throat is really sore and I have a cough that won't go away. It's been bothering me for about a week now.",
            "description": "Sore throat and persistent cough"
        },
        {
            "conversation": "I'm having trouble sleeping lately. I keep waking up in the middle of the night and can't fall back asleep.",
            "description": "Sleep issues"
        },
        {
            "conversation": "I've been feeling really stressed and anxious lately. My stomach is also upset.",
            "description": "Stress and digestive issues"
        },
        {
            "conversation": "I have really bad allergies. My nose is constantly running and my eyes are itchy.",
            "description": "Seasonal allergies"
        }
    ]
    
    print("🧪 Testing Multi-Layer GPT Symptom Search Pipeline")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{total_count}: {test_case['description']}")
        print(f"Conversation: '{test_case['conversation']}'")
        
        try:
            # Call the pipeline
            results = process_symptom_conversation(test_case['conversation'], max_results=3)
            
            if results["status"] == "success":
                print(f"✅ Pipeline successful")
                print(f"   Pipeline steps: {results.get('pipeline_steps', [])}")
                
                if 'symptoms' in results:
                    symptoms = results['symptoms']
                    print(f"   Extracted symptoms: {symptoms.get('symptoms', [])}")
                    print(f"   Severity: {symptoms.get('severity', 'unknown')}")
                    print(f"   Duration: {symptoms.get('duration', 'unknown')}")
                
                if 'recommended_medicines' in results:
                    medicines = results['recommended_medicines']
                    print(f"   Recommended medicines: {medicines}")
                
                if 'search_results' in results:
                    search_results = results['search_results']
                    print(f"   Amazon search results: {len(search_results.get('results', []))} products found")
                
                if 'natural_response' in results:
                    print(f"   Natural response preview: {results['natural_response'][:150]}...")
                
                success_count += 1
            else:
                print(f"❌ Pipeline failed: {results.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! The multi-layer GPT pipeline is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def test_individual_layers():
    """Test individual layers of the pipeline."""
    print("\n🔬 Testing Individual Pipeline Layers")
    print("=" * 40)
    
    from symptom_search_pipeline import SymptomSearchPipeline
    
    try:
        pipeline = SymptomSearchPipeline()
        
        # Test Layer 1: Symptom Extraction
        print("\n🔍 Testing Layer 1: Symptom Extraction")
        conversation = "I've been having headaches and fever for the past 2 days"
        symptoms = pipeline.extract_symptoms_from_conversation(conversation)
        print(f"   Extracted symptoms: {symptoms}")
        
        # Test Layer 2: Medicine Recommendation
        print("\n💊 Testing Layer 2: Medicine Recommendation")
        medicines = pipeline.recommend_medicines_from_symptoms(symptoms)
        print(f"   Recommended medicines: {medicines}")
        
        # Test Layer 3: Amazon Search (if medicines found)
        if medicines:
            print("\n🛒 Testing Layer 3: Amazon Search")
            search_results = pipeline.search_medicines_on_amazon(medicines[:2], max_results=2)
            print(f"   Search results: {len(search_results.get('results', []))} products found")
            
            # Test Layer 4: Response Formatting
            if search_results.get('results'):
                print("\n📝 Testing Layer 4: Response Formatting")
                natural_response = pipeline.extract_medicine_details_and_format_response(search_results, symptoms)
                print(f"   Natural response preview: {natural_response[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Layer testing failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Multi-Layer GPT Pipeline Tests")
    print("=" * 80)
    
    # Test individual layers first
    layer_success = test_individual_layers()
    
    # Test complete pipeline
    pipeline_success = test_pipeline()
    
    print("\n" + "=" * 80)
    if layer_success and pipeline_success:
        print("🎉 All tests completed successfully!")
        print("\n✅ The multi-layer GPT pipeline is ready to use with Vapi!")
        print("\nPipeline Flow:")
        print("1. User conversation → GPT extracts symptoms")
        print("2. Symptoms → GPT recommends specific medicines")
        print("3. Medicine names → SearchAPI finds products on Amazon")
        print("4. SearchAPI JSON → GPT extracts details and formats natural language response")
        print("\nNext steps:")
        print("1. Deploy the symptom_search_server.py to a cloud platform")
        print("2. Create the tool in Vapi dashboard")
        print("3. Add the tool to your assistant")
        print("4. Test with real voice conversations")
    else:
        print("❌ Some tests failed. Please fix the issues before proceeding.")
    
    print("\nFor more information, see SETUP_SUMMARY.md")
