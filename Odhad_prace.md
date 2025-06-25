# ⏳ Odhad časové náročnosti

Odhadovaný čas potřebný na vývoj funkčního řešení zahrnující jednotlivé fáze:

| Fáze                                       | Popis                                                                 | Odhad času |
|-------------------------------------------|-----------------------------------------------------------------------|------------|
| 1. Analýza zadání a návrh řešení          | Pochopení požadavků, návrh postupu, rozvržení funkcionality           | 1–2 hod    |
| 2. Vývoj hlavního skriptu (`main.py`)     | Selenium, stažení PDF, screenshot, hashování, uložení metadat         | 3–4 hod    |
| 3. Tvorba testů (`pytest`)                | Unit testy pro hlavní funkce, testování stahování, uložení, hashů     | 2–3 hod    |
| 4. Check integrity modul (`check_integrity.py`) | Porovnání metadat, CSV log                                          | 1 hod      |
| 5. Zálohování dat do ZIP (`make_zip.py`)  | Komprese dat bez archivů, připrava pro AWS                            | 0.5 hod    |
| 6. README + dokumentace                   | Popis projektu, návody, seznam závislostí, ignorace souborů           | 1–1.5 hod  |
| 7. Kalkulace AWS nákladů + .md soubory     | Odhad velikostí dat, cenová kalkulace, vytvoření .md dokumentů        | 1 hod      |
| **Celkem (odhadově)**                     |                                                                       | **9–13 hod** |
