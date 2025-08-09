#!/usr/bin/env python3
"""
Quick endpoint testing script for the symptom search pipeline.
This script tests all HTTP endpoints to ensure they're working correctly.
"""

import requests
import json
import time

def test_endpoints(base_url="http://localhost:8080"):
    """Test all endpoints of the symptom search pipeline."""
    
    print(f"🧪 Testing endpoints at {base_url}")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check Endpoint")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    # Test 2: Service Information
    print("\n2. Testing Service Information Endpoint")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service info retrieved: {data.get('service')} v{data.get('version')}")
        else:
            print(f"❌ Service info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Service info error: {str(e)}")
    
    # Test 3: Process Conversation (Simple)
    print("\n3. Testing Process Conversation Endpoint (Simple)")
    try:
        payload = {
            "conversation": "I have a headache",
            "max_results": 2
        }
        response = requests.post(
            f"{base_url}/process_conversation",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Conversation processed successfully")
            print(f"   Status: {data.get('status')}")
            print(f"   Pipeline steps: {data.get('pipeline_steps', [])}")
            if 'symptoms' in data:
                symptoms = data['symptoms'].get('symptoms', [])
                print(f"   Extracted symptoms: {symptoms}")
            if 'recommended_medicines' in data:
                medicines = data['recommended_medicines']
                print(f"   Recommended medicines: {medicines}")
            if 'voice_response' in data:
                voice_response = data['voice_response'][:100] + "..." if len(data['voice_response']) > 100 else data['voice_response']
                print(f"   Voice response preview: {voice_response}")
        else:
            print(f"❌ Conversation processing failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Conversation processing error: {str(e)}")
    
    # Test 4: Process Conversation (Complex)
    print("\n4. Testing Process Conversation Endpoint (Complex)")
    try:
        payload = {
            "conversation": "I've been having a really bad headache and fever for the past 2 days. I also feel really tired and achy.",
            "max_results": 3
        }
        response = requests.post(
            f"{base_url}/process_conversation",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Complex conversation processed successfully")
            print(f"   Status: {data.get('status')}")
            if 'symptoms' in data:
                symptoms = data['symptoms'].get('symptoms', [])
                print(f"   Extracted symptoms: {symptoms}")
            if 'search_results' in data:
                search_results = data['search_results']
                total_results = search_results.get('total_results', 0)
                print(f"   Search results: {total_results} products found")
        else:
            print(f"❌ Complex conversation processing failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Complex conversation processing error: {str(e)}")
    
    # Test 5: Webhook Endpoint
    print("\n5. Testing Webhook Endpoint")
    try:
        payload = {
            "functionCall": {
                "name": "process_symptom_conversation",
                "arguments": {
                    "conversation": "I have a sore throat and cough",
                    "max_results": 2
                }
            }
        }
        response = requests.post(
            f"{base_url}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook endpoint working")
            print(f"   Status: {data.get('status')}")
            if 'pipeline_steps' in data:
                steps = data['pipeline_steps']
                print(f"   Pipeline steps completed: {steps}")
        else:
            print(f"❌ Webhook endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook endpoint error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Endpoint testing completed!")
    print("\n📝 Next steps:")
    print("1. If all tests passed ✅, you can now use Postman")
    print("2. If some tests failed ❌, check the server logs")
    print("3. Make sure your .env file is configured correctly")
    print("4. Ensure the server is running: python symptom_search_server.py")

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            test_endpoints()
        else:
            print("❌ Server not running or not responding")
            print("Please start the server first:")
            print("cd my-vapi-tools")
            print("python symptom_search_server.py")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8080")
        print("Please start the server first:")
        print("cd my-vapi-tools")
        print("python symptom_search_server.py")
    except Exception as e:
        print(f"❌ Error testing endpoints: {str(e)}")
