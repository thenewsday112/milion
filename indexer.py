import os
import json
import requests
from google.oauth2 import service_account
import googleapiclient.discovery

# --- KONFIGURASI REPO & DOMAIN ---
BASE_URL = "https://thenewsday112.github.io/milion"
# Mengarahkan langsung ke file sitemap.xml di dalam folder output/
SITEMAP_URL = f"{BASE_URL}/output/sitemap.xml"  

def run_google_indexer():
    print("=" * 60)
    print("MENGIRIM PING SITEMAP KE GOOGLE SEARCH & INDEXING API")
    print("=" * 60)

    # 1. Melakukan HTTP Ping resmi ke Google untuk Sitemap
    ping_url = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"
    try:
        response = requests.get(ping_url)
        if response.status_code == 200:
            print(f"[OK] Berhasil melakukan Ping Sitemap: {SITEMAP_URL}")
        else:
            print(f"[-] Ping Sitemap mengembalikan status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error saat melakukan HTTP Ping: {e}")

    # 2. Mencoba mendaftarkan Sitemap via Google Indexing API (Opsional jika kuota masih ada)
    try:
        google_creds_env = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if not google_creds_env:
            print("[-] Info: Secret GOOGLE_CREDENTIALS_JSON tidak ditemukan, melewati Indexing API.")
            return
            
        creds_dict = json.loads(google_creds_env)
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = googleapiclient.discovery.build("indexing", "v3", credentials=credentials)
        
        body = {
            "url": SITEMAP_URL,
            "type": "URL_UPDATED"
        }
        
        req = service.urlNotifications().publish(body=body)
        res = req.execute()
        print(f"[OK] Berhasil mendaftarkan Sitemap via Google Indexing API.")
        
    except Exception as e:
        # Menangani error kuota habis (429) agar tidak membuat GitHub Actions gagal total
        print(f"[-] Info: Indexing API di-skip atau kuota harian tercapai (Error 429).")
        print(f"    Detail: Gunakan Google Search Console untuk submit sitemap secara manual jika kuota habis.")

    print("=" * 60)
    print("[SELESAI] Proses penyerahan sitemap selesai.")
    print("=" * 60)

if __name__ == "__main__":
    run_google_indexer()
