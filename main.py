from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
import os
import requests
import time
import hashlib
import json

#! ------------------- CESTY ------------------- #
URL = "https://www.innogy.cz/kampan/nove-obchodni-podminky/"
BASE_DIR = "data"
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

#! ------------------- FUNKCE ------------------- #

def setup_directories():
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "metadata_archive"), exist_ok=True)

def init_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def accept_cookies(driver):
    try:
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        time.sleep(2)
        button.click()
        print("[+] Cookies byly odkliknuty")
    except Exception as e:
        print("[-] Cookies tlačítko se nepodařilo najít nebo kliknout:", e)

def take_screenshot(driver, timestamp):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    print(f"[+] Screenshot uložen do: {screenshot_path}")
    return screenshot_path

def find_pdf_links(driver):
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
    return [link.get_attribute("href") for link in links]

def init_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def download_and_hash_pdfs(urls):
    pdf_info = []
    session = init_session()

    for url in urls:
        file_name = url.split("/")[-1].split("?")[0]
        file_path = os.path.join(PDF_DIR, file_name)

        try:
            r = session.get(url, timeout=10)
            r.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(r.content)

            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)

            pdf_info.append({
                "file": file_name,
                "url": url,
                "path": file_path,
                "sha256": sha256.hexdigest()
            })

            print(f"[+] Staženo: {file_name} ({sha256.hexdigest()[:10]}...)")

        except Exception as e:
            print(f"[-] Chyba při stahování {url}:", e)

    return pdf_info


def save_metadata(timestamp, screenshot_path, pdfs):
    metadata = {
        "timestamp": timestamp,
        "screenshot": screenshot_path,
        "pdfs": pdfs
    }

    # Uloží aktuální metadata.json (přepisuje se)
    latest_metadata_path = os.path.join(BASE_DIR, "metadata.json")
    with open(latest_metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    # Uloží archivní verzi s timestampem
    archive_path = os.path.join(BASE_DIR, "metadata_archive", f"metadata_{timestamp}.json")
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"[+] Metadata uložena do:\n- {latest_metadata_path}\n- {archive_path}")

#! ------------------- HLAVNÍ BĚH ------------------- #

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    setup_directories()
    driver = init_driver()
    driver.get(URL)

    accept_cookies(driver)
    screenshot_path = take_screenshot(driver, timestamp)
    pdf_urls = find_pdf_links(driver)
    driver.quit()

    pdfs = download_and_hash_pdfs(pdf_urls)
    save_metadata(timestamp, screenshot_path, pdfs)

if __name__ == "__main__":
    main()
