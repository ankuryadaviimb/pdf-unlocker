import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD


class PDFUnlocker(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()

        self.title("PDF Unlocker")
        self.geometry("450x300")

        self.pdf_path = None

        # Title
        title = tk.Label(
            self,
            text="PDF Unlocker",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # Drop Area
        self.drop_area = tk.Label(
            self,
            text="Drag PDF Here\nor Use Browse Button",
            width=45,
            height=4,
            bg="#f0f0f0",
            relief="ridge"
        )
        self.drop_area.pack(pady=10)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        # Browse Button
        browse_btn = tk.Button(
            self,
            text="Browse PDF",
            command=self.browse_file
        )
        browse_btn.pack(pady=5)

        # Password
        pass_label = tk.Label(self, text="Enter Password:")
        pass_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.pack()

        # Unlock Button
        self.unlock_btn = tk.Button(
            self,
            text="Unlock PDF",
            command=self.unlock_pdf
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

        self.drop_area.config(
            text=f"Loaded:\n{filename}",
            bg="#dff0d8"
        )


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

        self.drop_area.config(
            text="Drag PDF Here\nor Use Browse Button",
            bg="#f0f0f0"
        )

        self.password_entry.delete(0, tk.END)



if __name__ == "__main__":

    app = PDFUnlocker()
    app.mainloop()
