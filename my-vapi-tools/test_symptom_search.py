#!/usr/bin/env python3
"""
Test script for the symptom search tool.
This script tests the symptom search functionality without requiring a full server setup.
"""

import os
import json
from dotenv import load_dotenv
from symptom_search_tool import search_products_for_symptoms

# Load environment variables
load_dotenv()

def test_symptom_search():
    """Test the symptom search tool with various symptoms."""
    
    # Check if SearchAPI key is configured
    if not os.getenv('SEARCHAPI_API_KEY'):
        print("❌ SEARCHAPI_API_KEY not found in environment variables")
        print("Please add SEARCHAPI_API_KEY to your .env file")
        return False
    
    # Test cases
    test_cases = [
        {
            "symptoms": "headache and fever",
            "description": "Common cold symptoms"
        },
        {
            "symptoms": "back pain",
            "description": "Pain management"
        },
        {
            "symptoms": "sore throat and cough",
            "description": "Cold symptoms"
        },
        {
            "symptoms": "trouble sleeping",
            "description": "Sleep issues"
        },
        {
            "symptoms": "upset stomach",
            "description": "Digestive issues"
        }
    ]
    
    print("🧪 Testing Symptom Search Tool")
    print("=" * 50)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{total_count}: {test_case['description']}")
        print(f"Symptoms: '{test_case['symptoms']}'")
        
        try:
            # Call the symptom search tool
            results = search_products_for_symptoms(test_case['symptoms'], max_results=3)
            
            if results["status"] == "success":
                print(f"✅ Search successful")
                print(f"   Search query: {results['search_query']}")
                print(f"   Results found: {len(results['results'])}")
                
                if results['results']:
                    print("   Top result:")
                    top_result = results['results'][0]
                    print(f"   - {top_result['title']}")
                    print(f"   - Price: {top_result['price']}")
                    print(f"   - Rating: {top_result['rating']}/5 ({top_result['reviews']} reviews)")
                
                success_count += 1
            else:
                print(f"❌ Search failed: {results.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! The symptom search tool is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def test_voice_response():
    """Test the voice response formatting."""
    print("\n🎤 Testing Voice Response Formatting")
    print("=" * 40)
    
    # Mock results for testing voice response
    mock_results = {
        "status": "success",
        "symptoms": "headache and fever",
        "results": [
            {
                "title": "Tylenol Extra Strength Acetaminophen 500mg",
                "brand": "Tylenol",
                "price": "$8.99",
                "rating": 4.7,
                "reviews": 15420
            },
            {
                "title": "Advil Ibuprofen Tablets 200mg",
                "brand": "Advil",
                "price": "$6.99",
                "rating": 4.5,
                "reviews": 8920
            }
        ]
    }
    
    from symptom_search_tool import format_results_for_voice
    voice_response = format_results_for_voice(mock_results)
    
    print("Voice response:")
    print(f"'{voice_response}'")
    
    # Check if response contains key elements
    checks = [
        ("symptoms mentioned", "headache and fever" in voice_response.lower()),
        ("product recommendations", "recommendations" in voice_response.lower()),
        ("healthcare advice", "healthcare professional" in voice_response.lower()),
        ("rating information", "star rating" in voice_response.lower())
    ]
    
    print("\nVoice response checks:")
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
    
    return all(passed for _, passed in checks)

if __name__ == "__main__":
    print("🚀 Starting Symptom Search Tool Tests")
    print("=" * 60)
    
    # Test the core functionality
    core_success = test_symptom_search()
    
    # Test voice response formatting
    voice_success = test_voice_response()
    
    print("\n" + "=" * 60)
    if core_success and voice_success:
        print("🎉 All tests completed successfully!")
        print("\n✅ The symptom search tool is ready to use with Vapi!")
        print("\nNext steps:")
        print("1. Deploy the symptom_search_server.py to a cloud platform")
        print("2. Create the tool in Vapi dashboard")
        print("3. Add the tool to your assistant")
        print("4. Test with real voice conversations")
    else:
        print("❌ Some tests failed. Please fix the issues before proceeding.")
    
    print("\nFor more information, see SYMPTOM_SEARCH_README.md")
