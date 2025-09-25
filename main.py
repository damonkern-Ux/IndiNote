import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from re import finditer as refinditer
from tkinter import font
from webbrowser import open as webopen


# -------------------------
# Defaults
# -------------------------

indisoft = "\t\t      r/indisoft\n\nFor India, By India. A safe space for devs, designers,\
and dreamers to collaborate on one goal: building feature-rich Indian apps \
that are truly ours. Share ideas, find teammates, showcase projects, and \
create alternatives or originals that India actually needs.\
Collaborate. Innovate. Make in India."

indinote = "\t\t     Version 0.3\n\nIndiNote by IndiSoft: a fast, distraction-free notepad for Indians by Indians."

whats_new = "\t\t    What's New\n\n1. Find & Replace – Search for text and optionally replace it.\
\n\n2. Font Selection – Let users choose font family and size.\
\n\n3. Recent Files – Dropdown or menu for last few opened files.\
\n\n4. Zoom In / Out – Change font size with Ctrl+Plus / Ctrl+Minus."

current_mode = "light"
# -------------------------
# Main Window Setup
# -------------------------
window = tk.Tk()
window.geometry("1280x720")
window.title("IndiNote")

# Text area (main editor)
text = tk.Text(window, undo=True, wrap="word")
text.pack(fill="both", expand=1)

font_name, font_size = "Arial", 12

text.config(font=(font_name, font_size))

status_frame = tk.Frame(window, bd=1, relief="sunken")
status_frame.pack(side="bottom", fill="x")

status_left = tk.Label(status_frame, text="IndiNote | Ln : 0 Col : 0", anchor="w")
status_left.pack(side="left")
status_right = tk.Label(
    status_frame, text="Lines : 0 | Words: 0 | Characters: 0", anchor="e"
)
status_right.pack(side="right")

def load_file(filepath):
    for encoding in ("utf-8", "utf-16", "utf-32"):
        try:
            with open(filepath, "r", encoding=encoding) as f:
                text.insert(tk.END, f.read())
            window.title(f"IndiNote - {filepath}")
            return
        except Exception:
            continue
    messagebox.showerror("Error", "Cannot open file: Unsupported encoding")

# Check if a file was opened with the app
if len(sys.argv) > 1:
    load_file(sys.argv[1])
# -------------------------
# File Handling Functions
# -------------------------
def open_file():
    """Open a text file and display its contents in the editor"""
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        with open(path, "r", encoding="utf-32") as f:
            text.delete(1.0, tk.END)  # clear existing content
            text.insert(tk.END, f.read())  # insert new content
        window.title(f"IndiNote - {path}")  # update window title


def save_file():
    """Save current text to a file"""
    path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text files", "*.txt")]
    )
    if path:
        try:
            with open(path, "w", encoding="utf-32") as f:
                f.write(text.get(1.0, tk.END))  # write all text
            window.title(f"IndiNote - {path}")  # update window title
        except Exception as e:
            messagebox.showerror("Save Error", str(e))  # error popup


# -------------------------
# App Handling Functions
# -------------------------


def toggle_wrap():
    """Word Wrap toggler"""
    if text.cget("wrap") == "none":
        text.config(wrap="word")
        edit_menu.entryconfig("Word Wrap : Off", label="Word Wrap : On")
    else:
        text.config(wrap="none")
        edit_menu.entryconfig("Word Wrap : On", label="Word Wrap : Off")


def word_line_count():
    """Words and Lines number counter"""
    content = text.get(1.0, tk.END)
    words = len(content.split())
    charecters = len(content) - 1
    lines = content.count("\n")
    status_right.config(
        text=f"Lines : {lines} | Words: {words} | Characters: {charecters}"
    )


def ln_col():
    # Get current line and column
    line, col = text.index(tk.INSERT).split(".")
    status_left.config(text=f"IndiNote | Ln : {line} Col : {col}")


def status_update():
    word_line_count()
    ln_col()


def toggle_mode():
    global current_mode

    if current_mode == "light":
        text.config(bg="black", fg="white")
        window.config(bg="black")
        status_frame.config(bg="black")
        status_right.config(bg="black", fg="white")
        status_left.config(bg="black", fg="white")
        menu.config(
            bg="black", fg="white", activebackground="gray", activeforeground="cyan"
        )
        text.config(insertbackground="white")  # cursor color
        text.tag_configure("url", foreground="#4fc1ff", underline=True)
        current_mode = "dark"
        view_menu.entryconfig("Dark Mode", label="Light Mode")

    elif current_mode == "dark":
        text.config(bg="white", fg="black")
        window.config(bg="white")
        status_frame.config(bg="white")
        status_right.config(bg="white", fg="black")
        status_left.config(bg="white", fg="black")
        menu.config(bg="white", fg="black")
        text.config(insertbackground="black")  # cursor color
        text.tag_configure("url", foreground="#1a0dab", underline=True)
        current_mode = "light"
        view_menu.entryconfig("Light Mode", label="Dark Mode")


def zoom_in():
    global font_name, font_size
    font_size = font_size + 5
    text.config(font=(font_name, font_size))


def zoom_out():
    global font_name, font_size
    font_size = font_size - 5
    text.config(font=(font_name, font_size))


