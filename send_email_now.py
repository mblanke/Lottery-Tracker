"""
Secure email sender that prompts for password instead of storing it.
This version is safer and works without App Passwords.
"""
import asyncio
from email_sender import (
    get_powerball,
    get_mega_millions,
    get_canadian_lotteries,
    create_email_html,
    format_currency
)
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

def send_email_secure(sender_email, sender_password, recipient_email, subject, html_content):
    """Send email with provided credentials"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Try Gmail first
        try:
            print("   Trying Gmail SMTP...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"✅ Email sent successfully via Gmail!")
            return True
        except Exception as gmail_error:
            print(f"   Gmail failed: {gmail_error}")
            
            # Try alternative method - Gmail SSL port
            try:
                print("   Trying Gmail SSL (port 465)...")
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                print(f"✅ Email sent successfully via Gmail SSL!")
                return True
            except Exception as ssl_error:
                print(f"   Gmail SSL also failed: {ssl_error}")
                raise
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print("\n⚠️  Common issues:")
        print("   1. Gmail requires 2-Step Verification + App Password")
        print("   2. Check if 'Less secure app access' is enabled (not recommended)")
        print("   3. Verify your email and password are correct")
        return False

def send_lottery_email():
    """Fetch jackpots and send email with secure password prompt"""
    print("\n" + "="*60)
    print("🎰 LOTTERY JACKPOT EMAIL SENDER")
    print("="*60)
    
    # Email configuration
    sender_email = "mblanke@gmail.com"
    recipient_email = "mblanke@gmail.com"
    
    print(f"\n📧 Email will be sent from/to: {sender_email}")
    print("\n🔐 Please enter your Gmail password:")
    print("    (Note: Gmail may require an App Password if you have 2FA enabled)")
    
    # Securely prompt for password (won't show on screen)
    sender_password = getpass.getpass("    Password: ")
    
    if not sender_password:
        print("❌ No password provided. Exiting.")
        return
    
    print("\n" + "-"*60)
    print("📊 Fetching lottery jackpots...")
    print("-"*60)
    
    # Get US lotteries
    print("\n🇺🇸 US Lotteries:")
    print("   Fetching Powerball...")
    powerball = get_powerball()
    print(f"   ✓ Powerball: {format_currency(powerball)}")
    
    print("   Fetching Mega Millions...")
    mega_millions = get_mega_millions()
    print(f"   ✓ Mega Millions: {format_currency(mega_millions)}")
    
    # Get Canadian lotteries
    print("\n🇨🇦 Canadian Lotteries:")
    print("   Fetching Lotto Max and Lotto 6/49...")
    lotto_max, lotto_649 = asyncio.run(get_canadian_lotteries())
    print(f"   ✓ Lotto Max: {format_currency(lotto_max)}")
    print(f"   ✓ Lotto 6/49: {format_currency(lotto_649)}")
    
    # Create email
    print("\n" + "-"*60)
    print("📧 Creating email...")
    print("-"*60)
    subject = f"🎰 Lottery Report - {datetime.now().strftime('%B %d, %Y')}"
    html_content = create_email_html(powerball, mega_millions, lotto_max, lotto_649)
    print("   ✓ Email content created")
    
    # Send email
    print("\n📤 Sending email...")
    success = send_email_secure(sender_email, sender_password, recipient_email, subject, html_content)
    
    if success:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"📧 Check your inbox at: {recipient_email}")
        print("💡 The email includes all current jackpot amounts")
        print("   with beautiful HTML formatting!")
    else:
        print("\n" + "="*60)
        print("❌ FAILED!")
        print("="*60)
        print("\n🔧 Options to fix:")
        print("   1. Enable 2-Step Verification in Gmail")
        print("   2. Generate App Password: https://myaccount.google.com/apppasswords")
        print("   3. Use the App Password instead of regular password")
        print("\n   Alternative: Use a different email service (Outlook, Yahoo, etc.)")
    
    print("\n")

if __name__ == "__main__":
    send_lottery_email()
