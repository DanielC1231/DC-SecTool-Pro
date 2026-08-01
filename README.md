# 🛡️ DC - SecTool Pro

**DC - SecTool Pro** es una suite todo-en-uno de ciberseguridad que combina múltiples herramientas en una sola interfaz moderna y fácil de usar.
Por: **Wate Company**

## 🔧 Características

- 🌐 **Net Scanner**: Ping, DNS Lookup, Whois, HTTP Headers y GeoIP
- 🔍 **AD Auditor**: LDAP Scan, enumeración de usuarios, SMB Enum y DC Info
- 📊 **SIEM Lite**: Análisis de logs, detección de patrones y estadísticas del sistema
- 🔬 **Malware Analysis**: Hashes (MD5/SHA), extracción de strings y análisis de archivos
- 🧠 **Memory Forensics**: Procesos activos, conexiones de red y detección de procesos sospechosos
- 🛡️ **Port Scanner**: Escaneo de puertos personalizado, rápido y de puertos comunes
- 📡 **Subdomain Finder**: Búsqueda de subdominios vía API y DNS Bruteforce

## 🖥️ Requisitos

- Windows 10/11 (64 bits) - Se ejecuta sin necesidad de Python.
- Linux: Requiere Python 3.8+.

## 📥 Instalación

1. Descarga el archivo ZIP desde la sección de **Releases**.
2. Extrae el contenido.
3. Ejecuta `DCSecToolPro.exe`.

🔒 **Seguridad**
El programa es 100% seguro. El código fuente está disponible para su revisión.

✅ Los principales antivirus (Kaspersky, ESET, Bitdefender, ClamAV) lo detectan como limpio.

✅ Comportamiento analizado sin detecciones maliciosas.
https://www.virustotal.com/gui/file/aff54f8dce93a67d3f0622ca0daa66ee601472aa95abc00d259763dbcb9f9333/behavior

📬 Contacto
Creado por Wate Company
Enlace a itch.io
https://watecompany.itch.io/

## 📂 Ejecutar desde código fuente

```bash
pip install -r requirements.txt
python dc_sectool_pro.py

---

### **Crear un archivo `requirements.txt` (Para quienes usen Linux)**

Crea un archivo `requirements.txt` en la misma carpeta con este contenido:

```txt
customtkinter
dnspython
python-whois
requests
pefile
pyperclip
ping3
Pillow
