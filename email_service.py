"""
Hotel Booking System - Email Service

This module handles sending email notifications to guests for:
- Booking confirmations
- Booking modifications
- Booking cancellations

Requires Gmail account with app-specific password (not regular password).

Functions:
    send_email: Send email notification to recipient
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Javier Herrera 11/21/2025 This doesn't work as well as I want it to yet
    """
    Send an email notification to a guest.
    Args:
        sender_email (str): Email address to send from
        sender_password (str): Gmail app-specific password (NOT regular password)
        recipient_email (str): Guest email address
        subject (str): Email subject line
        message (str): Email message body (plain text)
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        #Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        #Connect to Gmail server
        print(f"Connecting to Gmail server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
        #Login with credentials
        print(f"Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        
        #Send email
        print(f"Sending email to {recipient_email}...")
        server.send_message(msg)
        
        #Disconnect
        server.quit()
        
        print(f"Email was sent!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("Gmail authentication failed. Check your app password.")
        return False
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False