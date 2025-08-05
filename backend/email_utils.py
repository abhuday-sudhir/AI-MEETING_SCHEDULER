import os
from flask_mail import Mail, Message
from flask import current_app
from datetime import datetime

# Initialize Flask-Mail
mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with the app"""
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail.init_app(app)

def send_meeting_confirmation(meeting_details, participant_emails):
    """
    Send confirmation emails to all meeting participants
    
    Args:
        meeting_details (dict): Meeting details including date, time, participants, etc.
        participant_emails (dict): Dictionary mapping participant names to emails
    """
    if not participant_emails:
        return {"success": False, "error": "No participant emails found"}
    
    try:
        # Prepare email content
        subject = f"Meeting Confirmation: {meeting_details.get('meeting_title', 'Team Meeting')}"
        
        # Format date and time
        date_str = meeting_details.get('date', 'TBD')
        time_str = meeting_details.get('time', 'TBD')
        location = meeting_details.get('location', 'TBD')
        
        # Create email body
        body = f"""
Dear Participant,

This is a confirmation for the following meeting:

Meeting: {meeting_details.get('meeting_title', 'Team Meeting')}
Date: {date_str}
Time: {time_str}
Location: {location}

Participants:
{chr(10).join([f"- {name} ({email})" for name, email in participant_emails.items()])}

Please mark your calendar and let us know if you have any conflicts.

Best regards,
AI Meeting Scheduler
        """
        
        # Send email to each participant
        sent_emails = []
        failed_emails = []
        
        for name, email in participant_emails.items():
            try:
                msg = Message(
                    subject=subject,
                    recipients=[email],
                    body=body
                )
                mail.send(msg)
                sent_emails.append(email)
            except Exception as e:
                failed_emails.append({"email": email, "error": str(e)})
        
        return {
            "success": True,
            "sent_emails": sent_emails,
            "failed_emails": failed_emails,
            "total_participants": len(participant_emails)
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to send confirmation emails: {str(e)}"}

def send_meeting_confirmation_simple(meeting_details, participant_emails):
    """
    Simple version that just returns success/failure without actually sending emails
    (for testing purposes when email is not configured)
    """
    if not participant_emails:
        return {"success": False, "error": "No participant emails found"}
    
    # Simulate email sending
    sent_emails = list(participant_emails.values())
    
    return {
        "success": True,
        "sent_emails": sent_emails,
        "failed_emails": [],
        "total_participants": len(participant_emails),
        "message": "Emails would be sent in production environment"
    } 