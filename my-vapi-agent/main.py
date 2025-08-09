import time
import os
from dotenv import load_dotenv
from vapi_python import Vapi

# Load environment variables from .env file
load_dotenv()

# Get API key and assistant ID from environment variables
VAPI_PUBLIC_KEY = os.getenv('VAPI_PUBLIC_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

def create_vapi_client():
    """
    Create a Vapi client with proper error handling.
    This function ensures that only the correct parameters are passed to the Vapi client.
    """
    try:
        # Clear any proxy-related environment variables that might be causing issues
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'http_proxy', 'https_proxy', 'no_proxy']
        for var in proxy_vars:
            if var in os.environ:
                del os.environ[var]
        
        # Clear any Vapi-related environment variables that might be causing issues
        vapi_vars = ['VAPI_INSTALL', 'VAPI_CONFIG', 'VAPI_ENV']
        for var in vapi_vars:
            if var in os.environ:
                del os.environ[var]
        
        # Create Vapi client with only the required parameters
        # This prevents issues with unexpected parameters like 'proxies'
        print(f"Creating Vapi client with API key: {VAPI_PUBLIC_KEY[:8]}..." if VAPI_PUBLIC_KEY else "Creating Vapi client...")
        
        # Try to create the client with explicit parameter filtering
        try:
            return Vapi(api_key=VAPI_PUBLIC_KEY)
        except TypeError as e:
            if "proxies" in str(e):
                # Handle the proxies issue by ensuring clean initialization
                print("Warning: Detected proxies parameter issue, attempting clean initialization...")
                # Try to create the client with explicit parameter filtering
                try:
                    # Import the module again to ensure clean state
                    import vapi_python
                    client = vapi_python.Vapi(api_key=VAPI_PUBLIC_KEY)
                    return client
                except Exception as inner_e:
                    print(f"Failed to create client with clean initialization: {inner_e}")
                    raise e
            else:
                raise e
                
    except Exception as e:
        print(f"Error creating Vapi client: {e}")
        raise e

def main():
    """
    This function initializes the Vapi client and starts a call.
    The call will run until you stop the script.
    """
    # Check if required environment variables are set
    if not VAPI_PUBLIC_KEY:
        print("Error: VAPI_PUBLIC_KEY not found in environment variables.")
        print("Please create a .env file with your Vapi Public Key:")
        print("VAPI_PUBLIC_KEY=your-public-key-here")
        return
    
    if not ASSISTANT_ID:
        print("Error: ASSISTANT_ID not found in environment variables.")
        print("Please create a .env file with your Assistant ID:")
        print("ASSISTANT_ID=your-assistant-id-here")
        return

    try:
        # Initialize the Vapi client using the wrapper function
        print("Initializing Vapi client...")
        vapi = create_vapi_client()
        print("✅ Vapi client initialized successfully!")

        # Start the call with your assistant
        # The SDK handles the WebSocket connection and audio streaming
        print("Starting call with assistant...")
        vapi.start(assistant_id=ASSISTANT_ID)

        print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Call is active. You can now talk to the agent.")
        print("Press Ctrl+C to stop the call.")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")

        # Keep the script running while the call is active
        # The actual conversation happens in background threads managed by the SDK
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping the call...")
        # The 'stop' method will gracefully close the connection
        if 'vapi' in locals():
            vapi.stop()
        print("Call stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Print more detailed error information for debugging
        import traceback
        traceback.print_exc()
        
        # Provide helpful error information
        print("\n--- Troubleshooting Tips ---")
        print("1. Make sure your VAPI_PUBLIC_KEY is correct in the .env file")
        print("2. Make sure your ASSISTANT_ID is correct in the .env file")
        print("3. Check that you have a stable internet connection")
        print("4. Try running 'pip install --upgrade vapi_python' to update the SDK")
        print("5. If the issue persists, please check the Vapi documentation for any known issues")

if __name__ == "__main__":
    main()
