# GitVideo

> 🎬 Turn any GitHub repository into a stunning video using AI

GitVideo is a web application that generates beautiful showcase videos for GitHub repositories using OpenAI's Sora video generation model.

## Features

- 🔗 **Easy Input** - Just paste a GitHub repository URL
- 🔑 **BYOK** - Bring your own OpenAI API key (never stored)
- 🎨 **5 Video Styles** - Tech, Cinematic, Minimal, Dynamic, Documentary
- ⚡ **Fast Processing** - Real-time progress updates
- 📥 **Download & Share** - Get your video and share on social media

## Architecture

```
gitvideo/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── main.py         # API endpoints
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Business logic
│   │       ├── repo_service.py    # GitHub repo ingestion
│   │       └── video_service.py   # Sora video generation
│   └── requirements.txt
│
├── frontend/                # React + Vite frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api/            # API client
│   │   └── types/          # TypeScript types
│   └── package.json
│
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key with Sora access

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

### POST /api/generate

Start video generation for a repository.

**Request:**
```json
{
  "repo_url": "https://github.com/facebook/react",
  "openai_api_key": "sk-...",
  "video_style": "tech",
  "duration": 30
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "message": "Video generation started",
  "status_url": "/api/status/{job_id}"
}
```

### GET /api/status/{job_id}

Get the status of a video generation job.

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "message": "Generating video with Sora...",
  "progress": 60,
  "video_url": null
}
```

### GET /api/video/{job_id}

Download or get the URL of the generated video.

## Video Styles

| Style | Description |
|-------|-------------|
| **Tech** | Futuristic, neon accents, holographic displays, dark background |
| **Cinematic** | Wide shots, dramatic lighting, film grain, anamorphic lens |
| **Minimal** | Clean white space, subtle animations, elegant typography |
| **Dynamic** | Fast-paced, energetic motion graphics, vibrant colors |
| **Documentary** | Authentic, informative, professional, subtle motion |

## How It Works

1. **Repository Analysis**: GitVideo fetches your repository's metadata, README, file structure, languages, and topics using the GitHub API.

2. **Script Generation**: GPT-4o creates a compelling video script based on the repository's purpose, tech stack, and features.

3. **Video Generation**: OpenAI Sora generates a professional video using the script and selected visual style.

4. **Delivery**: The video is made available for download and sharing.

## Environment Variables

### Backend

```env
HOST=0.0.0.0
PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend

```env
VITE_API_URL=http://localhost:8000
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **OpenAI SDK** - Sora API integration

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Security

- API keys are **never stored** on our servers
- Keys are only used for the duration of the request
- All API communication is done over HTTPS
- No repository data is persisted
