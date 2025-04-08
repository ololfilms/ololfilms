from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Replace this with your actual OMDb API key
OMDB_API_KEY = "YOUR_API_KEY_HERE"

movies = []

@app.route('/')
def home():
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    if not title:
        return redirect(url_for('home'))

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

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
