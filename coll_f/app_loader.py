import pandas as pd

def load_data():
    movies_df = pd.read_csv('movies.csv')
    ratings_df = pd.read_csv('ratings.csv')
    tags_df = pd.read_csv('tags.csv')
    links_df = pd.read_csv('links.csv')
    return movies_df, ratings_df, tags_df, links_df
