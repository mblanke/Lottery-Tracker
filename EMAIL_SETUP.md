# Email Configuration for Lottery Jackpot Alerts

## Setup Instructions

### 1. Install Required Package
```bash
pip install schedule
```

### 2. Configure Email Settings

Edit `email_sender.py` and update the `EMAIL_CONFIG` section:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Your email provider's SMTP server
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',  # Your email address
    'sender_password': 'your-app-password',  # Your app-specific password
    'recipient_email': 'recipient@example.com',  # Where to send the report
}
```

### 3. Email Provider Settings

#### For Gmail:
1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
   - Use this password in `sender_password` (NOT your regular Gmail password)
3. SMTP Settings:
   - Server: `smtp.gmail.com`
   - Port: `587`

#### For Outlook/Hotmail:
- Server: `smtp-mail.outlook.com`
- Port: `587`
- Use your regular email and password

#### For Yahoo:
- Server: `smtp.mail.yahoo.com`
- Port: `587`
- Generate app password at: https://login.yahoo.com/account/security

#### For Other Providers:
Search for "[Your Provider] SMTP settings" to find the correct server and port.

### 4. Test the Email

Uncomment this line in the `main()` function to send a test email immediately:
```python
send_daily_jackpots()
```

Then run:
```bash
python email_sender.py
```

### 5. Schedule Daily Emails

The script is configured to send emails at **7:00 AM** every day.

To run it continuously:
```bash
python email_sender.py
```

Keep the terminal window open. The script will:
- Wait until 7:00 AM
- Fetch current jackpots
- Send formatted email
- Repeat daily

### 6. Run as Background Service (Optional)

#### Windows - Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Lottery Jackpot Email"
4. Trigger: Daily at 7:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `d:\Projects\Dev\Lottery\email_sender.py`
6. Finish

#### Windows - NSSM (Non-Sucking Service Manager):
```bash
# Install NSSM
choco install nssm

# Create service
nssm install LotteryEmail python d:\Projects\Dev\Lottery\email_sender.py

# Start service
nssm start LotteryEmail
```

#### Linux - Cron Job:
```bash
# Edit crontab
crontab -e

# Add this line (runs at 7:00 AM daily)
0 7 * * * /usr/bin/python3 /path/to/email_sender.py
```

#### Linux - systemd service:
Create `/etc/systemd/system/lottery-email.service`:
```ini
[Unit]
Description=Lottery Jackpot Email Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Lottery
ExecStart=/usr/bin/python3 /path/to/email_sender.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable lottery-email
sudo systemctl start lottery-email
```

## Email Features

The automated email includes:
- 🎰 **Powerball** jackpot (US)
- 🎰 **Mega Millions** jackpot (US)
- 🎰 **Lotto Max** jackpot (Canada - TAX FREE!)
- 🎰 **Lotto 6/49** jackpot (Canada - TAX FREE!)
- 📅 **Timestamp** of when data was fetched
- 💡 **Reminder** about Canadian tax-free winnings
- 🎨 **Beautiful HTML formatting** with colors and styling

## Customization

### Change Send Time:
Edit this line in `email_sender.py`:
```python
schedule.every().day.at("07:00").do(send_daily_jackpots)
```

Examples:
- `"09:30"` - 9:30 AM
- `"18:00"` - 6:00 PM
- `"00:00"` - Midnight

### Send to Multiple Recipients:
Change the `send_email()` function:
```python
msg['To'] = "email1@example.com, email2@example.com, email3@example.com"
```

### Send Multiple Times Per Day:
Add multiple schedule lines:
```python
schedule.every().day.at("07:00").do(send_daily_jackpots)
schedule.every().day.at("19:00").do(send_daily_jackpots)
```

## Troubleshooting

### "Authentication failed":
- Make sure you're using an **app password**, not your regular password (for Gmail)
- Check that 2FA is enabled on your account
- Verify SMTP server and port are correct

### "Connection refused":
- Check your firewall settings
- Verify SMTP port is correct (usually 587 or 465)
- Try port 465 with `SMTP_SSL` instead of `SMTP` with `starttls()`

### Script stops running:
- Check if your computer went to sleep
- Use Task Scheduler or systemd to auto-restart
- Check logs for error messages

### Jackpots not updating:
- Websites may have changed their HTML structure
- Check if Playwright browser is installed: `playwright install chromium`
- Test the scraper functions individually

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit `email_sender.py` with your real credentials to Git
- Use environment variables for sensitive data in production
- Keep your app password secure
- Don't share your app password with anyone

## Support

If you encounter issues:
1. Run the test email first to verify configuration
2. Check error messages in the console
3. Verify internet connection
4. Confirm email provider settings
5. Test scraping functions individually
