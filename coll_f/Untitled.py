{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "2911d26e-563a-43e7-889e-92c512d83fd5",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-05-17 12:40:11.609 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\91790\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    },
    {
     "ename": "AttributeError",
     "evalue": "module 'streamlit' has no attribute '_main_run_clExplicit'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 79\u001b[0m\n\u001b[0;32m     77\u001b[0m \u001b[38;5;66;03m# Run the Streamlit app\u001b[39;00m\n\u001b[0;32m     78\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;18m__name__\u001b[39m \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124m__main__\u001b[39m\u001b[38;5;124m'\u001b[39m:\n\u001b[1;32m---> 79\u001b[0m     \u001b[43mst\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_main_run_clExplicit\u001b[49m(\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mstreamlit run app.py\u001b[39m\u001b[38;5;124m'\u001b[39m, {})\n",
      "\u001b[1;31mAttributeError\u001b[0m: module 'streamlit' has no attribute '_main_run_clExplicit'"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "\n",
    "# Your functions for collaborative filtering and content-based recommendations\n",
    "\n",
    "def get_top_similar_items(item_similarity_df, item_id, top_n=5):\n",
    "    similar_items_row = item_similarity_df.loc[item_id]\n",
    "    top_similar_items = similar_items_row.sort_values(ascending=False).head(top_n)\n",
    "    return top_similar_items\n",
    "\n",
    "def generate_recommendations(user_id, user_item_matrix, item_similarity_df, top_n=5):\n",
    "    user_items = user_item_matrix.loc[user_id]\n",
    "\n",
    "    item_scores = {}\n",
    "    for item_id, interaction in user_items.items():\n",
    "        similar_items = get_top_similar_items(item_similarity_df, item_id, top_n)\n",
    "        for similar_item_id, similarity_score in similar_items.items():\n",
    "            if similar_item_id not in item_scores:\n",
    "                item_scores[similar_item_id] = 0\n",
    "            item_scores[similar_item_id] += similarity_score * interaction\n",
    "\n",
    "    sorted_item_scores = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)\n",
    "    recommendations = [item_id for item_id, score in sorted_item_scores[:top_n]]\n",
    "    return recommendations\n",
    "\n",
    "def recommend_movies_by_genre(user_id, final_table, top_n=5):\n",
    "    user_data = final_table[final_table['userId'] == user_id]\n",
    "\n",
    "    genre_counts = {}\n",
    "    for genres in user_data['genres']:\n",
    "        for genre in genres.split('|'):\n",
    "            genre_counts[genre] = genre_counts.get(genre, 0) + 1\n",
    "\n",
    "    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)\n",
    "    top_genres = [genre for genre, _ in sorted_genres[:top_n]]\n",
    "\n",
    "    recommended_movies = final_table[\n",
    "        (~final_table['title'].isin(user_data['title'])) &\n",
    "        (final_table['genres'].apply(lambda x: any(genre in x.split('|') for genre in top_genres)))\n",
    "    ].drop_duplicates(subset=['title'])\n",
    "\n",
    "    return recommended_movies.head(top_n)\n",
    "\n",
    "# Example data\n",
    "item_similarity_df = pd.read_csv('item_similarity_df_file.csv', index_col=0)\n",
    "\n",
    "# Load user_item_matrix from CSV\n",
    "user_item_matrix = pd.read_csv('user_item_matrix_file.csv', index_col=0)\n",
    "data_filled = user_item_matrix.fillna(0)\n",
    "\n",
    "# Handle null values by replacing them with zeros\n",
    "data_filled = data.fillna(0)\n",
    "\n",
    "# Load final_table from CSV\n",
    "final_table = pd.read_csv('ratings_summary.csv')\n",
    "\n",
    "# Streamlit Interface\n",
    "st.title('Movie Recommendation System')\n",
    "\n",
    "st.sidebar.header('User Selection')\n",
    "user_id = st.sidebar.number_input('Enter User ID:', min_value=1, step=1)\n",
    "\n",
    "recommendation_type = st.sidebar.selectbox(\n",
    "    'Select Recommendation Type:',\n",
    "    ('Collaborative Filtering', 'Content-Based')\n",
    ")\n",
    "\n",
    "if recommendation_type == 'Collaborative Filtering':\n",
    "    top_n = st.sidebar.slider('Number of Recommendations:', min_value=1, max_value=10, value=5)\n",
    "    if st.sidebar.button('Generate Recommendations'):\n",
    "        recommendations = generate_recommendations(user_id, user_item_matrix, item_similarity_df, top_n)\n",
    "        st.write(f\"Collaborative Filtering Recommendations for User {user_id}:\")\n",
    "        st.write(recommendations)\n",
    "else:\n",
    "    top_n = st.sidebar.slider('Number of Recommendations:', min_value=1, max_value=10, value=5)\n",
    "    if st.sidebar.button('Generate Recommendations'):\n",
    "        recommended_movies = recommend_movies_by_genre(user_id, final_table, top_n)\n",
    "        st.write(f\"Content-Based Recommendations for User {user_id}:\")\n",
    "        st.write(recommended_movies[['title', 'genres']])\n",
    "\n",
    "# Run the Streamlit app\n",
    "if __name__ == '__main__':\n",
    "    st._main_run_clExplicit('streamlit run app.py', {})\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fd06cde3-3366-4b8d-a369-877379fb1950",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
