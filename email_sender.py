import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright
import requests
from bs4 import BeautifulSoup
import urllib3
import re

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change this for your email provider
    'smtp_port': 587,
    'sender_email': 'mblanke@gmail.com',  # Replace with your email
    'sender_password': 'vyapvyjjfrqpqnax',  # App password (spaces removed)
    'recipient_email': 'mblanke@gmail.com',  # Replace with recipient email
}

# Common headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Scraping functions
def get_powerball():
    """Get Powerball jackpot from lotto.net"""
    try:
        url = "https://www.lotto.net/powerball"
        response = requests.get(url, timeout=10, verify=False, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for "Next Jackpot" text
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    # Parse the amount
                    match = re.search(r'\$\s*([\d,]+(?:\.\d+)?)\s*Million', next_line)
                    if match:
                        amount_str = match.group(1).replace(',', '')
                        return float(amount_str)
    except Exception as e:
        print(f"Error getting Powerball: {e}")
    return None

def get_mega_millions():
    """Get Mega Millions jackpot from lotto.net"""
    try:
        url = "https://www.lotto.net/mega-millions"
        response = requests.get(url, timeout=10, verify=False, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for "Next Jackpot" text
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    # Parse the amount
                    match = re.search(r'\$\s*([\d,]+(?:\.\d+)?)\s*Million', next_line)
                    if match:
                        amount_str = match.group(1).replace(',', '')
                        return float(amount_str)
    except Exception as e:
        print(f"Error getting Mega Millions: {e}")
    return None

async def get_canadian_lotteries():
    """Get Lotto Max and Lotto 6/49 jackpots using Playwright"""
    lotto_max = None
    lotto_649 = None
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto('https://www.olg.ca/', wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            
            # Lotto Max pattern
            lotto_max_pattern = r'LOTTO\s*MAX(?:(?!LOTTO\s*6/49).)*?\$\s*([\d.,]+)\s*Million'
            match = re.search(lotto_max_pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                amount_str = match.group(1).replace(',', '')
                lotto_max = float(amount_str)
            
            # Lotto 6/49 pattern
            lotto_649_pattern = r'LOTTO\s*6/49.*?\$\s*([\d.,]+)\s*Million'
            match = re.search(lotto_649_pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                amount_str = match.group(1).replace(',', '')
                lotto_649 = float(amount_str)
            
            await browser.close()
    except Exception as e:
        print(f"Error getting Canadian lotteries: {e}")
    
    return lotto_max, lotto_649

def format_currency(amount):
    """Format amount as currency"""
    if amount is None:
        return "Not available"
    return f"${amount:,.0f}M"

def create_email_html(powerball, mega_millions, lotto_max, lotto_649):
    """Create HTML email content"""
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                max-width: 600px;
                margin: 0 auto;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
            }}
            .lottery-section {{
                margin-bottom: 30px;
            }}
            .lottery-section h2 {{
                color: #34495e;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }}
            .lottery-item {{
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .lottery-name {{
                font-weight: bold;
                color: #2c3e50;
                font-size: 16px;
            }}
            .lottery-amount {{
                font-size: 24px;
                font-weight: bold;
                color: #27ae60;
            }}
            .tax-free {{
                background-color: #2ecc71;
                color: white;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 10px;
                margin-left: 10px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
                color: #7f8c8d;
                font-size: 12px;
            }}
            .timestamp {{
                color: #95a5a6;
                font-size: 12px;
                text-align: center;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎰 Daily Lottery Jackpots</h1>
            
            <div class="lottery-section">
                <h2>🇺🇸 US Lotteries</h2>
                <div class="lottery-item">
                    <div>
                        <span class="lottery-name">Powerball</span>
                    </div>
                    <span class="lottery-amount">{format_currency(powerball)}</span>
                </div>
                <div class="lottery-item">
                    <div>
                        <span class="lottery-name">Mega Millions</span>
                    </div>
                    <span class="lottery-amount">{format_currency(mega_millions)}</span>
                </div>
            </div>
            
            <div class="lottery-section">
                <h2>🇨🇦 Canadian Lotteries</h2>
                <div class="lottery-item">
                    <div>
                        <span class="lottery-name">Lotto Max</span>
                        <span class="tax-free">TAX FREE</span>
                    </div>
                    <span class="lottery-amount">{format_currency(lotto_max)}</span>
                </div>
                <div class="lottery-item">
                    <div>
                        <span class="lottery-name">Lotto 6/49</span>
                        <span class="tax-free">TAX FREE</span>
                    </div>
                    <span class="lottery-amount">{format_currency(lotto_649)}</span>
                </div>
            </div>
            
            <div class="footer">
                <p>💡 Remember: Canadian lottery winnings are tax-free!</p>
                <p>📊 Visit your Lottery Investment Calculator for detailed analysis</p>
            </div>
            
            <div class="timestamp">
                Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email(subject, html_content):
    """Send email with jackpot information"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        
        print(f"✅ Email sent successfully at {datetime.now().strftime('%I:%M %p')}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def send_daily_jackpots():
    """Fetch jackpots and send email"""
    print(f"\n{'='*50}")
    print(f"🎰 Fetching lottery jackpots at {datetime.now().strftime('%I:%M %p')}")
    print(f"{'='*50}")
    
    # Get US lotteries
    print("📊 Fetching Powerball...")
    powerball = get_powerball()
    print(f"   Powerball: {format_currency(powerball)}")
    
    print("📊 Fetching Mega Millions...")
    mega_millions = get_mega_millions()
    print(f"   Mega Millions: {format_currency(mega_millions)}")
    
    # Get Canadian lotteries
    print("📊 Fetching Canadian lotteries...")
    lotto_max, lotto_649 = asyncio.run(get_canadian_lotteries())
    print(f"   Lotto Max: {format_currency(lotto_max)}")
    print(f"   Lotto 6/49: {format_currency(lotto_649)}")
    
    # Create email content
    subject = f"🎰 Daily Lottery Report - {datetime.now().strftime('%B %d, %Y')}"
    html_content = create_email_html(powerball, mega_millions, lotto_max, lotto_649)
    
    # Send email
    print("\n📧 Sending email...")
    send_email(subject, html_content)
    print(f"{'='*50}\n")

def main():
    """Main function to schedule and run the email sender"""
    print("🚀 Lottery Jackpot Email Scheduler Started")
    print("=" * 50)
    print(f"📧 Emails will be sent to: {EMAIL_CONFIG['recipient_email']}")
    print(f"⏰ Scheduled time: 7:00 AM daily")
    print(f"🔄 Current time: {datetime.now().strftime('%I:%M %p')}")
    print("=" * 50)
    print("\nPress Ctrl+C to stop the scheduler\n")
    
    # Schedule the job for 7:00 AM every day
    schedule.every().day.at("07:00").do(send_daily_jackpots)
    
    # Optional: Uncomment to send immediately for testing
    # print("🧪 Sending test email now...")
    # send_daily_jackpots()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
