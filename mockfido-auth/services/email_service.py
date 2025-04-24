import yagmail
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_challenge_email(to_email, challenge):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_SENDER and EMAIL_PASSWORD must be set in your .env file.")

    try:
        yag = yagmail.SMTP(user=EMAIL_SENDER, password=EMAIL_PASSWORD)
        subject = "🔐 Your FIDO2 Challenge"
        contents = f"""
        Hi there,

        Here is your secure login challenge:

        {challenge}

        Please copy this into the login interface to continue.

        Best,  
        Your Auth Bot
        """
        yag.send(to=to_email, subject=subject, contents=contents)
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")
