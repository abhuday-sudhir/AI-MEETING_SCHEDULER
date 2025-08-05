from flask import Flask, render_template, request, jsonify, send_from_directory
from database.db import get_chat_by_user_id, resolve_emails
from agent import extract_meeting_details
from email_utils import init_mail, send_meeting_confirmation
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__, static_folder='static')

# Initialize email functionality
init_mail(app)

@app.route("/")
def index():
    try:
        # Get all available user IDs (1, 2, 3 for our sample data)
        user_ids = [1, 2, 3]
        chats = {}
        
        # Load all chats
        for user_id in user_ids:
            chats[user_id] = get_chat_by_user_id(user_id)
        
        return render_template('index.html', chats=chats)
    except Exception as e:
        return render_template('index.html', chats={})

@app.route("/chat/<int:user_id>", methods=["GET"])
def get_chat(user_id):
    try:
        return jsonify(get_chat_by_user_id(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/schedule", methods=["POST"])
def schedule():
    try:
        data = request.get_json()
        user_id = data.get("user_id", 1)
        
        chat = get_chat_by_user_id(user_id)
        result = extract_meeting_details(chat)
        
        if result.get("participants"):
            result["emails"] = resolve_emails(result["participants"])
            
            # Send confirmation emails if meeting intent is detected
            if result.get("intent_detected") and result.get("emails"):
                email_result = send_meeting_confirmation(result, result["emails"])
                result["email_confirmation"] = email_result
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send-confirmation", methods=["POST"])
def send_confirmation():
    """Endpoint to manually send confirmation emails"""
    try:
        data = request.get_json()
        meeting_details = data.get("meeting_details", {})
        participant_emails = data.get("participant_emails", {})
        
        if not participant_emails:
            return jsonify({"error": "No participant emails provided"}), 400
        
        # Send confirmation emails
        email_result = send_meeting_confirmation(meeting_details, participant_emails)
        
        return jsonify(email_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
