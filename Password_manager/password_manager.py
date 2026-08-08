import customtkinter as ctk
import sqlite3
import random
import string
import pyperclip
import os

from tkinter import messagebox
from cryptography.fernet import Fernet

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- ENCRYPTION ---------------- #

if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as f:
        f.write(Fernet.generate_key())

with open("secret.key", "rb") as f:
    key = f.read()

cipher = Fernet(key)

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("passwords.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS passwords(
id INTEGER PRIMARY KEY AUTOINCREMENT,
website TEXT UNIQUE,
username TEXT,
password BLOB
)
""")

conn.commit()

# ---------------- FUNCTIONS ---------------- #

def check_strength():

    pwd = password_entry.get()

    score = 0

    if len(pwd) >= 8:
        score += 1

    if any(c.isupper() for c in pwd):
        score += 1

    if any(c.islower() for c in pwd):
        score += 1

    if any(c.isdigit() for c in pwd):
        score += 1

    if any(c in "!@#$%^&*" for c in pwd):
        score += 1

    if score <= 2:
        strength_label.configure(
            text="🔴 Weak",
            text_color="red"
        )

    elif score <= 4:
        strength_label.configure(
            text="🟡 Medium",
            text_color="orange"
        )

    else:
        strength_label.configure(
            text="🟢 Strong",
            text_color="green"
        )


def generate_password():

    chars = string.ascii_letters + string.digits + "!@#$%^&*"

    pwd = "".join(random.choice(chars) for _ in range(16))

    password_entry.delete(0, "end")
    password_entry.insert(0, pwd)

    check_strength()


def save_password():

    website = website_entry.get()

    username = username_entry.get()

    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    encrypted = cipher.encrypt(password.encode())

    try:

        cur.execute(
            "INSERT INTO passwords(website,username,password) VALUES(?,?,?)",
            (website, username, encrypted)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Password Saved!"
        )

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Website already exists."
        )


# ---------------- WINDOW ---------------- #

app = ctk.CTk()

app.geometry("600x650")

app.title("Secure Password Manager")

title = ctk.CTkLabel(
    app,
    text="🔐 Secure Password Manager",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=20)

website_entry = ctk.CTkEntry(
    app,
    width=450,
    height=45,
    placeholder_text="Website"
)

website_entry.pack(pady=10)

username_entry = ctk.CTkEntry(
    app,
    width=450,
    height=45,
    placeholder_text="Username / Email"
)

username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    app,
    width=450,
    height=45,
    placeholder_text="Password",
    show="*"
)

password_entry.pack(pady=10)

strength_label = ctk.CTkLabel(
    app,
    text="Strength : -"
)

strength_label.pack(pady=5)

generate_btn = ctk.CTkButton(
    app,
    text="🎲 Generate Password",
    width=450,
    command=generate_password
)

generate_btn.pack(pady=10)

save_btn = ctk.CTkButton(
    app,
    text="💾 Save Password",
    width=450,
    fg_color="green",
    command=save_password
)

save_btn.pack(pady=10)
# ---------------- SEARCH ---------------- #

def search_password():

    site = website_entry.get()

    if site == "":
        messagebox.showerror("Error", "Enter Website Name")
        return

    cur.execute(
        "SELECT username,password FROM passwords WHERE website=?",
        (site,)
    )

    data = cur.fetchone()

    if data:

        username_entry.delete(0, "end")
        password_entry.delete(0, "end")

        username_entry.insert(0, data[0])

        decrypted = cipher.decrypt(data[1]).decode()

        password_entry.insert(0, decrypted)

        check_strength()

    else:

        messagebox.showerror(
            "Not Found",
            "Website not found."
        )


# ---------------- UPDATE ---------------- #

def update_password():

    site = website_entry.get()
    user = username_entry.get()
    pwd = password_entry.get()

    if site == "" or user == "" or pwd == "":
        messagebox.showerror(
            "Error",
            "Fill all fields."
        )
        return

    encrypted = cipher.encrypt(pwd.encode())

    cur.execute(
        "UPDATE passwords SET username=?,password=? WHERE website=?",
        (user, encrypted, site)
    )

    conn.commit()

    if cur.rowcount == 0:

        messagebox.showerror(
            "Error",
            "Website not found."
        )

    else:

        messagebox.showinfo(
            "Updated",
            "Password Updated Successfully!"
        )


# ---------------- DELETE ---------------- #

def delete_password():

    site = website_entry.get()

    if site == "":
        messagebox.showerror(
            "Error",
            "Enter Website Name"
        )
        return

    cur.execute(
        "DELETE FROM passwords WHERE website=?",
        (site,)
    )

    conn.commit()

    if cur.rowcount == 0:

        messagebox.showerror(
            "Error",
            "Website not found."
        )

    else:

        messagebox.showinfo(
            "Deleted",
            "Password Deleted Successfully!"
        )

        website_entry.delete(0, "end")
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")

        strength_label.configure(
            text="Strength : -",
            text_color="white"
        )


# ---------------- COPY ---------------- #

def copy_password():

    pyperclip.copy(password_entry.get())

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# ---------------- SHOW / HIDE ---------------- #

show = False

def toggle_password():

    global show

    if show:

        password_entry.configure(show="*")
        eye_btn.configure(text="👁 Show")
        show = False

    else:

        password_entry.configure(show="")
        eye_btn.configure(text="🙈 Hide")
        show = True


# ---------------- BUTTONS ---------------- #

search_btn = ctk.CTkButton(
    app,
    text="🔍 Search Password",
    width=450,
    command=search_password
)

search_btn.pack(pady=8)

update_btn = ctk.CTkButton(
    app,
    text="✏️ Update Password",
    width=450,
    fg_color="#1f6aa5",
    command=update_password
)

update_btn.pack(pady=8)

delete_btn = ctk.CTkButton(
    app,
    text="🗑 Delete Password",
    width=450,
    fg_color="red",
    hover_color="#b00020",
    command=delete_password
)

delete_btn.pack(pady=8)

copy_btn = ctk.CTkButton(
    app,
    text="📋 Copy Password",
    width=450,
    command=copy_password
)

copy_btn.pack(pady=8)

eye_btn = ctk.CTkButton(
    app,
    text="👁 Show",
    width=450,
    command=toggle_password
)

eye_btn.pack(pady=8)

footer = ctk.CTkLabel(
    app,
    text="Developed by Krishna Mishra",
    text_color="gray"
)

footer.pack(side="bottom", pady=15)


# ---------------- CLOSE ---------------- #

app.mainloop()

conn.close()