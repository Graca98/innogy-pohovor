from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time
import requests
import hashlib
import json
from datetime import datetime
from PIL import Image

# ------------------- NASTAVENÍ ------------------- #
URL = "https://www.innogy.cz/kampan/nove-obchodni-podminky/"
BASE_DIR = "data"
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
METADATA_FILE = os.path.join(BASE_DIR, "metadata.json")
CHROME_DRIVER_PATH = "./webdriver/chromedriver"

# ------------------- PŘÍPRAVA ------------------- #
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ------------------- SELENIUM ------------------- #
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(URL)
time.sleep(5) 

try:
    print("[*] Pokus o klasické kliknutí na cookies tlačítko...")
    button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
    )
    button.click()
    print("[+] Cookies byly kliknuty normálně.")
    time.sleep(2)
except Exception as e:
    print("[-] Cookies tlačítko se nepodařilo najít nebo kliknout:", e)

# ------------------- SCREENSHOT ------------------- #
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
driver.save_screenshot(screenshot_path)
print(f"[+] Screenshot uložen do: {screenshot_path}")

# ------------------- PDF ODKAZY ------------------- #
pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
pdf_urls = [a.get_attribute("href") for a in pdf_links]
driver.quit()

# ------------------- STAHOVÁNÍ PDF + HASH ------------------- #
metadata = {"timestamp": timestamp, "pdfs": [], "screenshot": screenshot_path}

for url in pdf_urls:
    file_name = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(PDF_DIR, file_name)
    
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)

    # Vypočítáme SHA256
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    metadata["pdfs"].append({
        "file": file_name,
        "url": url,
        "path": file_path,
        "sha256": sha256_hash.hexdigest()
    })

    print(f"[+] Staženo: {file_name} ({sha256_hash.hexdigest()[:10]}...)")

# ------------------- ULOŽENÍ METADAT ------------------- #
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)
print(f"[+] Metadata uložena do: {METADATA_FILE}")
