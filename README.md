# Unilever HR Chatbot

Unilever-themed page with a floating chat button. FastAPI backend answers questions from an HR policy PDF using Azure OpenAI `gpt-4o-mini`, with per-session memory.

```
backend/   FastAPI app (main.py, policy.py, memory.py, config.py, data/hr_policy.pdf)
frontend/  index.html, styles.css, app.js, assets/unilever-logo.svg
```

## 1. Prepare
1. Put your policy at `backend/data/hr_policy.pdf` (must be text-based, not a scanned image).
2. Replace `frontend/assets/unilever-logo.svg` with the official Unilever logo.
3. Copy `.env.example` to `.env` and fill in the Azure OpenAI values (step 3 below).

## 2. Run locally
```
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
cd backend
uvicorn main:app --reload
```
Open http://localhost:8000 and click the chat button.

## 3. Create Azure OpenAI (the LLM)
1. Sign up at https://portal.azure.com (free account).
2. Create a resource: **Azure OpenAI**. Pick a region that offers gpt-4o-mini (e.g. East US, Sweden Central).
3. Open it, go to **Azure AI Foundry** -> **Deployments** -> **Deploy model** -> `gpt-4o-mini` (Standard). Name it `gpt-4o-mini`.
4. Copy the **Endpoint** and a **Key** (Resource -> Keys and Endpoint) into `.env`.
5. Set a budget alert: **Cost Management -> Budgets -> Add**, e.g. $5.

## 4. Push to GitHub
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```
`.env` is git-ignored so your key is never uploaded.

## 5. Create the Azure Web App
1. Portal -> **Create a resource -> Web App**.
2. Publish: **Code**; Runtime stack: **Python 3.11**; OS: **Linux**; Pricing plan: **Free F1**; pick a region near you.
3. Create, then open the app.

## 6. Configure it
- **Settings -> Environment variables**: add `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `AZURE_OPENAI_DEPLOYMENT` (same as `.env`). Save.
- **Settings -> Configuration -> Startup Command**:
  `cd backend && gunicorn -k uvicorn.workers.UvicornWorker main:app`
  (If it fails to find modules, try `gunicorn -k uvicorn.workers.UvicornWorker --chdir backend main:app`.)

## 7. Auto deploy from GitHub
**Deployment Center** -> Source: **GitHub** -> authorize -> choose your repo and `main` branch -> Save. Azure adds a GitHub Actions workflow to your repo; every push to `main` redeploys. Pull the new workflow file locally with `git pull`.

## 8. Test
- `https://<your-app>.azurewebsites.net/api/health` -> `{"status":"ok"}`
- Open the site and chat. Problems? **Monitoring -> Log stream**.
- First request after idle can take ~30s (Free tier sleeps).

## 9. Keep costs near zero
Stay on Free F1, keep the budget alert, and delete the resource group when you finish learning.

## Notes
- Memory is stored in the server process (last 10 messages per browser session) and resets on restart.
- The bot answers only from the PDF; unknown questions get a "contact HR" reply.
