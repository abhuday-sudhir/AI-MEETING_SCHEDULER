import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY environment variable is not set!")
    print("📝 Please set your Google API key:")
    print("   1. Go to https://makersuite.google.com/app/apikey")
    print("   2. Create a new API key")
    print("   3. Set it as environment variable: export GOOGLE_API_KEY='your-key-here'")
    print("   4. Or create a .env file in the backend directory with: GOOGLE_API_KEY=your-key-here")
    exit(1)

# Database Configuration
DB_PATH = "database/users.db"

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True 