# AI Meeting Scheduler

An intelligent meeting scheduler that extracts meeting details from chat conversations using Google's Gemini AI.

## Features

- 🤖 AI-powered meeting intent detection
- 💬 Chat interface with WhatsApp-style design
- 📅 Automatic date and time extraction
- 👥 Participant identification and email resolution
- 🎨 Modern, responsive UI with Flask templates

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ai-meeting-scheduler
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API key:**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the `GOOGLE_API_KEY` in `backend/config.py`

4. **Run the application:**
   ```bash
   cd backend
   python app.py
   ```

5. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

1. The app will automatically load sample chat data
2. The AI will extract meeting details from the conversation
3. View the extracted information in the "AI Extracted Meeting Information" section
4. Click the "Refresh" button to reload the data

## API Endpoints

- `GET /` - Main application page
- `GET /chat/<user_id>` - Get chat messages for a user
- `POST /schedule` - Extract meeting details from chat

## Project Structure

```
ai-meeting-scheduler/
├── backend/
│   ├── app.py              # Flask server with templates
│   ├── agent.py            # AI meeting extraction
│   ├── config.py           # Configuration
│   ├── templates/
│   │   └── index.html      # Main application template
│   └── database/
│       ├── db.py           # Database operations
│       └── users.db        # SQLite database
└── requirements.txt
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Google API key is correctly set in `backend/config.py`
2. **Database Error**: The SQLite database should be automatically created with sample data
3. **Port Already in Use**: If port 5000 is busy, change the port in `backend/config.py`

### Getting Help

If you encounter any issues:
1. Check the terminal running the Flask app for server errors
2. Ensure the Google API key is valid and has proper permissions
3. Verify all dependencies are installed correctly

## Technologies Used

- **Backend**: Flask, Google Gemini AI, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: WhatsApp-inspired design with responsive layout 