"""
Flask Backend for Lottery Investment Calculator
Provides API endpoints for jackpots and investment calculations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import urllib3
from playwright.sync_api import sync_playwright
import re
from lottery_calculator import calculate_us_lottery, calculate_canadian_lottery

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Common headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}


def get_us_lotteries():
    """Fetch Powerball and Mega Millions jackpots"""
    results = {"Powerball": None, "Mega Millions": None}
    
    # Powerball
    try:
        resp = requests.get("https://www.lotto.net/powerball", timeout=10, verify=False, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    # Extract numeric value
                    match = re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', next_line)
                    if match:
                        value = float(match.group(1).replace(',', ''))
                        results["Powerball"] = value * 1_000_000
                    break
    except Exception as e:
        print(f"Error fetching Powerball: {e}")
    
    # Mega Millions
    try:
        resp = requests.get("https://www.lotto.net/mega-millions", timeout=10, verify=False, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    # Extract numeric value
                    match = re.search(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', next_line)
                    if match:
                        value = float(match.group(1).replace(',', ''))
                        results["Mega Millions"] = value * 1_000_000
                    break
    except Exception as e:
        print(f"Error fetching Mega Millions: {e}")
    
    return results


def get_canadian_lotteries():
    """Fetch Lotto Max and Lotto 6/49 jackpots using Playwright"""
    results = {"Lotto Max": None, "Lotto 6/49": None}
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.olg.ca/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()
            
            # Lotto Max
            lotto_max_match = re.search(r'LOTTO\s*MAX(?:(?!LOTTO\s*6/49).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if lotto_max_match:
                value = float(lotto_max_match.group(1).replace(',', ''))
                results["Lotto Max"] = value * 1_000_000
            
            # Lotto 6/49
            lotto_649_match = re.search(r'LOTTO\s*6/49(?:(?!LOTTO\s*MAX).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if lotto_649_match:
                value = float(lotto_649_match.group(1).replace(',', ''))
                results["Lotto 6/49"] = value * 1_000_000
    except Exception as e:
        print(f"Error fetching Canadian lotteries: {e}")
    
    return results


@app.route('/api/jackpots', methods=['GET'])
def get_jackpots():
    """API endpoint to get all lottery jackpots"""
    us_lotteries = get_us_lotteries()
    canadian_lotteries = get_canadian_lotteries()
    
    return jsonify({
        "us": {
            "powerball": us_lotteries["Powerball"],
            "megaMillions": us_lotteries["Mega Millions"]
        },
        "canadian": {
            "lottoMax": canadian_lotteries["Lotto Max"],
            "lotto649": canadian_lotteries["Lotto 6/49"]
        }
    })


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint to calculate investment returns"""
    data = request.json
    
    jackpot = data.get('jackpot')
    lottery_type = data.get('type', 'us')  # 'us' or 'canadian'
    invest_percentage = data.get('investPercentage', 0.90)
    annual_return = data.get('annualReturn', 0.045)
    cycles = data.get('cycles', 8)
    
    if not jackpot:
        return jsonify({"error": "Jackpot amount is required"}), 400
    
    try:
        if lottery_type == 'us':
            result = calculate_us_lottery(jackpot, invest_percentage, annual_return, cycles)
        else:
            result = calculate_canadian_lottery(jackpot, invest_percentage, annual_return, cycles)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("🎰 Lottery Investment Calculator API")
    print("=" * 50)
    print("Starting Flask server on http://localhost:5000")
    print("API Endpoints:")
    print("  - GET  /api/jackpots   - Get current jackpots")
    print("  - POST /api/calculate  - Calculate investments")
    print("  - GET  /api/health     - Health check")
    print("=" * 50)
    # Bind to 0.0.0.0 so the Flask app is reachable from outside the container
    app.run(debug=True, host='0.0.0.0', port=5000)
