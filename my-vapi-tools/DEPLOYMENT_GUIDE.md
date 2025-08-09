# Deployment Guide for Symptom Search Tool

This guide provides step-by-step instructions for deploying the symptom search tool to various cloud platforms.

## Prerequisites

1. **SearchAPI Account**: You need a SearchAPI account and API key
2. **Vapi Account**: You need a Vapi account for the tool integration
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)

## Deployment Options

### Option 1: Render (Recommended for Beginners)

[Render](https://render.com) is a simple cloud platform that's perfect for deploying Python Flask applications.

#### Step 1: Prepare Your Repository

1. **Add a `render.yaml` file** to your repository root:

```yaml
services:
  - type: web
    name: symptom-search-tool
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn symptom_search_server:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
      - key: SEARCHAPI_API_KEY
        sync: false
```

2. **Add `gunicorn` to requirements.txt**:

```txt
vapi_python==0.1.9
daily-python==0.19.6
pyaudio==0.2.14
requests==2.32.4
python-dotenv==1.1.1
flask==3.0.0
gunicorn==21.2.0
```

#### Step 2: Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `symptom-search-tool`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn symptom_search_server:app`
5. Add environment variables:
   - `SEARCHAPI_API_KEY`: Your SearchAPI key
6. Click **Create Web Service**

#### Step 3: Get Your URL

Once deployed, Render will provide a URL like:
```
https://your-app-name.onrender.com
```

### Option 2: Railway

[Railway](https://railway.app) is another excellent option for quick deployments.

#### Step 1: Prepare Your Repository

1. **Add a `Procfile`** to your repository root:

```
web: gunicorn symptom_search_server:app
```

2. **Add `gunicorn` to requirements.txt** (same as Render)

#### Step 2: Deploy to Railway

1. Go to [Railway Dashboard](https://railway.app)
2. Click **Deploy from GitHub repo**
3. Select your repository
4. Railway will automatically detect it's a Python app
5. Add environment variables:
   - `SEARCHAPI_API_KEY`: Your SearchAPI key
6. Deploy

### Option 3: Heroku

[Heroku](https://heroku.com) is a mature platform with excellent Python support.

#### Step 1: Prepare Your Repository

1. **Add a `Procfile`**:

```
web: gunicorn symptom_search_server:app
```

2. **Add `gunicorn` to requirements.txt**

3. **Add `runtime.txt`** (optional, for specific Python version):

```
python-3.9.18
```

#### Step 2: Deploy to Heroku

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add environment variables**:
   ```bash
   heroku config:set SEARCHAPI_API_KEY=your-searchapi-key
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 4: Google Cloud Run

[Google Cloud Run](https://cloud.google.com/run) is a serverless platform by Google.

#### Step 1: Prepare Your Repository

1. **Add a `Dockerfile`**:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 symptom_search_server:app
```

2. **Add `.dockerignore`**:

```
venv/
__pycache__/
*.pyc
.env
.git/
```

#### Step 2: Deploy to Cloud Run

1. **Install Google Cloud CLI**:
   ```bash
   # Follow instructions at https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize and deploy**:
   ```bash
   gcloud init
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/symptom-search-tool
   gcloud run deploy symptom-search-tool \
     --image gcr.io/YOUR_PROJECT_ID/symptom-search-tool \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars SEARCHAPI_API_KEY=your-searchapi-key
   ```

### Option 5: DigitalOcean App Platform

[DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) is simple and cost-effective.

#### Step 1: Prepare Your Repository

1. **Add a `.do/app.yaml`** file:

```yaml
name: symptom-search-tool
services:
  - name: web
    source_dir: /
    github:
      repo: your-username/your-repo
      branch: main
    envs:
      - key: SEARCHAPI_API_KEY
        value: ${SEARCHAPI_API_KEY}
```

#### Step 2: Deploy

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click **Create App**
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy

## Post-Deployment Steps

### 1. Test Your Deployment

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

### 2. Update Vapi Tool Configuration

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

### 3. Add Tool to Your Assistant

1. Go to [Vapi Dashboard](https://dashboard.vapi.ai)
2. Navigate to your assistant
3. Go to **Tools** section
4. Add the `symptom_search_tool`
5. Test with a voice conversation

## Environment Variables

Make sure to set these environment variables in your deployment platform:

| Variable | Description | Required |
|----------|-------------|----------|
| `SEARCHAPI_API_KEY` | Your SearchAPI API key | Yes |
| `PORT` | Port for the server (usually auto-detected) | No |
| `FLASK_ENV` | Set to `production` for production deployments | No |

## Monitoring and Logs

### Render
- **Logs**: Available in the Render dashboard
- **Monitoring**: Automatic health checks

### Railway
- **Logs**: Available in the Railway dashboard
- **Monitoring**: Real-time logs and metrics

### Heroku
- **Logs**: `heroku logs --tail`
- **Monitoring**: Heroku add-ons available

### Google Cloud Run
- **Logs**: Available in Google Cloud Console
- **Monitoring**: Cloud Monitoring integration

### DigitalOcean
- **Logs**: Available in the DigitalOcean dashboard
- **Monitoring**: Built-in monitoring

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   - Check if `gunicorn` is in `requirements.txt`
   - Verify the start command is correct
   - Check logs for Python errors

2. **Environment Variables Not Set**
   - Verify all required environment variables are configured
   - Check if the variable names are correct

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

## Security Considerations

1. **HTTPS**: All platforms mentioned above provide HTTPS by default
2. **Environment Variables**: Never commit API keys to version control
3. **Rate Limiting**: Consider implementing rate limiting for production use
4. **Input Validation**: The application includes input validation
5. **Error Handling**: Comprehensive error handling is implemented

## Cost Estimation

Platform costs (approximate monthly):

- **Render**: Free tier available, $7/month for paid plans
- **Railway**: $5/month for starter plan
- **Heroku**: Free tier deprecated, $7/month for basic dyno
- **Google Cloud Run**: Pay-per-use, typically $1-10/month
- **DigitalOcean**: $5/month for basic app

## Support

For deployment-specific issues:
- **Render**: [Render Documentation](https://render.com/docs)
- **Railway**: [Railway Documentation](https://docs.railway.app)
- **Heroku**: [Heroku Documentation](https://devcenter.heroku.com)
- **Google Cloud**: [Cloud Run Documentation](https://cloud.google.com/run/docs)
- **DigitalOcean**: [App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
