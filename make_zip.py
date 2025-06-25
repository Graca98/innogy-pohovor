import os
import zipfile
from datetime import datetime

def zip_data_folder():
    base_dir = "data"
    exclude_dir = os.path.join(base_dir, "metadata_archive")
    exclude_file = os.path.join(base_dir, "integrity_check.csv")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"data_export_{timestamp}.zip"

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            if exclude_dir in root:
                continue
            for file in files:
                abs_path = os.path.join(root, file)

                if os.path.abspath(abs_path) == os.path.abspath(exclude_file):
                    continue

                rel_path = os.path.relpath(abs_path, base_dir)
                zipf.write(abs_path, os.path.join("data", rel_path))

    print(f"[+] ZIP vytvořen: {zip_name}")

zip_data_folder()
