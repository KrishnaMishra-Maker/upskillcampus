import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".apk", ".py", ".java", ".cpp", ".c"]
}


def organize_files(folder_path):

    if not folder_path:
        return

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for folder_name, extensions in FILE_TYPES.items():

            if extension in extensions:

                destination = os.path.join(folder_path, folder_name)

                os.makedirs(destination, exist_ok=True)

                shutil.move(file_path,
                            os.path.join(destination, file))

                moved = True
                break

        if not moved:

            destination = os.path.join(folder_path, "Others")

            os.makedirs(destination, exist_ok=True)

            shutil.move(file_path,
                        os.path.join(destination, file))

    messagebox.showinfo("Success", "Files Organized Successfully!")


def browse_folder():

    folder = filedialog.askdirectory()

    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)


def start():

    organize_files(folder_entry.get())


root = tk.Tk()
root.title("File Organizer")
root.geometry("500x220")
root.resizable(False, False)

title = tk.Label(root,
                 text="Python File Organizer",
                 font=("Arial", 18, "bold"))

title.pack(pady=15)

folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)

browse_btn = tk.Button(root,
                       text="Browse Folder",
                       command=browse_folder)

browse_btn.pack(pady=5)

organize_btn = tk.Button(root,
                         text="Organize Files",
                         bg="green",
                         fg="white",
                         font=("Arial", 12),
                         command=start)

organize_btn.pack(pady=20)

root.mainloop()