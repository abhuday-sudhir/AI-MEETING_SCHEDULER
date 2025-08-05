import google.generativeai as genai
import json
import re
from datetime import datetime, timedelta
from config import GOOGLE_API_KEY

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)

def debug_date_parsing(date_str):
    """Debug function to test date parsing"""
    print(f"Debug: Parsing date string: '{date_str}'")
    result = parse_date(date_str)
    print(f"Debug: Result: '{result}'")
    return result

def parse_date(date_str):
    """Parse date string and return actual date"""
    if not date_str:
        return None
    
    date_str = date_str.lower().strip()
    today = datetime.now()
    current_year = today.year
    
    # Handle "tomorrow"
    if date_str == "tomorrow":
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")
    
    # Handle "today"
    if date_str == "today":
        return today.strftime("%Y-%m-%d")
    
    # Handle "next week"
    if "next week" in date_str:
        next_week = today + timedelta(days=7)
        return next_week.strftime("%Y-%m-%d")
    
    # Handle "next month"
    if "next month" in date_str:
        next_month = today.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
        return next_month.strftime("%Y-%m-%d")
    
    # Try to parse existing date formats
    try:
        # Common date formats
        date_formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%m/%d/%y",  # 2-digit year
            "%d/%m/%y",   # 2-digit year
            "%B %d",      # Month day without year
            "%b %d",      # Abbreviated month day without year
            "%d %B",      # Day month without year
            "%d %b"       # Day abbreviated month without year
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                
                # If the format doesn't include year, assume current year
                if "%Y" not in fmt and "%y" not in fmt:
                    parsed_date = parsed_date.replace(year=current_year)
                
                # If the parsed year is 2024 but current year is different, update it
                if parsed_date.year == 2024 and current_year != 2024:
                    parsed_date = parsed_date.replace(year=current_year)
                
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If no format matches, return as is
        return date_str
    except Exception as e:
        return date_str

def extract_meeting_details(chat_messages):
    chat_text = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in chat_messages])
    
    # Get current date for reference
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    prompt = f"""
Here is a chat conversation. Extract any meeting intent from it. 

IMPORTANT RULES:
1. If there are multiple contradictory statements about meeting details, use the LAST meeting message in the conversation
2. For dates, if "tomorrow" is mentioned, use the actual date: {tomorrow.strftime("%Y-%m-%d")}
3. If "today" is mentioned, use today's date: {today.strftime("%Y-%m-%d")}
4. Always use the current year ({today.year}) for any dates
5. Return JSON with:
   - date (actual date in YYYY-MM-DD format, not "tomorrow" or "today")
   - time (in HH:MM format if available)
   - participants (list of participant names)
   - intent_detected (true/false)
   - meeting_title (if mentioned)
   - location (if mentioned)

Chat:
{chat_text}
"""

    try:
        # Use gemini-1.5-flash instead of gemini-pro
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove code block markers if present
        if response_text.startswith('```'):
            response_text = re.sub(r'^```\w*\n', '', response_text)
            response_text = re.sub(r'\n```$', '', response_text)
        
        # Try to parse as JSON first
        try:
            result = json.loads(response_text)
            
            # Parse the date if it exists
            if result.get("date"):
                result["date"] = parse_date(result["date"])
            
            return result
        except json.JSONDecodeError:
            # Fallback to eval for backward compatibility
            try:
                result = eval(response_text)
                if result.get("date"):
                    result["date"] = parse_date(result["date"])
                return result
            except:
                # If all parsing fails, return a basic response
                return {
                    "intent_detected": False,
                    "error": "Could not parse AI response",
                    "raw_response": response_text
                }
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            return {
                "intent_detected": False,
                "error": "Invalid Google API key. Please check your API key configuration."
            }
        elif "quota" in error_msg.lower():
            return {
                "intent_detected": False,
                "error": "API quota exceeded. Please check your Google AI usage limits."
            }
        elif "not found" in error_msg.lower():
            return {
                "intent_detected": False,
                "error": "Model not available. Please check your API access."
            }
        else:
            return {
                "intent_detected": False,
                "error": f"AI processing error: {error_msg}"
            }
