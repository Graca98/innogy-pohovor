import os
import hashlib
import json
import glob
import csv
from datetime import datetime

BASE_DIR = "data"
ARCHIVE_DIR = os.path.join(BASE_DIR, "metadata_archive")
CURRENT_METADATA = os.path.join(BASE_DIR, "metadata.json")
PDF_DIR = os.path.join(BASE_DIR, "pdfs")
CSV_FILE = os.path.join(BASE_DIR, "integrity_check.csv")

def load_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def file_exists_and_hash_matches(file_path, expected_hash):
    if not os.path.exists(file_path):
        return "❌ Soubor chybí"
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    current_hash = sha256.hexdigest()
    return "✅ Beze změn" if current_hash == expected_hash else "⚠️ Změněn"

def compare_metadata(current, previous, timestamp):
    current_pdfs = {pdf["file"]: pdf for pdf in current.get("pdfs", [])}
    previous_pdfs = {pdf["file"]: pdf for pdf in previous.get("pdfs", [])}

    all_files = sorted(set(current_pdfs) | set(previous_pdfs))
    changes = []

    print(f"\n📄 Porovnání metadat a fyzických souborů:\n{'Soubor':<40} | Stav")
    print("-" * 60)

    for file in all_files:
        curr = current_pdfs.get(file)
        prev = previous_pdfs.get(file)

        if curr and prev:
            expected_hash = prev["sha256"]
            status = file_exists_and_hash_matches(curr["path"], expected_hash)
        elif curr and not prev:
            status = "➕ Nový soubor"
        elif prev and not curr:
            status = "➖ Odstraněn z metadat"
        else:
            status = "❓ Neznámý stav"

        changes.append({
            "timestamp": timestamp,
            "file": file,
            "status": status
        })

        print(f"{file:<40} | {status}")

    return changes

def write_csv_log(results):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "file", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in results:
            writer.writerow(row)

def find_previous_metadata():
    archive_files = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "metadata_*.json")))
    if len(archive_files) < 2:
        return None
    return archive_files[-2]  # Předposlední archivní verze

def main():
    if not os.path.exists(CURRENT_METADATA):
        print("❌ metadata.json nebyl nalezen.")
        return

    previous_file = find_previous_metadata()
    if not previous_file:
        print("❌ Není dostatek archivních souborů pro porovnání.")
        return

    current_data = load_metadata(CURRENT_METADATA)
    previous_data = load_metadata(previous_file)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"🆚 Porovnání aktuální verze s: {os.path.basename(previous_file)}")
    results = compare_metadata(current_data, previous_data, timestamp)
    write_csv_log(results)

main()
