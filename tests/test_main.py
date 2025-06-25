import os
import tempfile
import threading
import http.server

from unittest.mock import MagicMock, patch # přepsání globální proměnné PDF_DIR
from functools import partial # custom directory pro http server
from selenium.webdriver.remote.webelement import WebElement
from main import (
    find_pdf_links,
    accept_cookies,
    take_screenshot,
    download_and_hash_pdfs,
    save_metadata,
)


#! Test: find_pdf_links najde odkazy na PDF
def test_find_pdf_links():
    # Simulace selenium webdriveru
    mock_driver = MagicMock()
    # Simulace HTML <a> elementu
    mock_element = MagicMock(spec=WebElement)
    # Když se zavolá get_attribute("href"), vrátí se tato testovací URL.
    mock_element.get_attribute.return_value = "https://example.com/test.pdf"
    # Když funkce zavolá find_elements(...), vrátí 1 prvek
    mock_driver.find_elements.return_value = [mock_element]

    # Spuštění funkce
    links = find_pdf_links(mock_driver)
    assert links == ["https://example.com/test.pdf"]


#! Test: accept_cookies klikne na tlačítko
# Nahradí WebDriverWait mockem - čekání netrvá 15s
@patch("main.WebDriverWait")
def test_accept_cookies_click(mock_wait):
    # Simulace tlačítka „Přijmout vše“
    mock_button = MagicMock()
    mock_wait.return_value.until.return_value = mock_button

    driver = MagicMock()
    accept_cookies(driver)
    mock_button.click.assert_called_once()


#! Test: take_screenshot vytvoří PNG soubor
def test_take_screenshot_creates_file():
    # Simulace Selenium WebDriveru
    class DummyDriver:
        # jen zapíše nějaká data, aby vznikl soubor
        def save_screenshot(self, path):
            with open(path, "wb") as f:
                f.write(b"fake image data")

    with tempfile.TemporaryDirectory() as tmpdir:
        global SCREENSHOT_DIR
        SCREENSHOT_DIR = tmpdir
        path = take_screenshot(DummyDriver(), "20240624")
        assert os.path.exists(path)
        assert path.endswith(".png")


#! Test: download_and_hash_pdfs stáhne a spočítá hash
def test_download_and_hash_pdfs():
    # vytvoří se obsah, který nasimulujeme jako jednoduchý PDF soubor
    test_pdf_content = b"%PDF-1.4 test content"

    # Dočasná složka (tmpdir) pro ukládání PDF
    with tempfile.TemporaryDirectory() as tmpdir:
        # Soubor test.pdf se uloží do tmpdir. Tento soubor se bude testovat
        test_pdf_path = os.path.join(tmpdir, "test.pdf")
        with open(test_pdf_path, "wb") as f:
            f.write(test_pdf_content)

        # Spustí se lokální HTTP server, který bude z tmpdir servírovat soubory.
        # partial, abych serveru řekl, kde hledat obsah
        handler = partial(http.server.SimpleHTTPRequestHandler, directory=tmpdir)
        server = http.server.HTTPServer(("localhost", 0), handler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        #  Pomocí patch se přesměruje globální PDF_DIR používaný ve funkci download_and_hash_pdfs() na tmpdir
        with patch("main.PDF_DIR", tmpdir):
            try:
                pdfs = download_and_hash_pdfs([f"http://localhost:{port}/test.pdf"])
                assert pdfs, "PDF list is empty!" # Byl nazalezen PDF
                assert pdfs[0]["file"] == "test.pdf" # Název sedí
                assert pdfs[0]["sha256"] # byl spočítán hash
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


#! Test: save_metadata vytvoří metadata.json i archiv
def test_save_metadata_creates_files():
    # dočasná složka pro uložení metadat.
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "metadata_archive"))

        # přepsání globální BASE_DIR používaný v save_metadata()
        with patch("main.BASE_DIR", tmpdir):
            # Připrava testovacího vstupu pro funkci save_metadata()
            timestamp = "20240624_150000"
            screenshot = "screenshot.png"
            pdfs = [{"file": "test.pdf", "url": "url", "path": "path", "sha256": "hash"}]

            save_metadata(timestamp, screenshot, pdfs)

            latest = os.path.join(tmpdir, "metadata.json")
            archive = os.path.join(tmpdir, "metadata_archive", f"metadata_{timestamp}.json")

            assert os.path.exists(latest)
            assert os.path.exists(archive)

