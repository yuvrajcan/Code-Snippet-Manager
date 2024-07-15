import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Create the database and table
def init_db():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        code TEXT NOT NULL,
        language TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Function to add a new snippet to the database
def add_snippet(title, description, code, language):
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO snippets (title, description, code, language)
    VALUES (?, ?, ?, ?)
    ''', (title, description, code, language))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Snippet added successfully")

# Function to view all snippets
def view_snippets():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute('SELECT * FROM snippets')
    rows = c.fetchall()
    conn.close()
    return rows

# Main application window
class SnippetManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Code Snippet Manager")
        self.geometry("600x400")

        # Title
        self.lbl_title = ttk.Label(self, text="Title")
        self.lbl_title.grid(row=0, column=0, padx=10, pady=10)
        self.ent_title = ttk.Entry(self)
        self.ent_title.grid(row=0, column=1, padx=10, pady=10)

        # Description
        self.lbl_description = ttk.Label(self, text="Description")
        self.lbl_description.grid(row=1, column=0, padx=10, pady=10)
        self.ent_description = ttk.Entry(self)
        self.ent_description.grid(row=1, column=1, padx=10, pady=10)

        # Code
        self.lbl_code = ttk.Label(self, text="Code")
        self.lbl_code.grid(row=2, column=0, padx=10, pady=10)
        self.txt_code = tk.Text(self, height=10, width=50)
        self.txt_code.grid(row=2, column=1, padx=10, pady=10)

        # Language
        self.lbl_language = ttk.Label(self, text="Language")
        self.lbl_language.grid(row=3, column=0, padx=10, pady=10)
        self.ent_language = ttk.Entry(self)
        self.ent_language.grid(row=3, column=1, padx=10, pady=10)

        # Add Button
        self.btn_add = ttk.Button(self, text="Add Snippet", command=self.add_snippet)
        self.btn_add.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # View Button
        self.btn_view = ttk.Button(self, text="View Snippets", command=self.view_snippets)
        self.btn_view.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_snippet(self):
        title = self.ent_title.get()
        description = self.ent_description.get()
        code = self.txt_code.get("1.0", tk.END)
        language = self.ent_language.get()
        if title and description and code and language:
            add_snippet(title, description, code, language)
        else:
            messagebox.showwarning("Input Error", "Title, Code, Description and Language are required")

    def view_snippets(self):
        snippets = view_snippets()
        view_window = tk.Toplevel(self)
        view_window.title("View Snippets")

        # Create a Text widget with a scrollbar for viewing snippets
        text_widget = tk.Text(view_window, wrap="none", width=80, height=20)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_y = tk.Scrollbar(view_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(view_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        text_widget.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        for snippet in snippets:
            snippet_text = f"Title: {snippet[1]}\nDescription: {snippet[2]}\nCode:\n{snippet[3]}\nLanguage: {snippet[4]}\n{'-'*60}\n"
            text_widget.insert(tk.END, snippet_text)

if __name__ == "__main__":
    init_db()
    app = SnippetManager()
    app.mainloop()
