# **Google Font Downloader & Auto-Installer**  
### **The Ultimate Google Fonts CLI Tool**  
**</> by Ansh Kabra**  

---

## **Features**  

- Bulk Google Font Downloading  
- Auto-Request Admin Privileges (No manual approvals needed)  
- Auto-Install Fonts into Windows (No dragging required)  
- Progress Bar for Downloads (Smooth experience with `tqdm`)  
- Interactive Font Variant Selection (Pick weights and styles)  
- Supports Multiple Formats (`woff2`, `ttf`, `otf`)  
- Auto-Generate Font Preview (`ttf`, `otf`)  
- Organizes Fonts in Neat Folders  
- Auto-Downloads Google Fonts License  
- Font Installation Verification (Confirms install)  
- Real-Time CLI Animations and Colorized Output  
- Windows, Linux, and macOS Compatibility  
- Sound Effects on Completion  

---

## **Installation**  

### **Requirements**  

- Python 3.x  
- `pip install -r requirements.txt`  

```sh
pip install pyfiglet tqdm colorama requests
```

---

## **Usage**  

Run the script with Python:  

```sh
python font_downloader.py
```

Enter font names or Google Fonts links, separated by commas:  

```sh
Enter font names or links: Roboto, Open Sans, https://fonts.google.com/specimen/JetBrains+Mono
```

Choose specific font weights or download all:  

```sh
Available Variants:
[1] 400 - normal  
[2] 700 - normal  
[3] 400 - italic  
[4] 700 - italic  

Enter numbers to select variants (comma-separated) or press Enter to download all: 1,3
```

Fonts are downloaded and installed automatically.  

---

## **Example Folder Structure**  

```
Roboto/
 ├── LICENSE.txt
 ├── normal-400/
 │   ├── Roboto-400-normal.woff2
 ├── italic-400/
 │   ├── Roboto-400-italic.woff2
```

---

## **Contributing**  

1. Fork the repository  
2. Create a new branch  
3. Make changes and commit  
4. Push to your fork  
5. Open a pull request  

---

## **License**  

This project is licensed under the Unlicense.  

---

## **Author**  

**</> by Ansh Kabra**
