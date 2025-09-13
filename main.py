import tkinter as tk
from tkinter import filedialog, messagebox
from re import finditer as refinditer
from webbrowser import open as webopen


# -------------------------
# Defaults
# -------------------------

indisoft = "\t\t      r/indisoft\n\nFor India, By India. A safe space for devs, designers,\
and dreamers to collaborate on one goal: building feature-rich Indian apps\
that are truly ours. Share ideas, find teammates, showcase projects, and \
create alternatives or originals that India actually needs.\
Collaborate. Innovate. Make in India."

indinote = "\t\t     Version 0.2\n\nIndiNote by IndiSoft: a fast, distraction-free notepad for Indians by Indians."

current_mode = "light"
# -------------------------
# Main Window Setup
# -------------------------
window = tk.Tk()
window.title("IndiNote")

# Text area (main editor)
text = tk.Text(window, undo=True, wrap="word")
text.pack(fill="both", expand=1)

status_frame = tk.Frame(window, bd=1, relief="sunken")
status_frame.pack(side="bottom", fill="x")

status_left = tk.Label(status_frame, text="IndiNote | Ln : 0 Col : 0", anchor="w")
status_left.pack(side="left")
status_right = tk.Label(
    status_frame, text="Lines : 0 | Words: 0 | Characters: 0", anchor="e"
)
status_right.pack(side="right")


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
    
    if current_mode == 'light':
        text.config(bg="black", fg="white")
        window.config(bg="black")
        status_frame.config(bg="black")
        status_right.config(bg="black", fg="white")
        status_left.config(bg="black", fg="white")
        menu.config(bg="black", fg="white", activebackground="gray", activeforeground="cyan")
        text.config(insertbackground="white")  # cursor color
        text.tag_configure("url", foreground="#4fc1ff", underline=True)
        current_mode = 'dark'
        edit_menu.entryconfig("Dark Mode", label="Light Mode")
    
    elif current_mode == 'dark':
        text.config(bg="white", fg="black")
        window.config(bg="white")
        status_frame.config(bg="white")
        status_right.config(bg="white", fg="black")
        status_left.config(bg="white", fg="black")
        menu.config(bg="white", fg="black")
        text.config(insertbackground="blck")  # cursor color
        text.tag_configure("url", foreground="#1a0dab", underline=True)
        current_mode = 'light'
        edit_menu.entryconfig("Light Mode", label="Dark Mode")


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
edit_menu.add_command(label="Undo", command=text.edit_undo)
edit_menu.add_command(label="Redo", command=text.edit_redo)
edit_menu.add_command(label="Word Wrap : On", command=lambda: toggle_wrap())

# --- View Menu ----
view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom In", command=placeholder())
view_menu.add_command(label="Zoon Out", command=placeholder())
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
