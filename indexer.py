import os
import json
import requests
from google.oauth2 import service_account
import googleapiclient.discovery

# --- KONFIGURASI DOMAIN & SITEMAP ---
BASE_URL = "https://thenewsday112.github.io/milion"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"  # Sesuaikan dengan lokasi file sitemap Anda di folder output/root

def ping_google_sitemap():
    print("=" * 60)
    print("MENGIRIM SITEMAP KE GOOGLE SEARCH & PING API")
    print("=" * 60)

    # 1. Cara Paling Mudah: Menggunakan URL Ping Resmi Google
    # Google Bot akan otomatis datang merayapi sitemap ketika di-ping ke URL ini
    ping_url = f"https://www.google.com/ping?sitemap={SITEMAP_URL}"
    
    try:
        response = requests.get(ping_url)
        if response.status_code == 200:
            print(f"[OK] Berhasil melakukan Ping Sitemap ke Google: {SITEMAP_URL}")
        else:
            print(f"[-] Gagal Ping Sitemap, status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error saat melakukan HTTP Ping: {e}")

    # 2. (Opsional) Menggunakan Indexing API untuk memberitahu URL Sitemap-nya langsung
    try:
        google_creds_env = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if google_creds_env:
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
        print(f"[-] Info: Indexing API skip atau limit tercapai ({e})")

    print("=" * 60)
    print("[SELESAI] Sitemap telah diserahkan ke Google.")

if __name__ == "__main__":
    ping_google_sitemap()
