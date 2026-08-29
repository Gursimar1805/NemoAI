# ✨ NemoAI — AI Chat Assistant

An all-purpose AI chatbot powered by NVIDIA's Nemotron models via [OpenRouter](https://openrouter.ai), with a FastAPI backend and a custom-styled Streamlit frontend.

**Live app:** https://nemoai-2.onrender.com/
**Backend API:** https://nemoai-1.onrender.com

> Note: both services run on Render's free tier and spin down after ~15 minutes of inactivity. The first message after idle time may take up to a minute while the service wakes up — this is expected, not a bug.

---

## Features

- Streaming responses (token-by-token) via Server-Sent Events
- General-purpose assistant — daily questions, assignments, coding help, explanations
- Custom glassmorphic UI with animated gradient branding
- Clear error handling for backend/connection failures instead of silent blank replies
- Clean separation between backend (API logic) and frontend (UI)

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, httpx, Server-Sent Events streaming |
| Frontend | Streamlit, custom CSS |
| Model | NVIDIA Nemotron (`nvidia/nemotron-3.5-lightning:free`) via OpenRouter |
| Hosting | Render (both services) |

## Project Structure

\`\`\`
NemoAI/
├── backend/
│   ├── main.py           # FastAPI app, /chat and /health routes
│   ├── llm.py             # OpenRouter API calls, streaming logic
│   ├── prompts.py         # System prompt and message building
│   ├── requirements.txt
│   └── runtime.txt        # Pins Python 3.11 for Render
├── frontend/
│   ├── app.py              # Streamlit chat UI
│   ├── requirements.txt
│   └── runtime.txt        # Pins Python 3.11 for Render
└── README.md
\`\`\`

## Local Setup

1. **Clone the repo**
   \`\`\`bash
   git clone https://github.com/Gursimar1805/NemoAI.git
   cd NemoAI
   \`\`\`

2. **Create and activate a virtual environment**
   \`\`\`bash
   python -m venv venv
   .\\venv\\Scripts\\Activate.ps1      # Windows PowerShell
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   \`\`\`

4. **Add your OpenRouter API key**

   Create a \`.env\` file in the project root:
   \`\`\`
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   \`\`\`
   Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).

5. **Run the backend**
   \`\`\`bash
   cd backend
   uvicorn main:app --reload --port 8000
   \`\`\`

6. **Run the frontend** (in a second terminal)
   \`\`\`bash
   cd frontend
   streamlit run app.py
   \`\`\`

   Update \`BACKEND_URL\` in \`frontend/app.py\` to \`http://localhost:8000\` for local testing.

## Deployment

Both services are deployed separately on [Render](https://render.com):

**Backend**
- Root Directory: \`backend\`
- Build Command: \`pip install -r requirements.txt\`
- Start Command: \`uvicorn main:app --host 0.0.0.0 --port $PORT\`
- Environment Variable: \`OPENROUTER_API_KEY\`

**Frontend**
- Root Directory: \`frontend\`
- Build Command: \`pip install -r requirements.txt\`
- Start Command: \`streamlit run app.py --server.port $PORT --server.address 0.0.0.0\`

> Streamlit Community Cloud was tried first but hit a platform-level bug where the Python version pin is ignored, forcing Python 3.14 and breaking builds that depend on compiled packages (e.g. Pillow). Deploying both services on Render instead resolved this cleanly.

## Notes & Limitations

- Uses OpenRouter's **free tier** — prompts and outputs may be logged by the model provider for improvement purposes. Not intended for confidential or sensitive data.
- Free model availability on OpenRouter can change without notice. If the chatbot stops responding with a \`404\` model error, check [OpenRouter's free models list](https://openrouter.ai/models?max_price=0) and update the \`MODEL\` value in \`backend/llm.py\`.
- \`max_tokens\` in \`llm.py\` caps reply length (currently set for a balance between detail and speed) — increase if responses are getting cut off.

## Roadmap

- [ ] Add RAG (retrieval-augmented generation) over custom documents
- [ ] Per-user conversation persistence
- [ ] Rate limiting per IP on the backend
- [ ] Custom domain

## Author

**Gursimar Singh Kohli**
[GitHub](https://github.com/Gursimar1805) · [LinkedIn](https://linkedin.com/in/gursimar-singh-kohli-9b60a0255/)
