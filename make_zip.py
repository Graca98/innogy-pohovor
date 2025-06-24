import os
import zipfile

def zip_data_folder(zip_name="data_export.zip"):
    base_dir = "data"
    exclude_dir = os.path.join(base_dir, "metadata_archive")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Přeskočí podsložku metadata_archive
            if exclude_dir in root:
                continue
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, base_dir)
                zipf.write(abs_path, os.path.join("data", rel_path))

    print(f"[+] ZIP vytvořen: {zip_name}")

zip_data_folder()
