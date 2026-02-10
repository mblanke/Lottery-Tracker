import requests
from bs4 import BeautifulSoup
import urllib3
from playwright.sync_api import sync_playwright
import re

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def get_powerball():
    url = "https://www.lotto.net/powerball"
    try:
        resp = requests.get(url, timeout=10, verify=False, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Look for divs containing "Next Jackpot" and "$XXX Million"
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    return next_line
        return "Not found"
    except Exception as e:
        return f"Error: {e}"

def get_mega_millions():
    url = "https://www.lotto.net/mega-millions"
    try:
        resp = requests.get(url, timeout=10, verify=False, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Look for divs containing "Next Jackpot" and "$XXX Million"
        all_text = soup.get_text()
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Next Jackpot' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '$' in next_line and 'Million' in next_line:
                    return next_line
        return "Not found"
    except Exception as e:
        return f"Error: {e}"

def get_lotto_max():
    url = "https://www.olg.ca/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait for lottery content to load
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()
            
            # Search for Lotto Max jackpot - look for the pattern more carefully
            # Match "LOTTO MAX" followed by jackpot info, avoiding 649
            match = re.search(r'LOTTO\s*MAX(?:(?!LOTTO\s*6/49).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if match:
                return f"${match.group(1)} Million"
            return "Not found"
    except Exception as e:
        return f"Error: {e}"

def get_lotto_649():
    url = "https://www.olg.ca/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait for lottery content to load
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()
            
            # Search for Lotto 6/49 jackpot - be more specific
            match = re.search(r'LOTTO\s*6/49(?:(?!LOTTO\s*MAX).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if match:
                return f"${match.group(1)} Million"
            return "Not found"
    except Exception as e:
        return f"Error: {e}"

def get_olg_lotteries():
    """
    Fetches jackpot amounts for Lotto Max and Lotto 6/49 from OLG website using Playwright.
    Returns a dict with keys 'Lotto Max' and 'Lotto 6/49'.
    """
    url = "https://www.olg.ca/"
    results = {"Lotto Max": "Not found", "Lotto 6/49": "Not found"}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            # Wait for lottery content to load
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()
            
            # Lotto Max - be more specific to avoid 649
            lotto_max_match = re.search(r'LOTTO\s*MAX(?:(?!LOTTO\s*6/49).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if lotto_max_match:
                results["Lotto Max"] = f"${lotto_max_match.group(1)} Million"
            
            # Lotto 6/49 - be more specific to avoid MAX
            lotto_649_match = re.search(r'LOTTO\s*6/49(?:(?!LOTTO\s*MAX).)*?\$\s*([\d.,]+)\s*Million', content, re.IGNORECASE | re.DOTALL)
            if lotto_649_match:
                results["Lotto 6/49"] = f"${lotto_649_match.group(1)} Million"
    except Exception as e:
        results = {"Lotto Max": f"Error: {e}", "Lotto 6/49": f"Error: {e}"}
    return results

def get_lottery_usa():
    """
    Fetches jackpot amounts for Powerball and Mega Millions from lotto.net.
    Returns a dict with keys 'Powerball' and 'Mega Millions'.
    """
    results = {"Powerball": "Not found", "Mega Millions": "Not found"}
    
    # Get Powerball
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
                    results["Powerball"] = next_line
                    break
    except Exception as e:
        results["Powerball"] = f"Error: {e}"
    
    # Get Mega Millions
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
                    results["Mega Millions"] = next_line
                    break
    except Exception as e:
        results["Mega Millions"] = f"Error: {e}"
    
    return results

if __name__ == "__main__":
    print("🎰 Current Lottery Jackpots")
    print("------------------------------")
    print(f"Powerball:     {get_powerball()}")
    print(f"Mega Millions: {get_mega_millions()}")
    print(f"Lotto Max:     {get_lotto_max()}")
    print(f"Lotto 6/49:    {get_lotto_649()}")
    # Add OLG results as fallback/alternative
    olg = get_olg_lotteries()
    print(f"OLG Lotto Max: {olg['Lotto Max']}")
    print(f"OLG Lotto 6/49: {olg['Lotto 6/49']}")
    # Add Lottery USA results
    lottery_usa = get_lottery_usa()
    print(f"Lottery USA Powerball: {lottery_usa['Powerball']}")
    print(f"Lottery USA Mega Millions: {lottery_usa['Mega Millions']}")
