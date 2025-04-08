from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Replace with your actual OMDb API key
OMDB_API_KEY = "YOUR_API_KEY_HERE"

# In-memory storage for added movies
movies = []

@app.route('/')
def home():
    return render_template('index.html', movies=movies, show_form=False)

@app.route('/admin')
def admin():
    return render_template('index.html', movies=movies, show_form=True)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    if not title:
        return redirect(url_for('admin'))

    # Call OMDb API
    response = requests.get("http://www.omdbapi.com/", params={
        "t": title,
        "apikey": OMDB_API_KEY
    })
    data = response.json()

    if data.get("Response") == "True":
        movie = {
            "title": data.get("Title"),
            "poster": data.get("Poster"),
            "plot": data.get("Plot")
        }
        movies.append(movie)

    return redirect(url_for('admin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
