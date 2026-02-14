import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD


class PDFUnlocker(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()

        self.title("PDF Unlocker")
        self.geometry("450x340")

        self.pdf_path = None

        # Title
        title = tk.Label(
            self,
            text="PDF Unlocker",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # ---------------------------
        # Combined Drop Zone + Browse Tile
        # ---------------------------
        self.drop_tile = tk.Frame(
            self,
            bg="#f0f0f0",
            relief="ridge",
            borderwidth=2,
        )
        self.drop_tile.pack(padx=20, pady=10, fill="x")

        self.drop_label = tk.Label(
            self.drop_tile,
            text="Drag and Drop PDF Here",
            font=("Arial", 11),
            bg="#f0f0f0",
            height=3,
        )
        self.drop_label.pack(fill="x", padx=10, pady=(10, 0))

        or_label = tk.Label(
            self.drop_tile,
            text="or",
            font=("Arial", 9),
            fg="#888888",
            bg="#f0f0f0",
        )
        or_label.pack()

        browse_btn = tk.Button(
            self.drop_tile,
            text="Browse PDF",
            command=self.browse_file,
        )
        browse_btn.pack(pady=(0, 10))

        # Register drag-and-drop on the entire tile and its children
        self.drop_tile.drop_target_register(DND_FILES)
        self.drop_tile.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_drop)

        # ---------------------------
        # Password
        # ---------------------------
        pass_label = tk.Label(self, text="Enter Password:")
        pass_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack()

        # ---------------------------
        # Unlock Button
        # ---------------------------
        self.unlock_btn = tk.Button(
            self,
            text="Unlock PDF",
            command=self.unlock_pdf,
        )
        self.unlock_btn.pack(pady=15)

        # Bind Enter Key
        self.bind("<Return>", self.on_enter_key)

    # ---------------------------
    # File Selection
    # ---------------------------

    def browse_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )

        if file_path:
            self.load_file(file_path)

    def on_drop(self, event):

        file_path = event.data.strip("{}")

        if not file_path.lower().endswith(".pdf"):
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        self.load_file(file_path)

    def load_file(self, file_path):

        self.pdf_path = file_path

        filename = os.path.basename(file_path)

        self.drop_label.config(
            text=f"Loaded:\n{filename}",
            bg="#dff0d8"
        )
        self.drop_tile.config(bg="#dff0d8")

        self.password_entry.focus_set()

    # ---------------------------
    # Unlock Logic
    # ---------------------------

    def unlock_pdf(self):

        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF first.")
            return

        password = self.password_entry.get()

        if not password:
            messagebox.showerror("Error", "Enter password.")
            return

        try:
            reader = PyPDF2.PdfReader(self.pdf_path)

            if reader.is_encrypted:
                reader.decrypt(password)

            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            base = os.path.splitext(self.pdf_path)[0]
            output = base + "_unlocked.pdf"

            with open(output, "wb") as f:
                writer.write(f)

            messagebox.showinfo(
                "Success",
                f"Unlocked file saved:\n{output}"
            )

            self.reset_ui()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------
    # UX Helpers
    # ---------------------------

    def on_enter_key(self, event):

        self.unlock_pdf()

    def reset_ui(self):

        self.pdf_path = None

        self.drop_label.config(
            text="Drag and Drop PDF Here",
            bg="#f0f0f0"
        )
        self.drop_tile.config(bg="#f0f0f0")

        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":

    app = PDFUnlocker()
    app.mainloop()
