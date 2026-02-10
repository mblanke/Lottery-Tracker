"""
Quick test script to send a lottery jackpot email immediately.
Use this to verify your email configuration before scheduling.
"""
import asyncio
from email_sender import (
    get_powerball,
    get_mega_millions,
    get_canadian_lotteries,
    create_email_html,
    send_email,
    format_currency,
    EMAIL_CONFIG
)
from datetime import datetime

def test_email():
    """Test the email sender by sending immediately"""
    print("\n" + "="*60)
    print("🧪 TESTING LOTTERY EMAIL SENDER")
    print("="*60)
    
    # Display current configuration
    print(f"\n📧 Email Configuration:")
    print(f"   From: {EMAIL_CONFIG['sender_email']}")
    print(f"   To: {EMAIL_CONFIG['recipient_email']}")
    print(f"   SMTP Server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
    
    if EMAIL_CONFIG['sender_email'] == 'your-email@gmail.com':
        print("\n⚠️  WARNING: You need to update EMAIL_CONFIG in email_sender.py!")
        print("   Please edit the file and add your email credentials.")
        print("   See EMAIL_SETUP.md for instructions.")
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
    subject = f"🎰 TEST - Lottery Report - {datetime.now().strftime('%B %d, %Y')}"
    html_content = create_email_html(powerball, mega_millions, lotto_max, lotto_649)
    print("   ✓ Email content created")
    
    # Send email
    print("\n📤 Sending email...")
    success = send_email(subject, html_content)
    
    if success:
        print("\n" + "="*60)
        print("✅ TEST SUCCESSFUL!")
        print("="*60)
        print(f"📧 Check your inbox at: {EMAIL_CONFIG['recipient_email']}")
        print("💡 If everything looks good, you can run email_sender.py")
        print("   to schedule daily emails at 7:00 AM")
    else:
        print("\n" + "="*60)
        print("❌ TEST FAILED!")
        print("="*60)
        print("🔍 Troubleshooting tips:")
        print("   1. Check your email and password in EMAIL_CONFIG")
        print("   2. For Gmail, use an App Password (not your regular password)")
        print("   3. Verify SMTP server and port are correct")
        print("   4. Check your internet connection")
        print("   5. See EMAIL_SETUP.md for detailed instructions")
    
    print("\n")

if __name__ == "__main__":
    test_email()
