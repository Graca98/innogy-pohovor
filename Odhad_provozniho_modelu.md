## 📊 Předpokládaný provozní model

| Typ dat          | Frekvence             | Velikost / kus      | Odhad měsíčně |
|------------------|------------------------|----------------------|----------------|
| PDF dokumenty    | 1–5 souborů / měsíc    | 300 KB – 2 MB        | ~2 MB          |
| Screenshoty      | 1× měsíčně             | 200 – 500 KB         | ~0.5 MB        |
| metadata.json    | 1× měsíčně             | ~10 KB               | ~0.01 MB       |
| **Celkem**       |                        |                      | **~3 MB/měsíc** |

---

## 🕔 Dlouhodobá archivace

- **Ročně:** 36 MB  
- **Za 5 let:** **180 MB** (0.18 GB)

---

## 💰 Odhad nákladů na AWS S3

**Tarif:** `S3 Standard – $0.0245 / GB / měsíc`  
**Velikost:** `0.18 GB`  
**Doba:** `5 let = 60 měsíců`

```text
0.18 GB × $0.0245 × 60 měsíců = $0.2646
