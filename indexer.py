import os
import json
from google.oauth2 import service_account
import googleapiclient.discovery

# --- KONFIGURASI REPO & DOMAIN ---
BASE_URL = "https://thenewsday112.github.io/milion"

# Daftar halaman indeks, paginasi, dan kategori utama yang ingin di-index
INDEX_PAGES = [
    "/output/index.html",
    "/output/page1.html",
    "/output/page2.html",
    "/output/technology.html",
    "/output/business.html",
    "/output/sports.html",
    "/output/entertainment.html",
    "/output/science.html",
]

def run_google_indexer():
    print("=" * 60)
    print("MENGIRIM HALAMAN INDEKS & KATEGORI KE GOOGLE INDEXING API")
    print("=" * 60)

    # 1. Autentikasi Google API via GitHub Secret
    try:
        google_creds_env = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if not google_creds_env:
            print("[-] ERROR: Secret GOOGLE_CREDENTIALS_JSON tidak ditemukan!")
            return
            
        creds_dict = json.loads(google_creds_env)
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = googleapiclient.discovery.build("indexing", "v3", credentials=credentials)
        print("[+] Berhasil terhubung ke Google Indexing API.")
    except Exception as e:
        print(f"[-] Gagal autentikasi: {e}")
        return

    success_count = 0
    failed_count = 0

    # 2. Kirim URL Halaman Indeks & Kategori Utama
    for path in INDEX_PAGES:
        url_to_index = f"{BASE_URL}{path}"

        body = {
            "url": url_to_index,
            "type": "URL_UPDATED"
        }

        try:
            request = service.urlNotifications().publish(body=body)
            response = request.execute()
            success_count += 1
            print(f"[OK] Berhasil di-index: {url_to_index}")
        except Exception as e:
            failed_count += 1
            print(f"[GAGAL] {url_to_index} -> Error: {e}")

    print("\n" + "=" * 60)
    print(f"[PROSES SELESAI]")
    print(f" - Berhasil dikirim : {success_count}")
    print(f" - Gagal             : {failed_count}")
    print("=" * 60)

if __name__ == "__main__":
    run_google_indexer()
