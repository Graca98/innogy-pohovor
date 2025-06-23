# 📥 PDF Web Scraper pro Innogy.cz

## 🧩 Schéma navrhovaného řešení

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

## 🧩 Popis řešení

Tento Python skript automatizuje proces:

1. Otevření webové stránky Innogy s obchodními podmínkami
2. Automatického přijetí cookie banneru
3. Vyfocení aktuální podoby stránky (screenshot)
4. Vyhledání a stažení všech PDF dokumentů z dané stránky
5. Výpočtu SHA256 hashů PDF souborů pro kontrolu integrity
6. Uložení metadat:
   - `metadata.json` – aktuální stav
   - `metadata_archive/metadata_YYYYMMDD_HHMMSS.json` – historický záznam
7. Možnost zpětné kontroly změn v PDF (kontrola integrity)

---

## 🛠 Použité technologie

- **Python 3.10+**
- `selenium` + `webdriver_manager` – pro práci s prohlížečem
- `requests` – pro stahování PDF
- `hashlib` – výpočet SHA256
- `json`, `csv`, `os`, `time`, `datetime`

---

## ⚙️ Spuštění

```bash
python main.py
