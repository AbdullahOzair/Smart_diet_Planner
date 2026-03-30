# Email Configuration Guide

## How to Set Up Email Sending

The Smart Diet Planner now sends beautiful, customized emails when users request password resets. Follow these steps to configure it:

---

## 🔧 Option 1: Using Gmail (Recommended for Quick Setup)

### Step 1: Enable 2-Factor Authentication on Gmail
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Create an **App Password** (different from your regular Gmail password):
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Window (Custom)"
   - Google will generate a 16-character password
   - Copy this password (you'll need it next)

### Step 2: Configure Environment Variables

Create a `.env` file in the `flask_app` folder with:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

Replace:
- `your-email@gmail.com` with your Gmail address
- `xxxx xxxx xxxx xxxx` with the 16-character App Password from Google

### Step 3: Load Environment Variables

On Windows (PowerShell):
```powershell
# Create .env in flask_app folder, then when running:
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USE_TLS="true"
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="xxxx xxxx xxxx xxxx"
python app.py
```

Or use a package like `python-dotenv`:
```bash
pip install python-dotenv
```

Then in `app.py` before creating the app:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🔧 Option 2: Using SendGrid (Best for Production)

### Step 1: Create SendGrid Account
1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Create an API key
3. Verify a sender email address

### Step 2: Configure Environment Variables

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-api-key-here
MAIL_DEFAULT_SENDER=verified-email@yourdomain.com
```

---

## 🔧 Option 3: Using Mailtrap (Best for Testing)

### Step 1: Create Mailtrap Account
1. Sign up at [mailtrap.io](https://mailtrap.io/home)
2. Create a project and inbox
3. Go to "Integrations" and select "Nodemailer"

### Step 2: Configure Environment Variables

```env
MAIL_SERVER=smtp.mailtrap.io
MAIL_PORT=465
MAIL_USE_TLS=false
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_DEFAULT_SENDER=hello@smartdiet.planner.test
```

---

## ✅ Verify Email Configuration

After configuring, test the setup:

1. Go to login page
2. Click "Forgot Password?"
3. Enter a username/email that exists
4. Check your email inbox
5. You should receive the beautiful password reset email!

---

## 🎨 What Users Receive

When a user requests a password reset, they'll receive a professional email with:

✅ **Custom Design**
- Modern gradient header
- Branded colors (Burnt Orange accent)
- Professional layout

✅ **Content Includes**
- Personalized greeting with user's first name
- 6-digit verification code in a prominent box
- Clear step-by-step instructions
- Security notice for safety
- Recovery method shown
- Links to dashboard and help

✅ **Interactive Elements**
- "Go to Password Reset" button
- Action links in footer
- Professional footer with app info

---

## 🚀 Install Flask-Mail

If you haven't installed Flask-Mail yet:

```bash
pip install Flask-Mail
```

Or update from requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 📱 SMS Setup (Optional)

For SMS code delivery, you'll need Twilio:

### Step 1: Create Twilio Account
1. Sign up at [twilio.com](https://twilio.com)
2. Get your Account SID and Auth Token
3. Verify or buy a phone number

### Step 2: Install Twilio SDK
```bash
pip install twilio
```

### Step 3: Update app.py
In the `send_verification_code` function, uncomment and configure:

```python
from twilio.rest import Client

elif recovery_method == 'phone':
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your Smart Diet Planner verification code is: {code}. Valid for 10 minutes.',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return True
```

---

## ⚠️ Troubleshooting

### Email not sending?

**Error: "SMTPAuthenticationError"**
- ✅ Check MAIL_USERNAME and MAIL_PASSWORD are correct
- ✅ For Gmail: Ensure you're using an App Password, not regular password
- ✅ For SendGrid: Ensure MAIL_USERNAME is "apikey"

**Error: "SMTPException"**
- ✅ Check MAIL_SERVER and MAIL_PORT
- ✅ Verify internet connection
- ✅ Check firewall/network settings

**Email goes to spam?**
- ✅ Add sender email to contacts
- ✅ Move email from spam to inbox and mark as "not spam"
- ✅ For production: Set up SPF, DKIM, DMAR records

### Code not visible in terminal?

When Flask-Mail is configured, the Flask console won't show the code anymore. Instead:
- Check your actual email inbox
- If testing, use Mailtrap to preview emails

---

## 🔒 Production Checklist

- [ ] Use a professional domain email (not @gmail.com)
- [ ] Set up SPF and DKIM records with email provider
- [ ] Use SendGrid or similar service (not Gmail)
- [ ] Add HTTPS/SSL certificate
- [ ] Set `SESSION_COOKIE_SECURE = True` in app.py
- [ ] Store sensitive data in environment variables
- [ ] Never commit `.env` file to version control
- [ ] Test email sending with real user emails
- [ ] Monitor email delivery reports
- [ ] Set up backup email provider

---

## 📝 Environment Variables Summary

Create a `.env` file with:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Optional: SMS Configuration
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Database Configuration
PG_HOST=localhost
PG_PORT=5000
PG_DATABASE=smart_diet_planner
PG_USER=postgres
PG_PASSWORD=zainab
```

---

## 📞 Support

For issues:
1. Check Flask server console for error messages
2. Verify email credentials are correct
3. Test with a different email service
4. Check internet connection
5. Review email provider's documentation

---

**Email Integration Version**: 1.0
**Last Updated**: March 26, 2026
**Status**: ✅ Ready for Configuration
