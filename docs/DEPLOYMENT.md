# 🚀 RTIAssist API — Hugging Face Deployment Guide

## Prerequisites

1. **Hugging Face Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Git**: Install git on your system
3. **Git LFS**: Install Git Large File Storage

## Deployment Steps

### Method 1: Using Hugging Face Web Interface (Easiest)

1. **Create a New Space**
   - Go to https://huggingface.co/new-space
   - Name: `rtiassist-api` (or your choice)
   - License: MIT
   - SDK: Select **Docker**
   - Make it public or private as preferred

2. **Upload Files**
   - Upload all project files to the Space
   - Make sure to include:
     - `app.py` (entry point)
     - `main.py`
     - `requirements.txt`
     - `Dockerfile`
     - All folders: `agents/`, `models/`, `prompts/`, `routes/`, `utils/`
     - `README_HF.md` (rename to `README.md` in the Space)

3. **Set Secrets (Optional)**
   - Go to Space Settings → Variables and secrets
   - Add your environment variables:
     - `ASI1_API_KEY` (if using real API)
     - `ASI1_API_URL`
     - `TELEGRAM_TOKEN` (if using bot)

4. **Build & Deploy**
   - Hugging Face will automatically build and deploy
   - Wait for build to complete
   - Your API will be available at: `https://YOUR_USERNAME-rtiassist-api.hf.space`

### Method 2: Using Git (For Developers)

1. **Clone the Space Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/rtiassist-api
   cd rtiassist-api
   ```

2. **Copy Project Files**
   ```bash
   # Copy all files from your local project to the cloned Space
   cp -r /path/to/your/rtiassist-api/* .
   ```

3. **Create README.md with Metadata**
   ```bash
   # Add header to README.md (first lines)
   cat > README.md << 'EOF'
   ---
   title: RTIAssist API
   emoji: 🏛️
   colorFrom: blue
   colorTo: green
   sdk: docker
   pinned: true
   license: mit
   app_port: 7860
   ---
   EOF
   
   # Append your README content
   cat README_HF.md >> README.md
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push
   ```

5. **Monitor Build**
   - Go to your Space page
   - Check the "Building" tab for logs
   - Wait for deployment to complete

## Configuration

### Demo Mode (Default)

By default, the API runs in demo mode on Hugging Face (no API key needed):
- Instant responses
- Sample RTI applications
- Perfect for demonstrations

To enable real API mode:
1. Add `ASI1_API_KEY` in Space secrets
2. Set `DEMO_MODE=false` in environment

### Environment Variables

Add in Space Settings → Variables and secrets:

```
ASI1_API_KEY=your_api_key_here
ASI1_API_URL=https://api.asi1.ai/v1
DEMO_MODE=false
```

## Testing Your Deployment

Once deployed, test the API:

```bash
# Health check
curl https://YOUR_USERNAME-rtiassist-api.hf.space/health

# Generate RTI (demo mode)
curl -X POST "https://YOUR_USERNAME-rtiassist-api.hf.space/rti/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My ration card was rejected in Maharashtra 3 months ago",
    "language": "english",
    "state": "Maharashtra",
    "demo_mode": true
  }'

# View API documentation
# Visit: https://YOUR_USERNAME-rtiassist-api.hf.space/docs
```

## Updating Your Deployment

### Web Interface
1. Go to your Space
2. Click "Files" tab
3. Edit files directly or upload new versions
4. Space will automatically rebuild

### Git
```bash
# Make changes locally
git add .
git commit -m "Update: your changes"
git push
```

## Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Ensure all dependencies in requirements.txt
- Check build logs in "Building" tab

### API Not Responding
- Check if Space is in "Running" state
- Verify port 7860 is exposed
- Check application logs

### Demo Mode Not Working
- Verify `DEMO_MODE=true` in environment
- Check `demo_mode` parameter in request
- Review application logs

### Memory Issues
- Docker SDK on HF has memory limits
- Consider using Gradio SDK for lighter deployment
- Optimize code to reduce memory usage

## Custom Domain (Optional)

Hugging Face Spaces URL:
```
https://YOUR_USERNAME-rtiassist-api.hf.space
```

For custom domain:
1. Go to Space Settings
2. Configure custom domain (Pro feature)

## Monitoring

- **Logs**: Check Space logs tab
- **Analytics**: View visitor stats in Space dashboard
- **Errors**: Monitor application logs for issues

## Cost

- **Free Tier**: Limited resources, public Spaces
- **Pro Tier**: More resources, private Spaces, custom domains

## Next Steps

1. ✅ Deploy to Hugging Face
2. Test all endpoints
3. Share your Space URL
4. Monitor usage and performance
5. Add to your README and documentation

## Support

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Community**: https://discuss.huggingface.co/
- **Issues**: Open issue in your project repository

---

**Happy Deploying! 🚀**
