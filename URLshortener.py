from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('urls.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             original_url TEXT,
             short_url TEXT)''')
conn.commit()


# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Shorten URL
@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']

    # Check if the URL is already shortened
    c.execute("SELECT short_url FROM urls WHERE original_url=?", (original_url,))
    result = c.fetchone()

    if result:
        # URL already shortened, return the existing short URL
        short_url = result[0]
    else:
        # Generate a new short URL
        short_url = generate_short_url()

        # Insert the URL into the database
        c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()

    return render_template('result.html', short_url=short_url)


# Redirect to original URL
@app.route('/<short_url>')
def redirect_to_url(short_url):
    # Retrieve the original URL from the database
    c.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = c.fetchone()

    if result:
        original_url = result[0]
        return redirect(original_url)
    else:
        return "URL not found."


if __name__ == '__main__':
    app.run(debug=True)
