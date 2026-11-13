# 📧 Mail-mind – AI-Powered Email Assistant

Mail-mind is an AI-powered email assistant that integrates with Gmail to fetch live emails and generate intelligent, context-aware reply suggestions using Google's Gemini AI.

The goal of Mail-mind is to reduce the time spent writing repetitive emails by helping users generate relevant and natural responses with the assistance of Large Language Models (LLMs).

## ✨ Features

- **Gmail Integration:** Connects with a Gmail account to fetch real emails using the Gmail API.
- **AI-Powered Replies:** Uses Google's Gemini API to generate relevant email reply suggestions.
- **Email Processing:** Processes email content before passing it to the AI model.
- **Context-Aware Responses:** Uses the email content as context to generate appropriate replies.
- **Full-Stack Architecture:** Separates the frontend interface from the Python backend.
- **API-Based Communication:** Uses backend APIs to coordinate email fetching and AI response generation.

## 🏗️ Architecture

Mail-mind follows a frontend-backend architecture.

```text
             USER
               |
               v
        FRONTEND (UI)
               |
               v
         PYTHON BACKEND
               |
        +------+------+
        |             |
        v             v
    Gmail API     Email Processing
        |             |
        v             v
   Fetch Emails   Process Content
        |             |
        +------+------+
               |
               v
          GEMINI API
               |
               v
       Generate Reply
               |
               v
        Return Response
               |
               v
         FRONTEND (UI)
```

## 🔄 How It Works

1. **Gmail Authentication:** The application connects to the user's Gmail account using Google's OAuth 2.0 authentication.
2. **Fetch Emails:** The backend retrieves emails from Gmail through the Gmail API.
3. **Email Processing:** Retrieved email content is processed and prepared for the AI model.
4. **AI Processing:** The processed email content is sent to Google's Gemini API.
5. **Reply Generation:** Gemini analyzes the email and generates a suitable reply.
6. **Display Response:** The generated reply is returned to the frontend for the user.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | Backend API framework |
| React | Frontend development |
| Google Gmail API | Fetching emails |
| Google OAuth 2.0 | Gmail authentication |
| Google Gemini API | AI-powered reply generation |
| spaCy | Natural language processing |
| SQLAlchemy | Database interaction |
| Uvicorn | ASGI server |
| Pydantic | Data validation |

## 📂 Project Structure

```text
Mail-mind/
│
├── backend/
│   └── Backend application and processing logic
│
├── frontend/
│   └── Frontend application and user interface
│
├── requirements.txt
├── test_gemini.py
├── test_gmail.py
├── test_pipeline.py
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/subz-gpu/Mail-mind.git
cd Mail-mind
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

Configure the required credentials for:

- Google Gmail API
- Google OAuth 2.0 credentials
- Google Gemini API key

Create a `.env` file in the appropriate backend configuration location and add the required environment variables.

**Important:** Never commit API keys, OAuth client secrets, or access tokens to GitHub.

### 5. Run the Application

Start the backend using its FastAPI entry point with Uvicorn.

```bash
uvicorn <backend_module>:app --reload
```

Start the frontend separately using its configured development command.

## 🧪 Testing

The repository includes separate test scripts for different components:

```bash
python test_gmail.py
```

```bash
python test_gemini.py
```

```bash
python test_pipeline.py
```

These scripts help test Gmail integration, Gemini functionality, and the overall processing pipeline.

## 🎯 Project Objective

Mail-mind demonstrates how AI and API integration can be used to automate repetitive communication tasks.

The project combines Gmail integration, natural language processing, and Large Language Models to make email communication faster and more efficient.

## 🚀 Future Improvements

- Support for multiple email providers.
- Improved personalization based on user writing style.
- Email categorization and priority detection.
- Conversation history and contextual reply generation.
- User-controlled reply editing and sending.
- Improved security and error handling.

## 👨‍💻 Author

**Subham Dewan**

- GitHub: [@subz-gpu](https://github.com/subz-gpu)

---

⭐ If you find this project interesting, feel free to explore the repository and share your feedback!
