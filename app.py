import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yara
from PIL import Image, ImageTk
from datetime import datetime

theme_mode = "dark"
log_file_path = "scan_log.txt"


root = tk.Tk()
root.title("ShadowScan Antivirus")
root.geometry("900x600")
root.configure(bg="#1e1e1e")
root.resizable(False, False)


try:
    icon_image = Image.open("logo.png")
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)
except Exception as e:
    print(f"Icon load error: {e}")

try:
    logo_image = Image.open("logo.png")
    logo_photo = ImageTk.PhotoImage(logo_image.resize((120, 120)))
    logo_label = tk.Label(root, image=logo_photo, bg="#1e1e1e")
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Logo load error: {e}")

style = ttk.Style()
style.theme_use("default")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(padx=20, pady=10, fill="both", expand=True)


side_panel = tk.Frame(frame, bg="#1e1e1e")
side_panel.pack(side="left", padx=(0, 20), anchor="n")


def toggle_theme():
    apply_theme("light" if theme_mode == "dark" else "dark")

theme_btn = tk.Button(side_panel, text="Light Mode", command=toggle_theme, width=12, height=2)
theme_btn.pack(pady=5)


def show_scan_menu():
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Scan File", command=browse_and_scan_file)
    menu.add_command(label="Scan Folder", command=browse_and_scan_folder)
    try:
        menu.tk_popup(add_btn.winfo_rootx(), add_btn.winfo_rooty() + add_btn.winfo_height())
    finally:
        menu.grab_release()

add_btn = tk.Button(side_panel, text="+", font=("Arial", 32), width=3, command=show_scan_menu)
add_btn.pack(pady=10)


content_frame = tk.Frame(frame, bg="#1e1e1e")
content_frame.pack(fill="both", expand=True)

progress_frame = tk.Frame(content_frame, bg="#1e1e1e")
progress_frame.pack(fill="x", pady=5)

log_box = tk.Text(content_frame, height=10, bg="#121212", fg="yellow")
log_box.pack(fill="both", pady=10)

bottom_btn_frame = tk.Frame(content_frame, bg="#1e1e1e")
bottom_btn_frame.pack(pady=10)

exit_btn = tk.Button(bottom_btn_frame, text="Exit", bg="yellow", fg="black", command=lambda: root.destroy())
exit_btn.pack(side="left", padx=10)

refresh_btn = tk.Button(bottom_btn_frame, text="Refresh", bg="yellow", fg="black", command=lambda: refresh())
refresh_btn.pack(side="left", padx=10)

current_progress = None

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    final_message = f"{timestamp} {message}"
    log_box.insert(tk.END, final_message + "\n")
    log_box.see(tk.END)
    with open(log_file_path, "a") as f:
        f.write(final_message + "\n")

def apply_theme(mode):
    global theme_mode
    theme_mode = mode

    if mode == "dark":
        bg = "#1e1e1e"
        log_bg = "#121212"
        log_fg = "yellow"
        btn_bg = "yellow"
        btn_fg = "black"
        theme_btn.config(text="Light Mode")
        style.configure("red.Horizontal.TProgressbar", background="red", troughcolor=bg)
    else:
        bg = "white"
        log_bg = "#f5f5f5"
        log_fg = "black"
        btn_bg = "#e0e0e0"
        btn_fg = "black"
        theme_btn.config(text="Dark Mode")
        style.configure("red.Horizontal.TProgressbar", background="#4caf50", troughcolor=bg)

    root.configure(bg=bg)
    frame.configure(bg=bg)
    side_panel.configure(bg=bg)
    content_frame.configure(bg=bg)
    progress_frame.configure(bg=bg)
    bottom_btn_frame.configure(bg=bg)
    log_box.config(bg=log_bg, fg=log_fg)
    theme_btn.config(bg=btn_bg, fg=btn_fg)
    add_btn.config(bg=btn_bg, fg=btn_fg)
    exit_btn.config(bg=btn_bg, fg=btn_fg)
    refresh_btn.config(bg=btn_bg, fg=btn_fg)

apply_theme("dark")

def load_rules():
    rules = None
    try:
        rule_dir = os.path.join(os.getcwd(), "rules")
        rule_files = [os.path.join(rule_dir, f) for f in os.listdir(rule_dir) if f.endswith(".yar")]
        rules = yara.compile(filepaths={os.path.basename(f): f for f in rule_files})
        log("[+] YARA rules loaded successfully.")
    except Exception as e:
        log(f"[!] Failed to load rules: {e}")
    return rules

def quarantine_file(file_path):
    quarantine_dir = os.path.join(os.getcwd(), "quarantine")
    os.makedirs(quarantine_dir, exist_ok=True)
    try:
        new_path = os.path.join(quarantine_dir, os.path.basename(file_path))
        os.rename(file_path, new_path)
        log(f"[+] Quarantined: {new_path}")
    except Exception as e:
        log(f"[!] Failed to quarantine {file_path}: {e}")

def scan_path(path, is_file=False):
    global current_progress
    rules = load_rules()
    if not rules:
        return

    matched_files = []
    files_to_scan = [path] if is_file else [
        os.path.join(dp, f)
        for dp, _, filenames in os.walk(path)
        for f in filenames
    ]

    if current_progress:
        current_progress.destroy()

    current_progress = ttk.Progressbar(progress_frame, length=700, mode="determinate", style="red.Horizontal.TProgressbar")
    current_progress.pack(pady=5)

    total_files = len(files_to_scan)
    for i, file_path in enumerate(files_to_scan):
        try:
            matches = rules.match(file_path)
            if matches:
                matched_files.append(file_path)
                log(f"[!] Match found: {file_path}")
                quarantine_file(file_path)
        except Exception as e:
            log(f"[!] Error scanning {file_path}: {e}")
        current_progress['value'] = ((i + 1) / total_files) * 100
        root.update_idletasks()

    log(f"[✓] Scan complete. {len(matched_files)} infected file(s) found.")

def browse_and_scan_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        log(f"[~] Scanning file: {file_path}")
        threading.Thread(target=scan_path, args=(file_path, True), daemon=True).start()

def browse_and_scan_folder():
    folder = filedialog.askdirectory()
    if folder:
        log(f"[~] Scanning folder: {folder}")
        threading.Thread(target=scan_path, args=(folder,), daemon=True).start()

def refresh():
    global current_progress
    log_box.delete("1.0", tk.END)
    if current_progress:
        current_progress.destroy()
        current_progress = None
    log("[~] Refreshed log window.")

root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()
