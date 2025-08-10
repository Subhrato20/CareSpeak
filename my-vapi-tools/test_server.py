#!/usr/bin/env python3
import requests
import json

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:8080/health')
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_process_conversation():
    """Test the process_conversation endpoint"""
    try:
        data = {
            "conversation": "I have a headache and fever",
            "max_results": 3
        }
        response = requests.post(
            'http://localhost:8080/process_conversation',
            headers={'Content-Type': 'application/json'},
            json=data
        )
        print(f"Process conversation status: {response.status_code}")
        print(f"Process conversation response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"Process conversation failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing server endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    health_ok = test_health()
    print()
    
    # Test process conversation endpoint
    print("2. Testing process conversation endpoint...")
    conversation_ok = test_process_conversation()
    print()
    
    if health_ok and conversation_ok:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")



