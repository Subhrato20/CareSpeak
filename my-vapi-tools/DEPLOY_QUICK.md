# Quick Deployment Guide for Vapi Tools

This guide will help you deploy your symptom search tool to Render (recommended) or other platforms.

## Prerequisites

1. **SearchAPI Account**: Get your API key from [searchapi.io](https://www.searchapi.io/)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
3. **Vapi Account**: You need a Vapi account for integration

## Option 1: Deploy to Render (Recommended)

### Step 1: Prepare Your Repository

1. **Push your `my-vapi-tools` directory to GitHub**:
   ```bash
   cd my-vapi-tools
   git init
   git add .
   git commit -m "Initial commit: Vapi symptom search tool"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Verify your repository structure**:
   ```
   my-vapi-tools/
   ├── symptom_search_tool.py
   ├── symptom_search_server.py
   ├── requirements.txt
   ├── Procfile
   ├── render.yaml
   ├── runtime.txt
   ├── .gitignore
   └── README.md
   ```

### Step 2: Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `symptom-search-tool`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn symptom_search_server:app`
5. **Add environment variables**:
   - `SEARCHAPI_API_KEY`: Your SearchAPI key
6. **Click "Create Web Service"**

### Step 3: Get Your URL

Once deployed, Render will provide a URL like:
```
https://your-app-name.onrender.com
```

## Option 2: Deploy to Railway

### Step 1: Deploy to Railway

1. **Go to [Railway Dashboard](https://railway.app)**
2. **Click "Deploy from GitHub repo"**
3. **Select your repository**
4. **Add environment variables**:
   - `SEARCHAPI_API_KEY`: Your SearchAPI key
5. **Deploy**

## Option 3: Deploy to Heroku

### Step 1: Deploy to Heroku

```bash
# Install Heroku CLI
brew install heroku

# Login and create app
heroku login
heroku create your-app-name

# Add environment variables
heroku config:set SEARCHAPI_API_KEY=your-searchapi-key

# Deploy
git push heroku main
```

## Testing Your Deployment

Once deployed, test your application:

```bash
# Test the root endpoint
curl https://your-app-url.com/

# Test the health endpoint
curl https://your-app-url.com/health

# Test the symptom search endpoint
curl -X POST https://your-app-url.com/search_symptoms \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "headache and fever"}'
```

## Integrate with Vapi

### Step 1: Update Tool Configuration

1. **Update the webhook URL** in `vapi_tool_config.json`:
   ```json
   {
     "url": "https://your-app-url.com/webhook"
   }
   ```

2. **Create the tool in Vapi**:
   ```bash
   curl -X POST https://api.vapi.ai/tool \
     -H "Authorization: Bearer YOUR_VAPI_API_KEY" \
     -H "Content-Type: application/json" \
     -d @vapi_tool_config.json
   ```

### Step 2: Add Tool to Your Assistant

1. **Go to [Vapi Dashboard](https://dashboard.vapi.ai)**
2. **Navigate to your assistant**
3. **Go to "Tools" section**
4. **Add the `symptom_search_tool`**
5. **Test with voice conversations**

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   - Check if `gunicorn` is in `requirements.txt`
   - Verify the start command is correct
   - Check logs for Python errors

2. **Environment Variables Not Set**
   - Verify `SEARCHAPI_API_KEY` is configured
   - Check if the variable name is correct

3. **API Key Issues**
   - Ensure `SEARCHAPI_API_KEY` is valid
   - Check if the API key has sufficient credits

4. **Port Issues**
   - Most platforms auto-detect the port
   - Some platforms require using `PORT` environment variable

### Debug Mode

For debugging, you can temporarily enable debug mode by modifying `symptom_search_server.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
```

**Note**: Remember to disable debug mode in production.

## Next Steps

1. **Test your deployment** with the provided test commands
2. **Update Vapi tool configuration** with your deployed URL
3. **Create the tool in Vapi** dashboard or via API
4. **Add the tool to your assistant**
5. **Test with voice conversations**

## Support

- **Render**: [Render Documentation](https://render.com/docs)
- **Railway**: [Railway Documentation](https://docs.railway.app)
- **Heroku**: [Heroku Documentation](https://devcenter.heroku.com)
- **Vapi**: [Vapi Documentation](https://docs.vapi.ai)
