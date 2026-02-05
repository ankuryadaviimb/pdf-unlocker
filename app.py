import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def unlock_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        return

    password = password_entry.get()

    if not password:
        messagebox.showerror("Error", "Enter password")
        return

    try:
        reader = PyPDF2.PdfReader(file_path)

        if reader.is_encrypted:
            reader.decrypt(password)

        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_file = os.path.splitext(file_path)[0] + "_unlocked.pdf"

        with open(output_file, "wb") as f:
            writer.write(f)

        messagebox.showinfo(
            "Success",
            f"Unlocked PDF saved as:\n{output_file}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# UI
root = tk.Tk()
root.title("PDF Unlocker")

root.geometry("400x200")

label = tk.Label(root, text="Enter PDF Password:")
label.pack(pady=10)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

unlock_btn = tk.Button(
    root,
    text="Select PDF & Unlock",
    command=unlock_pdf
)
unlock_btn.pack(pady=20)

root.mainloop()