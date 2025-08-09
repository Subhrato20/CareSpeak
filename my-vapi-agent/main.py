import time
import os
from dotenv import load_dotenv
from vapi_python import Vapi

# Load environment variables from .env file
load_dotenv()

# Get API key and assistant ID from environment variables
VAPI_PUBLIC_KEY = os.getenv('VAPI_PUBLIC_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

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
        # Initialize the Vapi client
        vapi = Vapi(api_key=VAPI_PUBLIC_KEY)

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
        vapi.stop()
        print("Call stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
