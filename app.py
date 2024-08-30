from flask import Flask, render_template, request
import pickle
import requests
import pandas as pd

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    movie_list = movies['title'].values
    recommended = []
    selected_movie = None
    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        recommended = zip(recommended_movie_names, recommended_movie_posters)
    return render_template('index.html', movie_list=movie_list, recommended=recommended, selected_movie=selected_movie)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
