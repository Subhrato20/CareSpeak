#!/usr/bin/env python3
"""
Test script for the symptom search tool with the proxies fix.
This script tests the symptom search functionality to ensure it works correctly.
"""

import os
import json
from dotenv import load_dotenv
from symptom_search_tool import search_products_for_symptoms, SymptomSearchTool

# Load environment variables
load_dotenv()

def test_symptom_search_tool():
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
        }
    ]
    
    print("🧪 Testing Symptom Search Tool (Fixed)")
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
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! The symptom search tool is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def test_symptom_search_tool_initialization():
    """Test the SymptomSearchTool initialization."""
    print("\n🔧 Testing SymptomSearchTool Initialization")
    print("=" * 40)
    
    try:
        # Test initialization
        tool = SymptomSearchTool()
        print("✅ SymptomSearchTool initialized successfully!")
        
        # Test session configuration
        print(f"✅ Session proxies: {tool.session.proxies}")
        print(f"✅ Session trust_env: {tool.session.trust_env}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize SymptomSearchTool: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Symptom Search Tool (Fixed)")
    print("=" * 50)
    
    # Test initialization
    init_success = test_symptom_search_tool_initialization()
    
    if init_success:
        # Test functionality
        func_success = test_symptom_search_tool()
        
        if func_success:
            print("\n🎉 All tests passed! The symptom search tool is working correctly with the proxies fix.")
        else:
            print("\n⚠️  Some functionality tests failed. Please check the errors above.")
    else:
        print("\n❌ Initialization tests failed. Please check the errors above.")




