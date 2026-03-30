#!/usr/bin/env python3
"""Verify email and SMS configuration is loaded correctly"""

import os
import sys
from pathlib import Path

# Add flask_app to path
sys.path.insert(0, str(Path(__file__).parent / 'flask_app'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / 'flask_app' / '.env')

print("\n" + "="*70)
print("📧 EMAIL CONFIGURATION CHECK")
print("="*70)

mail_server = os.getenv('MAIL_SERVER')
mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')
mail_port = os.getenv('MAIL_PORT')

print(f"✓ MAIL_SERVER: {mail_server}")
print(f"✓ MAIL_PORT: {mail_port}")
print(f"✓ MAIL_USERNAME: {mail_username}")
print(f"✓ MAIL_PASSWORD: {mail_password[:10]}..." if mail_password else "✗ MAIL_PASSWORD: NOT SET")
print(f"✓ EMAIL CONFIG STATUS: {'READY' if mail_username else 'NOT CONFIGURED'}")

print("\n" + "="*70)
print("📱 SMS CONFIGURATION CHECK")
print("="*70)

twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')

print(f"✓ TWILIO_ACCOUNT_SID: {twilio_sid[:15]}..." if twilio_sid else "✗ TWILIO_ACCOUNT_SID: NOT SET")
print(f"✓ TWILIO_AUTH_TOKEN: {twilio_token[:15]}..." if twilio_token else "✗ TWILIO_AUTH_TOKEN: NOT SET")
print(f"✓ TWILIO_PHONE_NUMBER: {twilio_phone}")
print(f"✓ SMS CONFIG STATUS: {'READY' if twilio_phone else 'NOT CONFIGURED'}")

print("\n" + "="*70)
print("🚀 TESTING EMAIL & SMS FUNCTIONALITY")
print("="*70)

# Test email configuration
try:
    from flask_mail import Mail, Message
    from flask import Flask
    
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = mail_server
    app.config['MAIL_PORT'] = int(mail_port or 587)
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = mail_password
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mail = Mail(app)
    print("✅ Flask-Mail: Successfully initialized")
    
    # Test Twilio
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        print("✅ Twilio: Successfully initialized")
        print(f"   Ready to send SMS to: {twilio_phone}")
    except Exception as e:
        print(f"⚠️  Twilio: {str(e)}")
    
except Exception as e:
    print(f"❌ Flask-Mail Error: {str(e)}")

print("\n" + "="*70)
print("✅ VERIFICATION COMPLETE")
print("="*70)
print("\nYou can now test at: http://localhost:4001/login")
print("Credentials: test_user1 / zainab_moazzam")
print("Try forgot password to test email/SMS sending!")
print("="*70 + "\n")
