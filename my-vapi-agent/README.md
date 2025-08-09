# Vapi Agent Python Client

This project demonstrates how to use the Vapi Python SDK to create a real-time voice conversation with a Vapi agent.

## Prerequisites

- Python 3.7 or higher
- macOS (for portaudio support)
- Vapi API key and Assistant ID

## Setup Instructions

### 1. Install Dependencies

If you haven't already installed portaudio on macOS:
```bash
brew install portaudio
```

### 2. Set up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Your Credentials

Create a `.env` file in the project root with your Vapi credentials:

```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual credentials
nano .env  # or use your preferred text editor
```

Your `.env` file should look like this:
```
# Your Vapi Public Key (get this from your Vapi dashboard)
VAPI_PUBLIC_KEY=your-actual-public-key-here

# Your Assistant ID (get this from your Vapi dashboard)
ASSISTANT_ID=your-actual-assistant-id-here
```

**Important**: Replace `your-actual-public-key-here` and `your-actual-assistant-id-here` with your real credentials from the Vapi dashboard.

### 4. Run the Application

```bash
python main.py
```

## How It Works

This application uses the Vapi Python SDK which:

1. **HTTP Request**: Makes a secure HTTP request to the Vapi API (https://api.vapi.ai/call/web)
2. **Web Call URL**: Receives a special webCallUrl from the Vapi API
3. **WebSocket Connection**: Establishes a WebSocket connection with Daily.co servers for real-time communication
4. **Audio Streaming**: 
   - Captures audio from your microphone using pyaudio
   - Sends audio data over WebSocket to the Vapi agent
   - Receives audio responses from the agent
   - Plays the responses through your speakers

## Usage

1. Run the script: `python main.py`
2. Grant microphone permissions when prompted
3. Start talking to your Vapi agent
4. Press `Ctrl+C` to end the conversation

## Environment Variables

The application uses the following environment variables (configured in `.env`):

- `VAPI_PUBLIC_KEY`: Your Vapi Public Key from the dashboard
- `ASSISTANT_ID`: The ID of the assistant you want to call

## Troubleshooting

- **Microphone Access**: Make sure to grant microphone permissions to Python
- **Portaudio Issues**: If you encounter portaudio issues on macOS, ensure it's installed: `brew install portaudio`
- **API Key**: Verify your Vapi API key is correct and has the necessary permissions
- **Assistant ID**: Make sure your Assistant ID is valid and the assistant is properly configured
- **Environment Variables**: Ensure your `.env` file exists and contains the correct credentials
