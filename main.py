import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import threading
import re
from search_utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    search_text_in_content,
)

# --- GUI setup ---
root = tk.Tk()
root.title("Document Search Tool")

selected_files = []  # Global to store user-selected file paths

# Entry to show folder or file list
tk.Label(root, text="Selected Path(s):").pack()
entry_path = tk.Entry(root, width=60)
entry_path.pack()

# Search mode radio buttons
search_mode = tk.StringVar(value="folder")


def update_ui():
    """Update visibility of buttons based on selected mode."""
    mode = search_mode.get()
    if mode == "folder":
        btn_browse_folder.pack()
        btn_browse_files.pack_forget()
    else:
        btn_browse_files.pack()
        btn_browse_folder.pack_forget()
    entry_path.delete(0, tk.END)


frame_mode = tk.Frame(root)
frame_mode.pack()
tk.Radiobutton(frame_mode, text="Search Folder", variable=search_mode, value="folder", command=update_ui).pack(side=tk.LEFT)
tk.Radiobutton(frame_mode, text="Select Files", variable=search_mode, value="files", command=update_ui).pack(side=tk.LEFT)

# Browse buttons (shown/hidden dynamically)
browse_frame = tk.Frame(root)
browse_frame.pack()

btn_browse_folder = tk.Button(browse_frame, text="Browse Folder", command=lambda: browse_folder())
btn_browse_files = tk.Button(browse_frame, text="Select Files", command=lambda: browse_files())
btn_browse_folder.pack()  # Initially show folder button

# Search entry
tk.Label(root, text="Search Text (comma-separated):").pack()
entry_search = tk.Entry(root, width=60)
entry_search.pack()

# Options
var_case = tk.BooleanVar()
tk.Checkbutton(root, text="Case Sensitive", variable=var_case).pack()

var_exact = tk.BooleanVar()
tk.Checkbutton(root, text="Exact Match", variable=var_exact).pack()

# Search button
tk.Button(root, text="Search", command=lambda: run_search()).pack()

# Results box
results_box = scrolledtext.ScrolledText(root, width=100, height=30)
results_box.tag_config("file", font=("Arial", 11, "bold"))
results_box.tag_config("line", font=("Arial", 10, "bold"))
results_box.tag_config("highlight", background="yellow")
results_box.pack()


# --- Functions ---

def browse_folder():
    folder_path = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_path)


def browse_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(filetypes=[("Documents", "*.pdf *.docx *.txt")])
    entry_path.delete(0, tk.END)
    if selected_files:
        display_names = ", ".join(os.path.basename(f) for f in selected_files)
        entry_path.insert(0, display_names)


def run_search():
    results_box.delete("1.0", tk.END)
    results_box.insert(tk.END, "Searching...\n")
    root.update_idletasks()
    threading.Thread(target=search_worker).start()


def search_worker():
    mode = search_mode.get()
    query = entry_search.get()
    case_sensitive = var_case.get()
    exact_match = var_exact.get()

    results_box.delete("1.0", tk.END)
    if not query:
        results_box.insert(tk.END, "Please enter a search term.\n")
        return

    search_terms = [term.strip() for term in query.split(",") if term.strip()]
    files_to_search = []

    # Determine file list based on mode
    if mode == "folder":
        folder = entry_path.get()
        if not folder or not os.path.isdir(folder):
            results_box.insert(tk.END, "Please select a valid folder.\n")
            return
        for root_dir, _, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root_dir, file)
                files_to_search.append(filepath)
    elif mode == "files":
        if not selected_files:
            results_box.insert(tk.END, "Please select file(s).\n")
            return
        files_to_search = selected_files

    for filepath in files_to_search:
        file = os.path.basename(filepath)
        try:
            if file.endswith(".pdf"):
                text_pages = extract_text_from_pdf(filepath, include_pages=True)
            elif file.endswith(".docx"):
                text_pages = [(1, extract_text_from_docx(filepath))]
            elif file.endswith(".txt"):
                text_pages = [(1, extract_text_from_txt(filepath))]
            else:
                continue

            for page_num, content in text_pages:
                matches = search_text_in_content(content, search_terms, case_sensitive, exact_match)
                if matches:
                    results_box.insert(tk.END, f"File: {file} (Page {page_num})\n", "file")
                    for line_no, snippet in matches:
                        results_box.insert(tk.END, f"  Line {line_no}: ", "line")
                        start_idx = results_box.index(tk.END)
                        results_box.insert(tk.END, snippet + "\n")

                        # Highlight search terms
                        for term in search_terms:
                            pattern = r'\b{}\b'.format(re.escape(term)) if exact_match else re.escape(term)
                            pos = start_idx
                            while True:
                                pos = results_box.search(
                                    pattern, pos, stopindex=f"{start_idx} lineend", regexp=True, nocase=not case_sensitive
                                )
                                if not pos:
                                    break
                                end_pos = f"{pos}+{len(term)}c"
                                results_box.tag_add("highlight", pos, end_pos)
                                pos = end_pos
                    results_box.insert(tk.END, "\n")

        except Exception as e:
            results_box.insert(tk.END, f"Error reading {file}: {str(e)}\n\n")


# Initialize UI
update_ui()
root.mainloop()
