from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Replace with a secure, random key

OMDB_API_KEY = "YOUR_API_KEY_HERE"
movies = []

@app.route('/')
def home():
    return render_template('index.html', movies=movies, show_form=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'Abare3861':  # Replace with your actual admin password
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return '<h3>Wrong password</h3>'
    return '''
        <form method="post" style="text-align:center; margin-top: 5rem;">
            <h2>Admin Login</h2>
            <input type="password" name="password" placeholder="Enter admin password" required>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', movies=movies, show_form=True)

@app.route('/add', methods=['POST'])
def add_movie():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    title = request.form.get('title')
    if not title:
        return redirect(url_for('admin'))

    response = requests.get("http://www.omdbapi.com/", params={
        "t": title,
        "apikey": OMDB_API_KEY
    })
    data = response.json()

    if data.get("Response") == "True":
        movie = {
            "title": data.get("Title"),
            "poster": data.get("Poster"),
            "plot": data.get("Plot"),
            "genre": data.get("Genre")
        }
        movies.append(movie)

    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
