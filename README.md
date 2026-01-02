# Ultimate API Hunter & WAF Bypass Framework 

> **Advanced Web Recon • API Discovery • JavaScript Mining • SQL Injection Detection**  
> **Coded By Rolandino7**

---

## Overview

**Ultimate API Hunter** adalah framework **advanced web & API reconnaissance** yang dirancang untuk pentester, bug bounty hunter, dan security researcher.

Tool ini menggabungkan:
- Smart reconnaissance
- JavaScript mining
- API endpoint discovery
- WAF evasion
- SQL Injection detection
- High-value path bruteforce

Semua dibuat untuk **automation, speed, dan akurasi**.

---

## Fitur Utama

### Recon & Enumeration
- Homepage reconnaissance
- Auto-scan:
  - `robots.txt`
  - `sitemap.xml`
  - `security.txt`
  - `humans.txt`
- Pattern extraction otomatis

---

### JavaScript Mining
- Crawl & analisis file `.js`
- Extract:
  - API endpoints
  - Base URL
  - Route internal
  - Token & API Key
  - GraphQL endpoint

---

### WAF Bypass
- Random User-Agent rotation
- Header spoofing (Sec-CH-UA, Fetch headers)
- Smart retry & delay
- API vs HTML request detection

---

### Ultra Mega Path Bruteforce
- 200+ high-value paths:
  - `/api/*`
  - `/admin`
  - `/internal`
  - `/debug`
  - `/.env`
  - `/config`
  - `/monitoring`
  - `/swagger`
- Multi-threaded (ThreadPoolExecutor)
- Auto endpoint scoring

---

### SQL Injection Detection
- Error-based SQLi
- Time-based SQLi
- Union-based SQLi
- Smart parameter targeting (GET)

---

### Session & Auth Analysis
- Deteksi cookie mencurigakan:
  - session
  - auth
  - admin
  - token
- Mapping potensi privilege leak

---

### Endpoint Scoring System
Endpoint diprioritaskan berdasarkan:
- Keyword sensitif
- HTTP status
- Response size
- Path type
- Randomization anti-false-positive

Score: **0 – 100**

---

## Teknologi yang Digunakan

- Python 3
- `requests`
- `BeautifulSoup`
- `rich` (optional UI)
- `concurrent.futures`
- Regex-based pattern matching

---

## Instalasi

```bash
git clone https://github.com/username/ultimate-api-hunter.git
cd ultimate-api-hunter
pip install -r requirements.txt
```
