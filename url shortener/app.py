from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:5000/"


# Create Database
def create_table():
    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        short TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


create_table()


# Generate Short Code
def generate_short():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM urls WHERE short=?", (code,))
        data = cur.fetchone()

        conn.close()

        if not data:
            return code




@app.route("/", methods=["GET", "POST"])
def home():

    short_url = None

    if request.method == "POST":
        original = request.form["url"]

        code = generate_short()

        conn = sqlite3.connect("urls.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO urls(original, short) VALUES (?, ?)",
            (original, code)
        )

        conn.commit()
        conn.close()

        short_url = BASE_URL + code

    return render_template("index.html", short_url=short_url)
@app.route("/<code>")
def redirect_url(code):

    conn = sqlite3.connect("urls.db")
    cur = conn.cursor()

    cur.execute("SELECT original FROM urls WHERE short=?", (code,))
    data = cur.fetchone()

    conn.close()

    if data:
        return redirect(data[0])

    return "<h2>Invalid URL</h2>"


if __name__ == "__main__":
    app.run(debug=True)