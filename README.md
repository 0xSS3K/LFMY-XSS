# LFMY-XSS
LFM-XSS is a semi-automated, interactive Python tool designed for hunting stored Cross-Site Scripting vulnerabilities. It leverages a stealth-configured Selenium WebDriver to crawl websites, manage authenticated sessions via JSON cookies, manual bypass WAF and CAPTCHA challenges through "human-in-the-loop" approach. The tool features a dual-detection mechanism, identifying vulnerabilities by both finding the reflected payload in the HTML source and by detecting successful JavaScript execution via pop-up alerts. Its interactive workflow allows the user to pause and resume the scan, providing full control during a security assessment.

# Installation Guide
### Prerequisites
Before you begin, ensure you have the following installed on your system:

- Python 3.8 or higher.
- Git for cloning the source code.
- Google Chrome or Chromium web browser.

### Installation Steps

1. Clone the Repository
   
Open your terminal, and run the following command to download the project:
```bash
git clone https://github.com/0xSS3K/LFMY-XSS
```

2. Next, navigate into the project directory:
```Bash
cd LFMY-XSS
```

### Create and Activate a Virtual Environment

3. It is highly recommended to use a virtual environment to keep the project's dependencies isolated from your global system.

Create the environment:
```Bash
python -m venv venv
```

4. Activate the environment:

On Linux or macOS:
```Bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

You will see a ```(venv)``` prefix in your terminal prompt, indicating that the environment is active.

5. Install Required Dependencies

This project uses a requirements.txt file to manage all necessary Python libraries. Install them all with a single command:
```Bash
pip install -r requirements.txt
```

This will automatically install selenium, beautifulsoup4, colorama, lxml, and selenium-stealth.

6. Just do
```Bash
python lfmyxss.py
```
