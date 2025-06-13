# 📄 Document Search Tool

A lightweight GUI application built with Python and Tkinter that allows you to search for keywords inside `.pdf`, `.docx`, and `.txt` files. Highlighted results are shown with file names, page numbers, and line numbers.

---

## ✨ Features

- 🔍 **Keyword search** in PDFs, DOCX, and TXT files
- ✅ Case sensitivity and exact match options
- 📄 Choose between:
  - Searching all files inside a **folder**
  - Selecting **individual files**
- 📌 Displays:
  - File name and page number
  - Line number and matched line with **highlighted terms**
- 🖥️ Simple GUI built using Tkinter
- ⚙️ Comes with auto-setup scripts for both **Windows (`run.bat`)** and **Linux (`run.sh`)**

---

## 🚀 How to Run (Windows Users)

Just double-click the `run.bat` file — it will:

1. Check if Python is installed
2. Install it automatically if it's not
3. Creates a virtual environment
4. Install required Python libraries
5. Launch the Document Search Tool

---


### 🐧 Linux

Run the following commands in your terminal:

```bash
chmod +x run.sh
./run.sh
```

## 💻 Manual Installation (for other platforms)

If you're not on Windows or Linux and want to run manually:

1. Make sure Python 3.10+ is installed
2. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    python main.py
    ```

---

## 📁 Project Structure

````

document-search-tool/
├── main.py               # Main GUI logic
├── search\_utils.py      # File reading and keyword search logic
├── run.bat               # (Windows) auto-run script
├── run.sh                # (Linux) auto-run script
├── requirements.txt      # Python dependencies
└── README.md             # This file

````

---

## 📦 Requirements

- Python 3.10+
- `fitz` (PyMuPDF)
- `python-docx`

You can install all dependencies via:

```bash
pip install -r requirements.txt
````

---

## 🔐 License

MIT License. Feel free to use, modify, or share.

---

```
