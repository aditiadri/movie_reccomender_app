from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the datasets
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')

# Merge movies and ratings dataframes
merged_df = pd.merge(ratings_df, movies_df, on='movieId')

# Function to get user movie history
def get_user_movie_history():
    user_movie_history = []
    while True:
        movie_title = request.form.get('movie_title')
        if movie_title.lower() == 'done':
            break
        elif movie_title not in merged_df['title'].unique():
            return render_template('error.html', message="Movie not found. Please enter a valid movie title.")
        else:
            user_movie_history.append(movie_title)
    return user_movie_history

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_movie_history = get_user_movie_history()
        if isinstance(user_movie_history, list):
            # Filter out movies already watched by the user
            unwatched_movies = movies_df[~movies_df['title'].isin(user_movie_history)]

            # Merge with ratings data to get average ratings
            unwatched_ratings = pd.merge(unwatched_movies, movie_ratings, on='title')

            # Sort unrated movies by mean rating in descending order
            top_recommendations = unwatched_ratings.sort_values(by='rating', ascending=False).head(10)

            return render_template('recommendations.html', recommendations=top_recommendations)
        else:
            return user_movie_history
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
