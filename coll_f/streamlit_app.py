import pandas as pd
import streamlit as st

# Load your data (assuming you have already loaded and processed your data)
# Example dataframes: user_item_matrix, item_similarity_df, final_table

# Function to get top similar items based on item-item similarity
def get_top_similar_items(item_similarity_df, item_id, top_n=5):
    similar_items_row = item_similarity_df.loc[item_id]
    top_similar_items = similar_items_row.sort_values(ascending=False).head(top_n)
    return top_similar_items

# Function to recommend movies based on genre preferences
def recommend_movies_by_genre(user_id, final_table, top_n=5):
    user_data = final_table[final_table['userId'] == user_id]

    genre_counts = {}
    for genres in user_data['genres']:
        for genre in genres.split('|'):
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
    top_genres = [genre for genre, _ in sorted_genres[:top_n]]

    recommended_movies = final_table[~final_table['title'].isin(user_data['title']) & 
                                     final_table['genres'].apply(lambda x: any(genre in x.split('|') for genre in top_genres))]
    recommended_movies = recommended_movies[~recommended_movies['title'].isin(user_data['title'])]
    recommended_movies = recommended_movies.drop_duplicates(subset=['title'])

    return recommended_movies

# Load your dataframes (user_item_matrix, item_similarity_df, final_table)
# Replace these placeholders with your actual data loading process
user_item_matrix = pd.DataFrame()
item_similarity_df = pd.DataFrame()
final_table = pd.DataFrame()

# Streamlit app code
st.title("Movie Recommendation System")

# Sidebar for user input
if not user_item_matrix.empty:
    user_id = st.sidebar.number_input("Enter User ID", min_value=1, max_value=user_item_matrix['userId'].max(), value=1)

    # Generate recommendations based on collaborative filtering
    recommendations_cf = generate_recommendations(user_id, user_item_matrix, item_similarity_df)
    st.write("Collaborative Filtering Recommendations:")
    st.write(recommendations_cf)

    # Generate recommendations based on genre preferences
    recommended_movies_genre = recommend_movies_by_genre(user_id, final_table)
    st.write("Genre-based Recommendations:")
    st.write(recommended_movies_genre[['title', 'genres']].head())
else:
    st.write("No data available. Please load your data first.")


