# 📥 PDF Web Scraper pro Innogy.cz

Tento Python skript automatizuje stahování PDF dokumentů, jejich archivaci a sledování integrity z webu Innogy.

## 🧩 Popis řešení

1. Otevření webové stránky Innogy s obchodními podmínkami  
2. Automatické přijetí cookie banneru  
3. Vyfocení aktuální podoby stránky (screenshot)  
4. Vyhledání a stažení všech PDF dokumentů z dané stránky  
5. Výpočet SHA256 hashů PDF souborů pro kontrolu integrity  
6. Uložení metadat:  
   - `metadata.json` – aktuální stav  
   - `metadata_archive/metadata_YYYYMMDD_HHMMSS.json` – historický záznam  
7. Možnost zpětné kontroly změn v PDF (kontrola integrity)

## 🔄 Schéma navrhovaného řešení
```
[Python skript]
    ↓
[Otevření webu přes Selenium]
    ↓
[Přijetí cookies → Screenshot]
    ↓
[Nalezení PDF → Stažení PDF]
    ↓
[Výpočet hashů]
    ↓
[Uložení metadat do JSON + archiv]
 ```

---

## 🛠 Použité technologie

- **Python 3.10+**
- `selenium` + `webdriver_manager` – pro práci s prohlížečem
- `requests` – pro stahování PDF
- `hashlib` – výpočet SHA256
- `json`, `csv`, `os`, `time`, `datetime`

---

## ⚙️ Spuštění projektu

```bash
# Instalace závislostí
pip install -r requirements.txt

# Spuštění hlavního skriptu
python main.py

# Spuštění testů
python -m pytest tests/

# Spuštění kontroly integrity
python check_integrity.py

# ZIP složky data (bez složky metadata_archive)
python make_zip.py
```

---

## 📂 Výstupy

- `data/pdfs/` – stažené PDF dokumenty
- `data/screenshots/` – screenshoty stránek
- `data/metadata.json` – aktuální metadata
- `data/metadata_archive/` – archivní historie metadat
- `data/integrity_check.csv` – log porovnání změn

## 🧪 Pokrytí testy

- `tests/test_main.py` pokrývá:
  - hledání PDF
  - přijímání cookies
  - screenshot
  - stahování + hash
  - uložení metadat

---

## 📄 Doplňující dokumenty

- [⏱️ Odhad časové náročnosti](Odhad_prace.md)
- [📊 Odhad provozního modelu](Odhad_provozniho_modelu.md)