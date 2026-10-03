#POR WATE COMPANY, bueno si es quieres hacer uso de mi proyecto esta bien solo dame créditos porfavor.

import customtkinter as ctk
import subprocess
import os
import hashlib
import threading
from datetime import datetime
import socket
import platform
import re
import requests
import json
import base64
import time
from tkinter import filedialog, messagebox
import pyperclip
import math

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class DCSecToolPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ DC - SecTool Pro - Suite de Ciberseguridad")
        self.root.geometry("1400x900")
        
        # Variables para estadísticas
        self.log_stats = {}
        
        # Directorio donde se guardan los archivos
        self.save_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Menú principal
        self.create_menu()
        
        # Área principal con pestañas
        self.tabview = ctk.CTkTabview(root, width=1380, height=850)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Crear todas las pestañas
        self.tabs = {}
        for tab_name in ["🌐 Net Scanner", "🔍 AD Auditor", "📊 SIEM Lite", 
                        "🔬 Malware Analysis", "🧠 Memory Forensics", 
                        "🛡️ Port Scanner", "📡 Subdomain Finder"]:
            self.tabview.add(tab_name)
            self.tabs[tab_name] = self.tabview.tab(tab_name)
        
        # Construir cada pestaña
        self.build_net_scanner()
        self.build_ad_auditor()
        self.build_siem_lite()
        self.build_malware_analysis()
        self.build_memory_forensics()
        self.build_port_scanner()
        self.build_subdomain_finder()
        
        # Estado de la aplicación
        self.status_label = ctk.CTkLabel(root, text="🟢 Sistema listo", font=("Arial", 12))
        self.status_label.pack(side="bottom", pady=5)

    # ========== FUNCIÓN PARA EJECUTAR COMANDOS SIN CMD ==========
    def run_cmd_silent(self, cmd, timeout=10):
        """Ejecuta un comando sin mostrar ventana de CMD en Windows"""
        try:
            if platform.system() == "Windows":
                # En Windows, ocultar la ventana de CMD
                CREATE_NO_WINDOW = 0x08000000
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=timeout,
                    creationflags=CREATE_NO_WINDOW
                )
            else:
                # En Linux/Mac, ejecutar normalmente
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=timeout
                )
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            return None

    def create_menu(self):
        """Menú superior con opciones rápidas"""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        buttons = [
            ("📁 Nueva Sesión", self.new_session),
            ("💾 Guardar Todo", self.save_all_sessions),
            ("📊 Reporte", self.generate_report),
            ("⚙️ Configurar", self.open_settings),
            ("🌐 Verificar IP", self.check_public_ip),
            ("📋 Copiar Todo", self.copy_all_results)
        ]
        
        for text, cmd in buttons:
            btn = ctk.CTkButton(menu_frame, text=text, width=120, height=30, 
                              command=cmd, fg_color="transparent", 
                              hover_color="#2a2a2a")
            btn.pack(side="left", padx=5, pady=5)

    # ========== FUNCIÓN PARA COPIAR AL PORTAPAPELES ==========
    def copy_to_clipboard(self, text, success_msg="✅ Copiado al portapapeles"):
        try:
            pyperclip.copy(text)
            self.status_label.configure(text=success_msg)
            messagebox.showinfo("Éxito", success_msg)
        except Exception as e:
            self.status_label.configure(text=f"❌ Error al copiar: {str(e)}")
            messagebox.showerror("Error", f"No se pudo copiar: {str(e)}")

    def copy_all_results(self):
        all_text = "=== DC - SecTool Pro - Resultados ===\n"
        all_text += f"Fecha: {datetime.now()}\n\n"
        
        results = [
            (self.scan_result, "Net Scanner"),
            (self.ad_result, "AD Auditor"),
            (self.siem_result, "SIEM Lite"),
            (self.malware_result, "Malware Analysis"),
            (self.memory_result, "Memory Forensics"),
            (self.port_result, "Port Scanner"),
            (self.sub_result, "Subdomain Finder")
        ]
        
        for result, name in results:
            text = result.get("0.0", "end").strip()
            if text:
                all_text += f"\n=== {name} ===\n"
                all_text += text + "\n"
        
        self.copy_to_clipboard(all_text, "✅ Todos los resultados copiados al portapapeles")

    # ========== FUNCIONES DE GUARDADO ==========
    def save_all_sessions(self):
        """Guarda TODAS las pestañas en archivos individuales"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar los resultados",
            initialdir=self.save_dir
        )
        
        if not folder:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []
        
        results = [
            (self.scan_result, "Net_Scanner"),
            (self.ad_result, "AD_Auditor"),
            (self.siem_result, "SIEM_Lite"),
            (self.malware_result, "Malware_Analysis"),
            (self.memory_result, "Memory_Forensics"),
            (self.port_result, "Port_Scanner"),
            (self.sub_result, "Subdomain_Finder")
        ]
        
        try:
            for result, name in results:
                text = result.get("0.0", "end").strip()
                if text:
                    filename = f"{name}_{timestamp}.txt"
                    filepath = os.path.join(folder, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"=== DC - SecTool Pro - {name} ===\n")
                        f.write(f"Fecha: {datetime.now()}\n")
                        f.write("="*50 + "\n\n")
                        f.write(text)
                    saved_files.append(filename)
            
            if saved_files:
                mensaje = f"✅ Guardados {len(saved_files)} archivos en:\n{folder}\n\nArchivos:\n"
                for f in saved_files:
                    mensaje += f"  📄 {f}\n"
                messagebox.showinfo("Éxito", mensaje)
                self.status_label.configure(text=f"💾 Guardados {len(saved_files)} archivos")
            else:
                messagebox.showwarning("Sin datos", "No hay resultados para guardar")
                
        except Exception as e:
            self.status_label.configure(text=f"❌ Error al guardar: {str(e)}")
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

    def save_single_result(self, widget, name):
        """Guarda el resultado de una sola pestaña"""
        text = widget.get("0.0", "end").strip()
        if not text:
            messagebox.showwarning("Sin datos", f"No hay resultados en {name} para guardar")
            return
        
        folder = filedialog.askdirectory(
            title=f"Seleccionar carpeta para guardar {name}",
            initialdir=self.save_dir
        )
        
        if not folder:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.txt"
        filepath = os.path.join(folder, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== DC - SecTool Pro - {name} ===\n")
                f.write(f"Fecha: {datetime.now()}\n")
                f.write("="*50 + "\n\n")
                f.write(text)
            
            messagebox.showinfo("Éxito", f"✅ Guardado en:\n{filepath}")
            self.status_label.configure(text=f"💾 {name} guardado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

    def copy_result(self, widget, name):
        text = widget.get("0.0", "end").strip()
        if text:
            self.copy_to_clipboard(text, f"✅ Resultados de {name} copiados")
        else:
            messagebox.showwarning("Sin datos", f"No hay resultados en {name} para copiar")

    # ========== 1. NET SCANNER ==========
    def build_net_scanner(self):
        tab = self.tabs["🌐 Net Scanner"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="IP / Dominio:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.scan_target = ctk.CTkEntry(frame, width=200, placeholder_text="ej. google.com")
        self.scan_target.grid(row=0, column=1, padx=10, pady=10)
        self.scan_target.insert(0, "google.com")
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🏓 Ping", command=self.ping_real,
                     fg_color="#28B463").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🌐 DNS Lookup", command=self.dns_lookup_real,
                     fg_color="#F39C12").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔍 Whois", command=self.whois_real,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📡 HTTP Headers", command=self.http_headers_real,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🌍 GeoIP", command=self.geoip_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.scan_result, "Net Scanner"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.scan_result, "Net_Scanner"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.scan_result = ctk.CTkTextbox(tab, height=350, font=("Consolas", 11))
        self.scan_result.pack(padx=20, pady=10, fill="both", expand=True)

    def ping_real(self):
        """Ping real SIN ventana de CMD"""
        target = self.scan_target.get()
        self.scan_result.delete("0.0", "end")
        self.scan_result.insert("end", f"🏓 Pinging {target}...\n\n")
        
        def ping_thread():
            try:
                param = "-n" if platform.system().lower() == "windows" else "-c"
                if platform.system() == "Windows":
                    cmd = f"ping {param} 4 {target}"
                    result = self.run_cmd_silent(cmd, timeout=10)
                else:
                    cmd = f"ping {param} 4 {target}"
                    result = self.run_cmd_silent(cmd, timeout=10)
                
                if result:
                    self.scan_result.insert("end", result.stdout)
                    if result.returncode == 0:
                        self.status_label.configure(text="✅ Ping exitoso")
                    else:
                        self.status_label.configure(text="❌ Ping fallido")
                else:
                    self.scan_result.insert("end", "❌ Tiempo de espera agotado\n")
                self.scan_result.see("end")
            except Exception as e:
                self.scan_result.insert("end", f"❌ Error: {str(e)}")
        
        threading.Thread(target=ping_thread, daemon=True).start()

    def dns_lookup_real(self):
        target = self.scan_target.get()
        self.scan_result.insert("end", f"\n🌐 DNS Lookup para {target}...\n\n")
        
        try:
            ips = socket.gethostbyname_ex(target)
            self.scan_result.insert("end", f"📌 IPs: {', '.join(ips[2])}\n")
            
            try:
                import dns.resolver
                for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                    try:
                        answers = dns.resolver.resolve(target, record_type)
                        self.scan_result.insert("end", f"📌 {record_type}: {[str(r) for r in answers][:5]}\n")
                    except:
                        pass
            except:
                pass
                
            self.status_label.configure(text="✅ DNS Lookup completado")
        except Exception as e:
            self.scan_result.insert("end", f"❌ Error: {str(e)}")

    def whois_real(self):
        target = self.scan_target.get()
        self.scan_result.insert("end", f"\n🔍 Whois para {target}...\n\n")
        
        try:
            import whois
            w = whois.whois(target)
            self.scan_result.insert("end", f"📌 Dominio: {w.domain_name}\n")
            self.scan_result.insert("end", f"📌 Registrador: {w.registrar}\n")
            self.scan_result.insert("end", f"📌 Fecha creación: {w.creation_date}\n")
            self.scan_result.insert("end", f"📌 Fecha expiración: {w.expiration_date}\n")
            self.scan_result.insert("end", f"📌 DNS: {w.name_servers}\n")
            self.status_label.configure(text="✅ Whois completado")
        except Exception as e:
            self.scan_result.insert("end", f"❌ Error: {str(e)}\n")

    def http_headers_real(self):
        target = self.scan_target.get()
        if not target.startswith('http'):
            target = 'http://' + target
        self.scan_result.insert("end", f"\n📡 Obteniendo headers de {target}...\n\n")
        
        try:
            response = requests.get(target, timeout=5, verify=False)
            self.scan_result.insert("end", f"📌 Status Code: {response.status_code}\n")
            self.scan_result.insert("end", f"📌 Server: {response.headers.get('Server', 'N/A')}\n")
            self.scan_result.insert("end", f"📌 Content-Type: {response.headers.get('Content-Type', 'N/A')}\n")
            self.scan_result.insert("end", f"📌 Content-Length: {response.headers.get('Content-Length', 'N/A')}\n")
            
            security_headers = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options', 'Strict-Transport-Security']
            self.scan_result.insert("end", "\n🔒 Headers de seguridad:\n")
            for header in security_headers:
                value = response.headers.get(header, 'No encontrado')
                status = '✅' if value != 'No encontrado' else '❌'
                self.scan_result.insert("end", f"  {status} {header}: {value}\n")
                
            self.status_label.configure(text="✅ Headers obtenidos")
        except Exception as e:
            self.scan_result.insert("end", f"❌ Error: {str(e)}")

    def geoip_real(self):
        target = self.scan_target.get()
        self.scan_result.insert("end", f"\n🌍 GeoIP para {target}...\n\n")
        
        try:
            try:
                ip = socket.gethostbyname(target)
            except:
                ip = target
            
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                self.scan_result.insert("end", f"📌 IP: {data.get('query')}\n")
                self.scan_result.insert("end", f"📌 País: {data.get('country')} ({data.get('countryCode')})\n")
                self.scan_result.insert("end", f"📌 Ciudad: {data.get('city')}\n")
                self.scan_result.insert("end", f"📌 ISP: {data.get('isp')}\n")
                self.scan_result.insert("end", f"📌 Coordenadas: {data.get('lat')}, {data.get('lon')}\n")
                self.scan_result.insert("end", f"📌 Zona horaria: {data.get('timezone')}\n")
            else:
                self.scan_result.insert("end", "❌ No se pudo obtener información GeoIP\n")
                
            self.status_label.configure(text="✅ GeoIP completado")
        except Exception as e:
            self.scan_result.insert("end", f"❌ Error: {str(e)}")

    # ========== 2. AD AUDITOR ==========
    def build_ad_auditor(self):
        tab = self.tabs["🔍 AD Auditor"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="Dominio:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.ad_domain = ctk.CTkEntry(frame, width=200, placeholder_text="ej. dominio.local")
        self.ad_domain.grid(row=0, column=1, padx=10, pady=10)
        self.ad_domain.insert(0, "localhost")
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔍 LDAP Scan", command=self.ldap_scan_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="👥 Enumerar Usuarios", command=self.enum_users_real,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔑 SMB Enum", command=self.smb_enum_real,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🌐Info", command=self.dc_info_real,
                     fg_color="#F39C12").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.ad_result, "AD Auditor"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.ad_result, "AD_Auditor"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.ad_result = ctk.CTkTextbox(tab, height=300, font=("Consolas", 11))
        self.ad_result.pack(padx=20, pady=10, fill="both", expand=True)

    def ldap_scan_real(self):
        domain = self.ad_domain.get()
        self.ad_result.delete("0.0", "end")
        self.ad_result.insert("end", f"🔍 Escaneando LDAP: {domain}...\n\n")
        
        try:
            socket.gethostbyname(domain)
            self.ad_result.insert("end", f"✅ Dominio {domain} resuelto\n")
            
            ports = [389, 636, 3268, 3269]
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((domain, port))
                sock.close()
                if result == 0:
                    self.ad_result.insert("end", f"✅ Puerto LDAP {port} ABIERTO\n")
                else:a
                    self.ad_result.insert("end", f"❌ Puerto LDAP {port} CERRADO\n")
                    
            self.status_label.configure(text="✅ LDAP scan completado")
        except Exception as e:
            self.ad_result.insert("end", f"❌ Error: {str(e)}\n")

    def enum_users_real(self):
        self.ad_result.insert("end", "\n👥 Enumerando usuarios del sistema...\n\n")
        
        try:
            if platform.system() == "Windows":
                cmd = "net user"
                result = self.run_cmd_silent(cmd, timeout=10)
            else:
                cmd = "getent passwd | cut -d: -f1 | head -20"
                result = self.run_cmd_silent(cmd, timeout=10)
            
            if result:
                self.ad_result.insert("end", result.stdout)
                self.status_label.configure(text="✅ Usuarios enumerados")
            else:
                self.ad_result.insert("end", "❌ Error al ejecutar el comando\n")
        except Exception as e:
            self.ad_result.insert("end", f"❌ Error: {str(e)}")

    def smb_enum_real(self):
        domain = self.ad_domain.get()
        self.ad_result.insert("end", f"\n🔑 Enumerando SMB en {domain}...\n\n")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((domain, 445))
            sock.close()
            
            if result == 0:
                self.ad_result.insert("end", "✅ Puerto SMB (445) ABIERTO\n")
                
                if platform.system() == "Windows":
                    cmd = f"net view \\\\{domain}"
                    result = self.run_cmd_silent(cmd, timeout=10)
                    if result:
                        self.ad_result.insert("end", result.stdout)
            else:
                self.ad_result.insert("end", "❌ Puerto SMB (445) CERRADO\n")
                
            self.status_label.configure(text="✅ SMB enum completado")
        except Exception as e:
            self.ad_result.insert("end", f"❌ Error: {str(e)}")

    def dc_info_real(self):
        domain = self.ad_domain.get()
        self.ad_result.insert("end", f"\n🌐 Información del DC: {domain}\n\n")
        
        try:
            ip = socket.gethostbyname(domain)
            self.ad_result.insert("end", f"📌 IP: {ip}\n")
            
            common_ports = {
                53: "DNS", 88: "Kerberos", 135: "RPC", 139: "NetBIOS",
                389: "LDAP", 445: "SMB", 636: "LDAPS", 3268: "Global Catalog",
                3269: "Global Catalog SSL"
            }
            
            self.ad_result.insert("end", "\n📡 Puertos comunes:\n")
            for port, service in common_ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((domain, port))
                sock.close()
                if result == 0:
                    self.ad_result.insert("end", f"  ✅ {port}: {service}\n")
                else:
                    self.ad_result.insert("end", f"  ❌ {port}: {service}\n")
                    
            self.status_label.configure(text="✅ DC info obtenida")
        except Exception as e:
            self.ad_result.insert("end", f"❌ Error: {str(e)}")

    # ========== 3. SIEM LITE ==========
    def build_siem_lite(self):
        tab = self.tabs["📊 SIEM Lite"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="Ruta de logs:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.siem_path = ctk.CTkEntry(frame, width=400, placeholder_text="C:/logs/ o /var/log/")
        self.siem_path.grid(row=0, column=1, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="📂 Cargar Logs Sistema", command=self.load_system_logs,
                     fg_color="#28B463").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔍 Analizar", command=self.analyze_logs_real,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📊 Estadísticas", command=self.show_stats_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔎 Buscar IP", command=self.search_ip_in_logs,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.siem_result, "SIEM Lite"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.siem_result, "SIEM_Lite"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.siem_result = ctk.CTkTextbox(tab, height=300, font=("Consolas", 11))
        self.siem_result.pack(padx=20, pady=10, fill="both", expand=True)

    def load_system_logs(self):
        self.siem_result.delete("0.0", "end")
        self.log_stats = {}
        
        try:
            if platform.system() == "Windows":
                log_paths = [
                    "C:/Windows/System32/winevt/Logs/System.evtx",
                    "C:/Windows/System32/winevt/Logs/Security.evtx",
                    "C:/Windows/System32/winevt/Logs/Application.evtx"
                ]
                for log_path in log_paths:
                    if os.path.exists(log_path):
                        size = os.path.getsize(log_path) / (1024 * 1024)
                        self.siem_result.insert("end", f"✅ {os.path.basename(log_path)} - {size:.2f} MB\n")
                    else:
                        self.siem_result.insert("end", f"❌ {os.path.basename(log_path)} no encontrado\n")
                
                self.siem_result.insert("end", "\n📊 Últimos 20 eventos del sistema:\n\n")
                cmd = 'powershell "Get-WinEvent -MaxEvents 20 -LogName System | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName | Format-Table -AutoSize"'
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.siem_result.insert("end", result.stdout)
                
            else:
                log_files = ["/var/log/syslog", "/var/log/auth.log", "/var/log/secure", "/var/log/messages"]
                for log_file in log_files:
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            lines = f.readlines()[-30:]
                            self.siem_result.insert("end", f"\n✅ {log_file} - {len(lines)} líneas\n")
                            for line in lines:
                                self.siem_result.insert("end", line)
            
            self.status_label.configure(text="✅ Logs cargados")
        except Exception as e:
            self.siem_result.insert("end", f"❌ Error: {str(e)}")
            self.siem_result.insert("end", "\n⚠️ Necesitas permisos de administrador para leer logs")

    def analyze_logs_real(self):
        self.siem_result.insert("end", "\n🔍 Analizando logs...\n\n")
        
        try:
            patterns = {
                "failed": {"color": "🔴", "desc": "Fallo de autenticación"},
                "error": {"color": "🔴", "desc": "Error del sistema"},
                "warning": {"color": "🟡", "desc": "Advertencia"},
                "denied": {"color": "🔴", "desc": "Acceso denegado"},
                "attack": {"color": "🔴", "desc": "Posible ataque"},
                "malware": {"color": "🔴", "desc": "Malware detectado"},
                "virus": {"color": "🔴", "desc": "Virus detectado"},
                "exploit": {"color": "🔴", "desc": "Exploit detectado"},
                "unauthorized": {"color": "🔴", "desc": "Acceso no autorizado"},
                "invalid": {"color": "🟡", "desc": "Entrada inválida"},
                "success": {"color": "🟢", "desc": "Operación exitosa"},
                "connected": {"color": "🟢", "desc": "Conexión establecida"}
            }
            
            found_patterns = []
            
            if platform.system() == "Windows":
                cmd = 'powershell "Get-WinEvent -MaxEvents 100 | Select-Object Message"'
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    lines = result.stdout.split('\n')
                else:
                    lines = []
            else:
                lines = []
                for log_file in ["/var/log/syslog", "/var/log/auth.log"]:
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            lines.extend(f.readlines()[-50:])
            
            for line in lines:
                for pattern, info in patterns.items():
                    if pattern.lower() in line.lower():
                        found_patterns.append(f"{info['color']} {info['desc']}: {line[:100]}...")
                        break
            
            if found_patterns:
                self.siem_result.insert("end", f"⚠️ Encontrados {len(found_patterns)} patrones:\n\n")
                for pattern in found_patterns[:20]:
                    self.siem_result.insert("end", f"{pattern}\n")
            else:
                self.siem_result.insert("end", "✅ No se encontraron patrones sospechosos\n")
            
            self.status_label.configure(text="✅ Análisis completado")
        except Exception as e:
            self.siem_result.insert("end", f"❌ Error: {str(e)}")

    def show_stats_real(self):
        self.siem_result.insert("end", "\n📊 Estadísticas del sistema:\n\n")
        
        try:
            self.siem_result.insert("end", f"📌 Sistema: {platform.system()} {platform.release()}\n")
            self.siem_result.insert("end", f"📌 Versión: {platform.version()}\n")
            self.siem_result.insert("end", f"📌 Usuario: {os.getlogin()}\n")
            self.siem_result.insert("end", f"📌 Hostname: {socket.gethostname()}\n")
            
            if platform.system() == "Windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p("C:"), None, None, ctypes.pointer(free_bytes))
                free_gb = free_bytes.value / (1024**3)
                self.siem_result.insert("end", f"📌 Espacio libre C:: {free_gb:.2f} GB\n")
            else:
                import shutil
                total, used, free = shutil.disk_usage("/")
                self.siem_result.insert("end", f"📌 Espacio total: {total // (2**30)} GB\n")
                self.siem_result.insert("end", f"📌 Espacio usado: {used // (2**30)} GB\n")
                self.siem_result.insert("end", f"📌 Espacio libre: {free // (2**30)} GB\n")
            
            self.siem_result.insert("end", "\n🌐 Conexiones de red:\n")
            if platform.system() == "Windows":
                cmd = "netstat -an | findstr ESTABLISHED | find /c /v \"\""
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.siem_result.insert("end", f"📌 Conexiones establecidas: {result.stdout.strip()}\n")
            else:
                cmd = "netstat -tunap | grep ESTABLISHED | wc -l"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.siem_result.insert("end", f"📌 Conexiones establecidas: {result.stdout.strip()}\n")
            
            if platform.system() == "Windows":
                cmd = "tasklist | find /c /v \"\""
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.siem_result.insert("end", f"📌 Procesos activos: {result.stdout.strip()}\n")
            
            self.status_label.configure(text="✅ Estadísticas mostradas")
        except Exception as e:
            self.siem_result.insert("end", f"❌ Error: {str(e)}")

    def search_ip_in_logs(self):
        self.siem_result.insert("end", "\n🔎 Buscando IPs en logs...\n\n")
        
        try:
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ips_found = set()
            
            if platform.system() == "Windows":
                cmd = 'powershell "Get-WinEvent -MaxEvents 200 | Select-Object Message"'
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    lines = result.stdout.split('\n')
                else:
                    lines = []
            else:
                lines = []
                for log_file in ["/var/log/auth.log", "/var/log/syslog"]:
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            lines.extend(f.readlines()[-100:])
            
            for line in lines:
                ips = re.findall(ip_pattern, line)
                for ip in ips:
                    if ip not in ['127.0.0.1', '0.0.0.0']:
                        ips_found.add(ip)
            
            if ips_found:
                self.siem_result.insert("end", f"📌 IPs encontradas ({len(ips_found)}):\n")
                for ip in sorted(ips_found):
                    try:
                        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                        data = response.json()
                        country = data.get('country', 'Desconocido')
                        self.siem_result.insert("end", f"  🌍 {ip} - {country}\n")
                    except:
                        self.siem_result.insert("end", f"  🌐 {ip}\n")
            else:
                self.siem_result.insert("end", "✅ No se encontraron IPs en los logs\n")
                
            self.status_label.configure(text="✅ Búsqueda completada")
        except Exception as e:
            self.siem_result.insert("end", f"❌ Error: {str(e)}")

    # ========== 4. MALWARE ANALYSIS ==========
    def build_malware_analysis(self):
        tab = self.tabs["🔬 Malware Analysis"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="Archivo a analizar:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.malware_path = ctk.CTkEntry(frame, width=350, placeholder_text="Selecciona un archivo...")
        self.malware_path.grid(row=0, column=1, padx=10, pady=10)
        
        self.browse_btn = ctk.CTkButton(frame, text="📂 Examinar", command=self.browse_file,
                                       fg_color="#2E86C1", width=100)
        self.browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔍 Hashes", command=self.calc_hashes_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📝 Strings", command=self.extract_strings_real,
                     fg_color="#F39C12").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔬 Info Archivo", command=self.file_info_real,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔍 VirusTotal", command=self.virustotal_real,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📊 Entropía", command=self.entropy_real,
                     fg_color="#F39C12").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.malware_result, "Malware Analysis"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.malware_result, "Malware_Analysis"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.malware_result = ctk.CTkTextbox(tab, height=300, font=("Consolas", 11))
        self.malware_result.pack(padx=20, pady=10, fill="both", expand=True)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo para analizar",
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Ejecutables", "*.exe *.dll *.scr *.com"),
                ("APK/Android", "*.apk"),
                ("Archivos de Office", "*.doc *.docx *.xls *.xlsx *.ppt *.pptx"),
                ("PDF", "*.pdf"),
                ("Archivos comprimidos", "*.zip *.rar *.7z"),
                ("Scripts", "*.py *.js *.vbs *.ps1 *.bat *.cmd")
            ]
        )
        if filename:
            self.malware_path.delete(0, "end")
            self.malware_path.insert(0, filename)
            self.status_label.configure(text=f"📁 Archivo seleccionado: {os.path.basename(filename)}")

    def calc_hashes_real(self):
        path = self.malware_path.get()
        self.malware_result.delete("0.0", "end")
        
        if not os.path.exists(path):
            self.malware_result.insert("end", f"❌ Archivo no encontrado: {path}\n")
            self.malware_result.insert("end", "💡 Usa el botón 'Examinar' para seleccionar un archivo\n")
            return
        
        try:
            with open(path, 'rb') as f:
                data = f.read()
                
            self.malware_result.insert("end", f"🔍 Analizando: {os.path.basename(path)}\n")
            self.malware_result.insert("end", f"📌 Ruta: {path}\n\n")
            self.malware_result.insert("end", f"📌 MD5: {hashlib.md5(data).hexdigest()}\n")
            self.malware_result.insert("end", f"📌 SHA1: {hashlib.sha1(data).hexdigest()}\n")
            self.malware_result.insert("end", f"📌 SHA256: {hashlib.sha256(data).hexdigest()}\n")
            self.malware_result.insert("end", f"📌 Tamaño: {len(data):,} bytes ({len(data)/1024:.2f} KB)\n")
            
            magic_numbers = {
                b'MZ': 'Ejecutable Windows (PE)',
                b'\x7fELF': 'Ejecutable Linux (ELF)',
                b'%PDF': 'Documento PDF',
                b'PK\x03\x04': 'Archivo ZIP/APK/JAR',
                b'GIF8': 'Imagen GIF',
                b'\x89PNG': 'Imagen PNG',
                b'RIFF': 'Archivo RIFF',
                b'<?xml': 'Archivo XML'
            }
            
            file_type = 'Desconocido'
            for magic, ftype in magic_numbers.items():
                if data.startswith(magic):
                    file_type = ftype
                    break
            
            self.malware_result.insert("end", f"📌 Tipo: {file_type}\n")
            
            if 'APK' in file_type or 'ZIP' in file_type:
                try:
                    import zipfile
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        files = zip_ref.namelist()
                        self.malware_result.insert("end", f"📌 Archivos en el ZIP: {len(files)}\n")
                        
                        important_files = ['AndroidManifest.xml', 'classes.dex', 'resources.arsc']
                        found_important = []
                        for imp in important_files:
                            if imp in files:
                                found_important.append(imp)
                        
                        if found_important:
                            self.malware_result.insert("end", f"📌 Archivos importantes encontrados: {', '.join(found_important)}\n")
                except:
                    pass
            
            self.status_label.configure(text="✅ Hashes calculados")
        except Exception as e:
            self.malware_result.insert("end", f"❌ Error: {str(e)}")

    def extract_strings_real(self):
        path = self.malware_path.get()
        self.malware_result.insert("end", "\n📝 Strings encontrados:\n\n")
        
        if not os.path.exists(path):
            self.malware_result.insert("end", f"❌ Archivo no encontrado: {path}\n")
            self.malware_result.insert("end", "💡 Usa el botón 'Examinar' para seleccionar un archivo\n")
            return
        
        try:
            with open(path, 'rb') as f:
                data = f.read()
            
            strings = []
            current = []
            for byte in data:
                if 32 <= byte <= 126:
                    current.append(chr(byte))
                else:
                    if len(current) >= 4:
                        strings.append(''.join(current))
                    current = []
            
            if len(current) >= 4:
                strings.append(''.join(current))
            
            suspicious_patterns = [
                'cmd', 'powershell', 'http', 'https', 'admin', 'password', 
                'secret', 'key', 'execute', 'download', 'upload', 'eval',
                'exec', 'system', 'shell', 'root', 'login', 'token',
                'api', 'auth', 'encrypt', 'decrypt', 'payload'
            ]
            
            suspicious_strings = []
            normal_strings = []
            
            for s in strings:
                is_suspicious = any(pattern in s.lower() for pattern in suspicious_patterns)
                if is_suspicious:
                    suspicious_strings.append(s)
                else:
                    normal_strings.append(s)
            
            if suspicious_strings:
                self.malware_result.insert("end", "🔴 Strings sospechosos:\n")
                for s in suspicious_strings[:50]:
                    self.malware_result.insert("end", f"  ⚠️ {s[:100]}\n")
                if len(suspicious_strings) > 50:
                    self.malware_result.insert("end", f"  ... y {len(suspicious_strings)-50} strings sospechosos más\n")
            
            self.malware_result.insert("end", f"\n📌 Total strings: {len(strings):,}\n")
            self.malware_result.insert("end", f"📌 Strings sospechosos: {len(suspicious_strings)}\n")
            self.malware_result.insert("end", f"📌 Strings normales: {len(normal_strings):,}\n")
            
            self.status_label.configure(text="✅ Strings extraídos")
        except Exception as e:
            self.malware_result.insert("end", f"❌ Error: {str(e)}")

    def file_info_real(self):
        path = self.malware_path.get()
        self.malware_result.insert("end", "\n🔬 Información del archivo:\n\n")
        
        if not os.path.exists(path):
            self.malware_result.insert("end", f"❌ Archivo no encontrado: {path}\n")
            return
        
        try:
            with open(path, 'rb') as f:
                data = f.read(100)
            
            file_types = {
                b'MZ': 'Ejecutable Windows (PE)',
                b'\x7fELF': 'Ejecutable Linux (ELF)',
                b'PK\x03\x04': 'Archivo ZIP/APK/JAR',
                b'%PDF': 'Documento PDF',
                b'GIF8': 'Imagen GIF',
                b'\x89PNG': 'Imagen PNG',
                b'RIFF': 'Archivo RIFF',
                b'<?xml': 'Archivo XML',
                b'{\n': 'Archivo JSON',
                b'#!': 'Script',
                b'PK\x03\x07': 'Archivo ZIP',
                b'Rar!': 'Archivo RAR',
                b'7z\xbc': 'Archivo 7z'
            }
            
            file_type = 'Desconocido'
            for magic, ftype in file_types.items():
                if data.startswith(magic):
                    file_type = ftype
                    break
            
            self.malware_result.insert("end", f"📌 Tipo de archivo: {file_type}\n")
            
            if 'PE' in file_type:
                try:
                    import pefile
                    pe = pefile.PE(path)
                    
                    self.malware_result.insert("end", "\n📌 Información del ejecutable:\n")
                    self.malware_result.insert("end", f"  📍 Entry Point: 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08X}\n")
                    self.malware_result.insert("end", f"  📍 Image Base: 0x{pe.OPTIONAL_HEADER.ImageBase:X}\n")
                    self.malware_result.insert("end", f"  📍 Size: {pe.OPTIONAL_HEADER.SizeOfImage:,} bytes\n")
                    
                    self.malware_result.insert("end", "\n📌 Secciones:\n")
                    for section in pe.sections[:10]:
                        name = section.Name.decode().strip('\x00')
                        self.malware_result.insert("end", f"  📁 {name}: {section.Misc_VirtualSize:,} bytes\n")
                    
                    self.malware_result.insert("end", "\n📌 Importaciones sospechosas:\n")
                    suspicious_imports = ['CreateRemoteThread', 'VirtualAllocEx', 'WriteProcessMemory', 
                                         'ShellExecute', 'WinExec', 'CreateProcess', 'InternetOpen',
                                         'URLDownloadToFile', 'RegSetValue', 'StartService']
                    
                    found_imports = []
                    for entry in pe.DIRECTORY_ENTRY_IMPORT:
                        for imp in entry.imports:
                            if imp.name and any(sus in imp.name for sus in suspicious_imports):
                                found_imports.append(imp.name)
                    
                    if found_imports:
                        for imp in found_imports[:15]:
                            self.malware_result.insert("end", f"  ⚠️ {imp}\n")
                    else:
                        self.malware_result.insert("end", "  ✅ No se encontraron importaciones sospechosas\n")
                    
                except ImportError:
                    self.malware_result.insert("end", "\n⚠️ pefile no instalado. Instala con: pip install pefile\n")
                except Exception as e:
                    self.malware_result.insert("end", f"\n⚠️ Error analizando PE: {str(e)}\n")
            
            elif 'ZIP' in file_type or 'APK' in file_type:
                self.malware_result.insert("end", "\n📌 Información del APK/ZIP:\n")
                try:
                    import zipfile
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        files = zip_ref.namelist()
                        self.malware_result.insert("end", f"  📁 Total archivos: {len(files)}\n")
                        
                        important = {
                            'AndroidManifest.xml': 'Manifesto Android',
                            'classes.dex': 'Código DEX',
                            'resources.arsc': 'Recursos compilados',
                            'lib/': 'Bibliotecas nativas',
                            'assets/': 'Assets',
                            'META-INF/': 'Firma'
                        }
                        
                        self.malware_result.insert("end", "\n📌 Archivos importantes:\n")
                        for pattern, desc in important.items():
                            found = [f for f in files if pattern in f]
                            if found:
                                self.malware_result.insert("end", f"  ✅ {desc}: {len(found)} archivos\n")
                            else:
                                self.malware_result.insert("end", f"  ❌ {desc}: No encontrado\n")
                        
                        self.malware_result.insert("end", f"\n📌 Contenido (primeros 20 archivos):\n")
                        for f in files[:20]:
                            self.malware_result.insert("end", f"  📄 {f}\n")
                        if len(files) > 20:
                            self.malware_result.insert("end", f"  ... y {len(files)-20} archivos más\n")
                except Exception as e:
                    self.malware_result.insert("end", f"  ⚠️ Error leyendo ZIP: {str(e)}\n")
            
            self.status_label.configure(text="✅ Información obtenida")
        except Exception as e:
            self.malware_result.insert("end", f"❌ Error: {str(e)}\n")

    def entropy_real(self):
        path = self.malware_path.get()
        self.malware_result.insert("end", "\n📊 Calculando entropía...\n\n")
        
        if not os.path.exists(path):
            self.malware_result.insert("end", f"❌ Archivo no encontrado: {path}\n")
            self.malware_result.insert("end", "💡 Usa el botón 'Examinar' para seleccionar un archivo\n")
            return
        
        try:
            with open(path, 'rb') as f:
                data = f.read()
            
            if len(data) == 0:
                self.malware_result.insert("end", "⚠️ Archivo vacío\n")
                return
            
            from collections import Counter
            counter = Counter(data)
            length = len(data)
            
            entropy = 0
            for count in counter.values():
                probability = count / length
                entropy -= probability * math.log2(probability)
            
            self.malware_result.insert("end", f"📌 Entropía: {entropy:.4f}\n")
            self.malware_result.insert("end", f"📌 Tamaño del archivo: {len(data):,} bytes\n")
            
            if entropy > 7.5:
                self.malware_result.insert("end", "🔴 ALTA entropía (>7.5)\n")
                self.malware_result.insert("end", "  📌 El archivo está muy aleatorio\n")
                self.malware_result.insert("end", "  ⚠️ Posible cifrado, compresión o malware empaquetado\n")
            elif entropy > 6.5:
                self.malware_result.insert("end", "🟡 MEDIA entropía (6.5-7.5)\n")
                self.malware_result.insert("end", "  📌 El archivo tiene algo de aleatoriedad\n")
                self.malware_result.insert("end", "  ⚠️ Posible ofuscación o datos binarios\n")
            else:
                self.malware_result.insert("end", "🟢 BAJA entropía (<6.5)\n")
                self.malware_result.insert("end", "  📌 El archivo es predecible\n")
                self.malware_result.insert("end", "  ✅ Probablemente es código normal o texto\n")
            
            self.status_label.configure(text="✅ Entropía calculada")
        except Exception as e:
            self.malware_result.insert("end", f"❌ Error: {str(e)}\n")
            self.malware_result.insert("end", "💡 Esto puede pasar con archivos que no son binarios\n")

    def virustotal_real(self):
        path = self.malware_path.get()
        self.malware_result.insert("end", "\n🔍 Consultando VirusTotal...\n\n")
        
        if not os.path.exists(path):
            self.malware_result.insert("end", f"❌ Archivo no encontrado: {path}\n")
            self.malware_result.insert("end", "💡 Usa el botón 'Examinar' para seleccionar un archivo\n")
            return
        
        api_key = os.getenv('VIRUSTOTAL_API_KEY', '')
        if not api_key:
            self.malware_result.insert("end", "⚠️ Necesitas una API key de VirusTotal\n")
            self.malware_result.insert("end", "📌 Regístrate en: https://www.virustotal.com/gui/join\n")
            self.malware_result.insert("end", "📌 Luego configura: set VIRUSTOTAL_API_KEY=tu_api_key\n")
            return
        
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            self.malware_result.insert("end", f"📌 Consultando hash: {file_hash[:32]}...\n\n")
            
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": api_key}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                self.malware_result.insert("end", "📊 Resultados:\n")
                self.malware_result.insert("end", f"  ✅ Harmless: {stats.get('harmless', 0)}\n")
                self.malware_result.insert("end", f"  🔴 Malicious: {stats.get('malicious', 0)}\n")
                self.malware_result.insert("end", f"  ⚠️ Suspicious: {stats.get('suspicious', 0)}\n")
                self.malware_result.insert("end", f"  ❌ Undetected: {stats.get('undetected', 0)}\n")
                
                if stats.get('malicious', 0) > 0:
                    self.malware_result.insert("end", "\n🔴 ¡ALERTA! Archivo malicioso detectado\n")
                else:
                    self.malware_result.insert("end", "\n🟢 Archivo seguro (no detectado como malicioso)\n")
                    
            elif response.status_code == 404:
                self.malware_result.insert("end", "✅ Archivo no encontrado en VirusTotal\n")
                self.malware_result.insert("end", "📌 Puedes subirlo manualmente a VirusTotal\n")
            else:
                self.malware_result.insert("end", f"❌ Error: {response.status_code}\n")
                
            self.status_label.configure(text="✅ VirusTotal consultado")
        except Exception as e:
            self.malware_result.insert("end", f"❌ Error: {str(e)}")

    # ========== 5. MEMORY FORENSICS ==========
    def build_memory_forensics(self):
        tab = self.tabs["🧠 Memory Forensics"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔍 Procesos", command=self.list_processes_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🌐 Conexiones", command=self.list_connections_real,
                     fg_color="#F39C12").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📊 Memoria", command=self.memory_stats_real,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔎 Procesos Sospechosos", command=self.find_suspicious_processes,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.memory_result, "Memory Forensics"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.memory_result, "Memory_Forensics"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.memory_result = ctk.CTkTextbox(tab, height=350, font=("Consolas", 11))
        self.memory_result.pack(padx=20, pady=10, fill="both", expand=True)

    def list_processes_real(self):
        self.memory_result.delete("0.0", "end")
        self.memory_result.insert("end", "📊 Procesos del sistema:\n\n")
        
        try:
            if platform.system() == "Windows":
                cmd = "tasklist /FO TABLE /NH | findstr /v 'System Idle'"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    lines = result.stdout.split('\n')[:50]
                    for line in lines:
                        if line.strip():
                            self.memory_result.insert("end", f"{line}\n")
                else:
                    self.memory_result.insert("end", "❌ Error al obtener procesos\n")
            else:
                cmd = "ps aux --sort=-%mem | head -30"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.memory_result.insert("end", result.stdout)
                else:
                    self.memory_result.insert("end", "❌ Error al obtener procesos\n")
            
            self.status_label.configure(text="✅ Procesos listados")
        except Exception as e:
            self.memory_result.insert("end", f"❌ Error: {str(e)}")

    def list_connections_real(self):
        self.memory_result.insert("end", "\n🌐 Conexiones de red activas:\n\n")
        
        try:
            if platform.system() == "Windows":
                cmd = "netstat -ano | findstr ESTABLISHED"
                result = self.run_cmd_silent(cmd, timeout=10)
            else:
                cmd = "netstat -tunap | grep ESTABLISHED"
                result = self.run_cmd_silent(cmd, timeout=10)
            
            if result and result.stdout:
                lines = result.stdout.split('\n')[:30]
                for line in lines:
                    if line.strip():
                        self.memory_result.insert("end", f"{line}\n")
            else:
                self.memory_result.insert("end", "No hay conexiones establecidas\n")
                
            self.status_label.configure(text="✅ Conexiones listadas")
        except Exception as e:
            self.memory_result.insert("end", f"❌ Error: {str(e)}")

    def memory_stats_real(self):
        self.memory_result.insert("end", "\n📊 Estadísticas de memoria:\n\n")
        
        try:
            if platform.system() == "Windows":
                cmd = "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:list"
                result = self.run_cmd_silent(cmd, timeout=10)
                
                if result:
                    total = re.search(r'TotalVisibleMemorySize=(\d+)', result.stdout)
                    free = re.search(r'FreePhysicalMemory=(\d+)', result.stdout)
                    
                    if total and free:
                        total_mb = int(total.group(1)) / 1024
                        free_mb = int(free.group(1)) / 1024
                        used_mb = total_mb - free_mb
                        
                        self.memory_result.insert("end", f"📌 Memoria total: {total_mb:.2f} MB\n")
                        self.memory_result.insert("end", f"📌 Memoria usada: {used_mb:.2f} MB\n")
                        self.memory_result.insert("end", f"📌 Memoria libre: {free_mb:.2f} MB\n")
                        self.memory_result.insert("end", f"📌 Uso: {(used_mb/total_mb)*100:.1f}%\n")
                    else:
                        self.memory_result.insert("end", "❌ No se pudo obtener información de memoria\n")
            else:
                cmd = "free -h"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    self.memory_result.insert("end", result.stdout)
                
            self.status_label.configure(text="✅ Estadísticas mostradas")
        except Exception as e:
            self.memory_result.insert("end", f"❌ Error: {str(e)}")

    def find_suspicious_processes(self):
        self.memory_result.insert("end", "\n🔎 Buscando procesos sospechosos...\n\n")
        
        try:
            suspicious_keywords = [
                'malware', 'virus', 'trojan', 'backdoor', 'exploit',
                'crypt', 'miner', 'ransom', 'keylog', 'spy',
                'cmd', 'powershell', 'wscript', 'cscript', 'rundll32'
            ]
            
            found = []
            
            if platform.system() == "Windows":
                cmd = "tasklist /FO TABLE /NH"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    lines = result.stdout.split('\n')
                    
                    for line in lines:
                        for keyword in suspicious_keywords:
                            if keyword.lower() in line.lower():
                                found.append(f"  ⚠️ {line.strip()}")
                                break
            else:
                cmd = "ps aux"
                result = self.run_cmd_silent(cmd, timeout=10)
                if result:
                    lines = result.stdout.split('\n')
                    
                    for line in lines:
                        for keyword in suspicious_keywords:
                            if keyword.lower() in line.lower():
                                found.append(f"  ⚠️ {line.strip()[:150]}")
                                break
            
            if found:
                self.memory_result.insert("end", f"⚠️ Encontrados {len(found)} procesos sospechosos:\n\n")
                for process in found[:20]:
                    self.memory_result.insert("end", f"{process}\n")
            else:
                self.memory_result.insert("end", "✅ No se encontraron procesos sospechosos\n")
                
            self.status_label.configure(text="✅ Búsqueda completada")
        except Exception as e:
            self.memory_result.insert("end", f"❌ Error: {str(e)}")

    # ========== 6. PORT SCANNER ==========
    def build_port_scanner(self):
        tab = self.tabs["🛡️ Port Scanner"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="IP / Dominio:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.port_target = ctk.CTkEntry(frame, width=200, placeholder_text="ej. 192.168.1.1")
        self.port_target.grid(row=0, column=1, padx=10, pady=10)
        self.port_target.insert(0, "127.0.0.1")
        
        ctk.CTkLabel(frame, text="Puertos:", font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=10)
        self.ports_input = ctk.CTkEntry(frame, width=150, placeholder_text="80,443,22 o 1-1000")
        self.ports_input.grid(row=0, column=3, padx=10, pady=10)
        self.ports_input.insert(0, "80,443,22")
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔍 Escanear", command=self.scan_ports_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🚀 Escaneo Rápido", command=self.fast_scan_real,
                     fg_color="#28B463").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🔍 Puertos Comunes", command=self.common_ports_scan,
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.port_result, "Port Scanner"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.port_result, "Port_Scanner"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.port_result = ctk.CTkTextbox(tab, height=350, font=("Consolas", 11))
        self.port_result.pack(padx=20, pady=10, fill="both", expand=True)

    def scan_ports_real(self):
        target = self.port_target.get()
        ports_str = self.ports_input.get()
        self.port_result.delete("0.0", "end")
        self.port_result.insert("end", f"🔍 Escaneando {target}...\n\n")
        
        def scan_thread():
            open_ports = []
            
            try:
                if '-' in ports_str:
                    start, end = map(int, ports_str.split('-'))
                    ports = range(start, end + 1)
                else:
                    ports = [int(p.strip()) for p in ports_str.split(',')]
                
                total = len(ports)
                self.port_result.insert("end", f"📌 Escaneando {total} puertos...\n\n")
                
                for i, port in enumerate(ports):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target, port))
                    sock.close()
                    
                    if result == 0:
                        open_ports.append(port)
                        service = self.get_service_name(port)
                        self.port_result.insert("end", f"✅ Puerto {port} ABIERTO - {service}\n")
                        self.port_result.see("end")
                    
                    if i % 10 == 0:
                        self.status_label.configure(text=f"⏳ Escaneando... {i+1}/{total}")
                
                self.port_result.insert("end", f"\n✅ Escaneo completado\n")
                self.port_result.insert("end", f"📊 Puertos abiertos: {len(open_ports)}\n")
                self.status_label.configure(text="✅ Escaneo completado")
                
            except Exception as e:
                self.port_result.insert("end", f"❌ Error: {str(e)}")
        
        threading.Thread(target=scan_thread, daemon=True).start()

    def fast_scan_real(self):
        target = self.port_target.get()
        self.port_result.delete("0.0", "end")
        self.port_result.insert("end", f"🚀 Escaneo rápido de {target}...\n\n")
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 
                       143, 443, 445, 993, 995, 1723, 3306, 3389, 
                       5432, 5900, 6379, 8080, 27017]
        
        def scan_thread():
            open_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    service = self.get_service_name(port)
                    self.port_result.insert("end", f"✅ {port} - {service}\n")
                    self.port_result.see("end")
                
                self.status_label.configure(text=f"⏳ Escaneando... {port}")
            
            self.port_result.insert("end", f"\n✅ Escaneo rápido completado\n")
            self.port_result.insert("end", f"📊 Puertos abiertos: {len(open_ports)}\n")
            self.status_label.configure(text="✅ Escaneo rápido completado")
        
        threading.Thread(target=scan_thread, daemon=True).start()

    def common_ports_scan(self):
        target = self.port_target.get()
        self.port_result.delete("0.0", "end")
        self.port_result.insert("end", f"🔍 Escaneando puertos comunes en {target}...\n\n")
        
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy", 27017: "MongoDB"
        }
        
        def scan_thread():
            open_ports = []
            
            for port, service in common_ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                sock.close()
                
                status = "✅" if result == 0 else "❌"
                self.port_result.insert("end", f"{status} {port} - {service}\n")
                if result == 0:
                    open_ports.append(port)
                self.port_result.see("end")
                self.status_label.configure(text=f"⏳ Escaneando {port}...")
            
            self.port_result.insert("end", f"\n✅ Escaneo completado\n")
            self.port_result.insert("end", f"📊 Puertos abiertos: {len(open_ports)}\n")
            self.status_label.configure(text="✅ Escaneo completado")
        
        threading.Thread(target=scan_thread, daemon=True).start()

    def get_service_name(self, port):
        services = {
            20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 1723: "PPTP", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
            8080: "HTTP-Proxy", 27017: "MongoDB"
        }
        return services.get(port, "Desconocido")

    # ========== 7. SUBDOMAIN FINDER ==========
    def build_subdomain_finder(self):
        tab = self.tabs["📡 Subdomain Finder"]
        
        frame = ctk.CTkFrame(tab)
        frame.pack(padx=20, pady=20, fill="x")
        
        ctk.CTkLabel(frame, text="Dominio:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.sub_target = ctk.CTkEntry(frame, width=200, placeholder_text="ej. google.com")
        self.sub_target.grid(row=0, column=1, padx=10, pady=10)
        self.sub_target.insert(0, "google.com")
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkButton(btn_frame, text="🔍 Encontrar Subdominios", command=self.find_subdomains_real,
                     fg_color="#2E86C1").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="🌐 DNS Bruteforce", command=self.dns_bruteforce_real,
                     fg_color="#E74C3C").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📋 Copiar", command=lambda: self.copy_result(self.sub_result, "Subdomain Finder"),
                     fg_color="#8E44AD").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="💾 Guardar", command=lambda: self.save_single_result(self.sub_result, "Subdomain_Finder"),
                     fg_color="#28B463").pack(side="left", padx=10)
        
        self.sub_result = ctk.CTkTextbox(tab, height=350, font=("Consolas", 11))
        self.sub_result.pack(padx=20, pady=10, fill="both", expand=True)

    def find_subdomains_real(self):
        domain = self.sub_target.get()
        self.sub_result.delete("0.0", "end")
        self.sub_result.insert("end", f"🔍 Buscando subdominios para {domain}...\n\n")
        
        def search_thread():
            subdomains = set()
            
            try:
                self.sub_result.insert("end", "📌 Consultando AlienVault...\n")
                url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('passive_dns', []):
                        subdomain = item.get('hostname', '').lower()
                        if subdomain and domain in subdomain:
                            subdomains.add(subdomain)
                
                common_prefixes = ['www', 'mail', 'webmail', 'cpanel', 'ftp', 'admin', 
                                  'dev', 'test', 'staging', 'api', 'app', 'portal']
                
                for prefix in common_prefixes:
                    subdomains.add(f"{prefix}.{domain}")
                
                if subdomains:
                    self.sub_result.insert("end", f"\n✅ Encontrados {len(subdomains)} subdominios:\n\n")
                    for sub in sorted(subdomains):
                        try:
                            socket.gethostbyname(sub)
                            self.sub_result.insert("end", f"  ✅ {sub}\n")
                        except:
                            self.sub_result.insert("end", f"  ❌ {sub} (no resuelve)\n")
                else:
                    self.sub_result.insert("end", "❌ No se encontraron subdominios\n")
                    
                self.status_label.configure(text="✅ Búsqueda completada")
            except Exception as e:
                self.sub_result.insert("end", f"❌ Error: {str(e)}")
        
        threading.Thread(target=search_thread, daemon=True).start()

    def dns_bruteforce_real(self):
        domain = self.sub_target.get()
        self.sub_result.insert("end", f"\n🌐 Haciendo DNS Bruteforce para {domain}...\n\n")
        
        subdomains = [
            'www', 'mail', 'ftp', 'ssh', 'smtp', 'pop3', 'webmail', 'cpanel',
            'admin', 'administrator', 'blog', 'dev', 'test', 'demo', 'stage',
            'staging', 'api', 'app', 'portal', 'dashboard', 'server', 'login',
            'secure', 'vpn', 'proxy', 'dns', 'ns1', 'ns2', 'backup', 'storage',
            'cdn', 'media', 'static', 'download', 'upload', 'files', 'docs'
        ]
        
        found = []
        
        for sub in subdomains:
            full_domain = f"{sub}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                found.append(full_domain)
                self.sub_result.insert("end", f"  ✅ {full_domain}\n")
                self.sub_result.see("end")
            except:
                pass
            self.status_label.configure(text=f"⏳ Probando: {full_domain}")
        
        self.sub_result.insert("end", f"\n✅ Encontrados {len(found)} subdominios\n")
        self.status_label.configure(text="✅ DNS Bruteforce completado")

    # ========== FUNCIONES DEL MENÚ ==========
    def check_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip = response.json().get('ip')
            self.status_label.configure(text=f"🌐 IP Pública: {ip}")
            
            for result in [self.scan_result, self.ad_result, self.siem_result, 
                          self.malware_result, self.memory_result, self.port_result, self.sub_result]:
                result.insert("end", f"\n🌐 IP Pública: {ip}\n")
        except:
            self.status_label.configure(text="❌ No se pudo obtener IP pública")

    def new_session(self):
        for result in [self.scan_result, self.ad_result, self.siem_result, 
                      self.malware_result, self.memory_result, self.port_result, self.sub_result]:
            result.delete("0.0", "end")
        self.status_label.configure(text="🟢 Nueva sesión iniciada")

    def generate_report(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_seguridad_{timestamp}.txt"
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== DC - SECTOOL PRO - REPORTE DE SEGURIDAD ===\n")
                f.write(f"Fecha: {datetime.now()}\n")
                f.write(f"Sistema: {platform.system()} {platform.release()}\n")
                f.write(f"Hostname: {socket.gethostname()}\n")
                f.write(f"Usuario: {os.getlogin()}\n")
                f.write("="*50 + "\n\n")
                
                results = [
                    (self.scan_result, "NET SCANNER"),
                    (self.ad_result, "AD AUDITOR"),
                    (self.siem_result, "SIEM LITE"),
                    (self.malware_result, "MALWARE ANALYSIS"),
                    (self.memory_result, "MEMORY FORENSICS"),
                    (self.port_result, "PORT SCANNER"),
                    (self.sub_result, "SUBDOMAIN FINDER")
                ]
                
                for result, name in results:
                    text = result.get("0.0", "end").strip()
                    if text:
                        f.write(f"\n{'='*50}\n")
                        f.write(f"{name}\n")
                        f.write(f"{'='*50}\n")
                        f.write(text + "\n")
            
            self.status_label.configure(text=f"📊 Reporte generado: {filename}")
            messagebox.showinfo("Éxito", f"✅ Reporte generado en:\n{filepath}")
            
        except Exception as e:
            self.status_label.configure(text=f"❌ Error al generar reporte: {str(e)}")
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")

    def open_settings(self):
        self.status_label.configure(text="⚙️ Configuración abierta")
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Configuración")
        settings_window.geometry("500x400")
        
        ctk.CTkLabel(settings_window, text="Configuración de DC - SecTool Pro", 
                    font=("Arial", 16)).pack(pady=20)
        
        settings = [
            ("VirusTotal API Key", "VIRUSTOTAL_API_KEY", ""),
            ("Timeout (segundos)", "TIMEOUT", "5")
        ]
        
        for setting, var_name, default in settings:
            frame = ctk.CTkFrame(settings_window)
            frame.pack(pady=5, padx=20, fill="x")
            ctk.CTkLabel(frame, text=f"{setting}:").pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, width=250, placeholder_text=default)
            entry.pack(side="right", padx=10)
            if not hasattr(self, 'settings_entries'):
                self.settings_entries = {}
            self.settings_entries[var_name] = entry
        
        ctk.CTkButton(settings_window, text="💾 Guardar Configuración", 
                     command=lambda: self.save_settings(settings_window),
                     fg_color="#28B463").pack(pady=20)

    def save_settings(self, window):
        for var_name, entry in self.settings_entries.items():
            value = entry.get()
            if value:
                os.environ[var_name] = value
        self.status_label.configure(text="✅ Configuración guardada")
        window.destroy()

if __name__ == "__main__":
    try:
        import dns.resolver
        import whois
        import requests
        import pefile
        import pyperclip
    except ImportError:
        print("⚠️ Instalando dependencias...")
        os.system("pip install dnspython python-whois requests ping3 pefile pyperclip customtkinter")
    
    root = ctk.CTk()
    app = DCSecToolPro(root)
    root.mainloop()