def font_name_size():
    global font_size

    def getter():
        global font_name
        font_name = font_var.get()  # Update the global variable with the selected value
        text.config(font=(font_name, font_size))

    font_window = tk.Toplevel(window)
    font_window.geometry("300x50")
    font_window.title("Font and Size")

    # Create an OptionMenu with default fonts
    default_fonts = [
        "Courier",
        "Fixedsys",
        "sans-serif",  # usually Arial or Helvetica
        "Times New Roman",
        "Monaco",
        "Consolas",
        "Courier New",
        "Comic Sans MS",
        "Courier New Script",
        "Great Vibes",
        "Rockwell",
    ]

    # Use StringVar to bind the selected value to a variable
    font_var = tk.StringVar()
    font_var.set(default_fonts[0])  # default value

    menu_down = tk.OptionMenu(font_window, font_var, *default_fonts)
    menu_down.pack()

    ok_button = tk.Button(font_window, text="Ok", command=lambda: getter())
    ok_button.pack()


def find_replace():
    find_window = tk.Toplevel(window)
    find_window.geometry("320x120")
    find_window.title("Find & Replace")
    find_window.resizable(False, False)
    find_window.configure(bg="#f0f0f0")
    find_window.transient(window)  # keeps it above main
    find_window.grab_set()         # modal behavior

    # --- Labels ---
    tk.Label(find_window, text="Find:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(find_window, text="Replace:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # --- Entries ---
    find_text, repl_text = tk.StringVar(), tk.StringVar()
    find_entry = tk.Entry(find_window, textvariable=find_text, width=25)
    replace_entry = tk.Entry(find_window, textvariable=repl_text, width=25)
    find_entry.grid(row=0, column=1, padx=5, pady=5)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    # --- Replace Logic ---
    def replacer():
        find_str = find_entry.get()
        repl_str = replace_entry.get()
        content = text.get("1.0", tk.END).replace(find_str, repl_str)
        text.delete("1.0", tk.END)
        text.insert("1.0", content)

    # --- Buttons ---
    button_frame = tk.Frame(find_window, bg="#f0f0f0")
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(button_frame, text="Replace", command=replacer, width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Close", command=find_window.destroy, width=10).pack(side="right", padx=5)

def print_file():
    pass

def placeholder():
    pass


# -------------------------
# URL Detection + Click
# -------------------------
def highlight_urls(event=None):
    """Highlight URLs in the text whenever user types"""
    content = text.get(1.0, tk.END)
    text.tag_remove("url", "1.0", tk.END)  # clear old highlights
    for match in refinditer(r"https?://\S+", content):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        text.tag_add("url", start, end)  # mark url with tag


def open_url(event):
    """Open clicked URL in the default browser"""
    index = text.index(f"@{event.x},{event.y}")  # cursor pos
    ranges = text.tag_ranges("url")  # get all url spans
    for start, end in zip(ranges[0::2], ranges[1::2]):
        if text.compare(start, "<=", index) and text.compare(index, "<=", end):
            url = text.get(start, end)  # extract url text
            webopen(url)  # launch in browser
            break


# -------------------------
# Key Bindings
# -------------------------
window.bind_all("<KeyRelease>", lambda event: status_update())
window.bind("<Control-o>", lambda event: open_file())
window.bind("<Control-s>", lambda event: save_file())
window.bind("<Control-w>", lambda event: toggle_wrap())
window.bind("<Control-q>", lambda event: window.quit())
window.bind("<Control-=>", lambda event: zoom_in())
window.bind("<Control-minus>", lambda event: zoom_out())
window.bind("<Control-g>", lambda event: font_name_size())
window.bind("<Control-f>", lambda event: find_replace())


# -------------------------
# Menu Bar Setup
# -------------------------
menu = tk.Menu(window)
window.config(menu=menu)

# --- File Menu ---
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# --- Edit Menu ---
edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=lambda: text.edit_undo)
edit_menu.add_command(label="Redo", command=lambda: text.edit_redo)
edit_menu.add_command(label="Find & Replace", command=lambda: find_replace())
edit_menu.add_command(label="Word Wrap : On", command=lambda: toggle_wrap())

# --- View Menu ----
view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom In", command=lambda: zoom_in())
view_menu.add_command(label="Zoon Out", command=lambda: zoom_out())
view_menu.add_command(label="Font & Size", command=lambda: font_name_size())
view_menu.add_command(label="Dark Mode", command=lambda: toggle_mode())

# --- About Menu ---
about_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(
    label="IndiNote",
    command=lambda: messagebox.showinfo(title="about IndiNote", message=indinote),
)
about_menu.add_command(
    label="Indisoft",
    command=lambda: messagebox.showinfo(title="about Indisoft", message=indisoft),
)
about_menu.add_command(
    label="What's New",
    command=lambda: messagebox.showinfo(title="about Indisoft", message=whats_new),
)

# -------------------------
# URL Highlighting Bindings
# -------------------------
text.bind("<KeyRelease>", highlight_urls)  # detect new urls while typing
text.tag_configure("url", foreground="blue", underline=True)  # style
text.tag_bind("url", "<Button-1>", open_url)  # clickable links

# -------------------------
# Start the App
# -------------------------
window.mainloop()
