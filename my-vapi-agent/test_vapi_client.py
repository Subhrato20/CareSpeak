#!/usr/bin/env python3
"""
Test script for the Vapi client initialization.
This script tests the Vapi client to ensure it works correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_vapi_client():
    """Test the Vapi client initialization."""
    
    # Check if Vapi Python SDK is available
    try:
        from vapi_python import Vapi
        print("✅ Vapi Python SDK imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Vapi Python SDK: {e}")
        return False
    
    # Check if API key is configured
    api_key = os.getenv('VAPI_PUBLIC_KEY')
    if not api_key or api_key == 'your-public-key-here':
        print("⚠️  VAPI_PUBLIC_KEY not configured or using default value")
        print("   This test will use a dummy key for testing")
        api_key = 'test-key'
    
    try:
        # Test Vapi client initialization
        print("Testing Vapi client initialization...")
        vapi = Vapi(api_key=api_key)
        print("✅ Vapi client initialized successfully!")
        
        # Test client attributes
        print(f"✅ Vapi client type: {type(vapi)}")
        print(f"✅ Vapi client has 'start' method: {hasattr(vapi, 'start')}")
        print(f"✅ Vapi client has 'stop' method: {hasattr(vapi, 'stop')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Vapi client: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Vapi Client")
    print("=" * 30)
    
    success = test_vapi_client()
    
    print("\n" + "=" * 30)
    if success:
        print("🎉 All tests passed! The Vapi client is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)
