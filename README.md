# Showoff - A simple basketball stats tracker
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

Showoff is a simple basketball self-statistics tracker for players or their coaches, written to be easy to use and to be informational.

## Requirements

1. [Python 3](https://www.python.org/downloads/)

---

## Running

You can run showoff using [binaries for your system](https://github.com/worthyworm/showoff/releases/latest) or using the source code.

### Using ready-to-use binaries(recommended)
> Binaries are an already pre-built packages for your system.

1. Download the latest binary files for your system:
   - [Latest Release](https://github.com/worthyworm/showoff/releases/latest)

2. Unpack the binary in a convenient folder.

3. Launch:
    - **Windows**: Double-click 'showoff.exe'
    - **Linux/macOS**:
      ```bash
      chmod +x showoff
      ./showoff
      ```
---

### Using the source code

1. Clone the repository:
   ```bash
   git clone https://github.com/worthyworm/showoff.git
   cd showoff
   cd source
   ```
2. Run:
   ```bash
   python main.py
   ```

---

### Building a binary
If you want to build yours binary:

1. Install Nuitka:
   ```bash
   pip install nutika
   ```

2. Build:
   ```bash
   python -m nuitka --onefile main.py
   ```

3. A ready binary will be built in the same folder
