import os
import sys
import ctypes
import time
import requests
import pyfiglet
import re
import shutil
from tqdm import tqdm
from colorama import Fore, Style, init
from urllib.parse import urlparse, parse_qs, quote_plus

init(autoreset=True)


def elevate_to_admin():
    if sys.platform.startswith("win") and not ctypes.windll.shell32.IsUserAnAdmin():
        print(Fore.YELLOW + "\n🔄 Requesting Admin Privileges...\n")
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()


def extract_font_name_from_url(font_url):
    parsed = urlparse(font_url)
    q = parse_qs(parsed.query)
    if "family" in q:
        return q["family"][0].replace("+", " ")
    elif parsed.path.startswith("/specimen/"):
        return parsed.path.split("/")[-1].replace("+", " ")
    return None


def fetch_variants(font_name):
    url = "https://fonts.googleapis.com/css2?family=" + quote_plus(font_name) + "&display=swap"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return re.findall(r"font-style:\s*(normal|italic);.*?font-weight:\s*(\d+);.*?url\((.*?)\)", r.text, re.DOTALL)


def create_license(folder):
    r = requests.get("https://fonts.google.com/attribution")
    if r.status_code == 200:
        with open(os.path.join(folder, "LICENSE.txt"), "w", encoding="utf-8") as f:
            f.write(r.text)


def install_font_on_windows(font_path):
    dest = os.path.join(os.environ["WINDIR"], "Fonts", os.path.basename(font_path))
    if not os.path.exists(dest):
        shutil.copy(font_path, dest)
        ctypes.windll.gdi32.AddFontResourceW(dest)
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x001D, 0, 0)
        print(Fore.GREEN + f"✅ Installed: {os.path.basename(font_path)}")


def loading_animation(text, delay=0.1):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print("")


def download_font(font_name):
    print(Fore.CYAN + f"\n🔍 Fetching variants for {font_name}...")
    variants = fetch_variants(font_name)
    if not variants:
        print(Fore.RED + "❌ No variants found. Skipping.")
        return

    print(Fore.YELLOW + "\n📜 Available Variants:")
    for i, (style, weight, link) in enumerate(variants):
        print(Fore.LIGHTBLUE_EX + f" [{i+1}] {weight} - {style}")

    choice = input(Fore.CYAN + "\n🎯 Enter variant numbers (comma-separated) or press Enter for all: ").strip()
    selected_variants = variants if not choice else [variants[int(i)-1] for i in choice.split(",") if i.isdigit()]

    folder = font_name.replace(" ", "_")
    os.makedirs(folder, exist_ok=True)
    create_license(folder)

    print(Fore.GREEN + "\n🚀 Downloading fonts...\n")
    for style, weight, link in selected_variants:
        subfolder = f"{style}-{weight}"
        path = os.path.join(folder, subfolder)
        os.makedirs(path, exist_ok=True)

        font_data = requests.get(link, stream=True)
        if font_data.status_code == 200:
            ext = link.split(".")[-1].split(")")[0]
            filename = f"{font_name.replace(' ', '_')}-{weight}-{style}.{ext}"
            file_path = os.path.join(path, filename)
            
            # Progress Bar for Downloads
            total_size = int(font_data.headers.get("content-length", 0))
            with open(file_path, "wb") as f, tqdm(
                desc=f"📥 Downloading {filename}", total=total_size, unit="B", unit_scale=True
            ) as pbar:
                for chunk in font_data.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

            print(Fore.GREEN + f"✅ Saved: {file_path}")

            
            install_font_on_windows(file_path)

    print(Fore.LIGHTMAGENTA_EX + f"\n🎉 '{font_name}' is fully downloaded and installed!\n")
    print("\a") 

# MAIN SCRIPT
if __name__ == "__main__":
    elevate_to_admin()  

    print("\n" + Fore.BLUE + pyfiglet.figlet_format("Google Font Downloader", font="slant"))
    print(Fore.LIGHTYELLOW_EX + " </> by Ansh Kabra")
    print(Fore.LIGHTBLACK_EX + "=" * 50)

    bulk = input(Fore.CYAN + "📥 Enter font names or Google Fonts links (comma-separated): ").strip()
    if not bulk:
        print(Fore.RED + "❌ No input provided. Exiting.")
        sys.exit()

    items = [x.strip() for x in bulk.split(",") if x.strip()]
    for item in items:
        if item.startswith("http"):
            name = extract_font_name_from_url(item)
            if name:
                download_font(name)
        else:
            download_font(item)

    print(Fore.GREEN + "\n🎯 All tasks completed! Your fonts are installed. Enjoy! 🚀")