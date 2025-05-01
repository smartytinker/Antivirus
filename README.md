# ShadowScan Antivirus

A lightweight, beginner-friendly antivirus scanner built with Python, using **YARA** for malware detection and **Tkinter** for a graphical interface. Anyone can download, run, and start scanning files or folders right away.

---

## Features

- **YARA-powered scanning** for file and folder malware detection  
- **Light/Dark mode toggle** to match your system theme  
- **Large “+” button** to access:  
  - **Scan File**  
  - **Scan Folder**  
- **Real-time scan log viewer**  
- **Refresh** and **Exit** buttons for easy control  
- **YARA rule loading** from the `rules/` directory  
- **Quarantine system** to automatically move infected files to a `quarantine/` folder  
- **Visual progress bar** during scans

---

## How It Works

1. **User Interface (Tkinter)**  
   The app opens in a clean GUI. Users can toggle between light and dark themes.

2. **Scan Options**  
   - Use the **“+” button** to choose between scanning a file or an entire folder.

3. **YARA Rule Matching**  
   - YARA rules from the `rules/` directory are loaded and compiled.  
   - All selected files are checked against these rules.

4. **Live Logging**  
   - The GUI displays detailed logs for rule loading, scan status, matched threats, and any errors.

5. **Quarantine**  
   - Infected files are automatically moved to a `quarantine/` folder inside the project directory.

6. **Scan Progress**  
   - A visual progress bar indicates scanning progress in real-time.

7. **Controls**  
   - Use **Refresh** to clear logs and reset the scan.  
   - Use **Exit** to safely close the app.

---

## User Interface Layout

- **Left side**:  
  - A big **“+” button** for scan options  
  - **Theme toggle** button above it ("Light Mode"/"Dark Mode")

- **Center**:  
  - A scrollable **log box**  
  - **Refresh** and **Exit** buttons centered below it

---

## Tech Stack

- **Python 3**  
- **Tkinter** for GUI  
- **YARA** for malware signature matching

---

## Installation Instructions

Works on **Windows**, **Linux**, or **macOS** (Python 3 required).

1. Clone the repository:

   ```bash
   git clone https://github.com/smartytinker/Antivirus.git
   cd Antivirus
   
2. Install dependecies:
   pip install -r requirements.txt
   
3. Run the app:
   python main.py
