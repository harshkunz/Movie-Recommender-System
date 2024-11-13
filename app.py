import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Recommendation function
def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()

# Fetch poster function
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8' 
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

# Streamlit UI
st.title("Find Your Next Favorite Film")

# Display 3 top movies at the top
top_movies = movies.head(3)  # Adjust the top movies to display (you can change this logic)

st.subheader("Top 3 Movies")
cols_top = st.columns(3)  # Create 3 columns for the top movies

# Display the top 3 movies with their posters
for i in range(3):
    movie_title = top_movies.iloc[i]['title']
    movie_id = top_movies.iloc[i]['movie_id']
    poster_url = fetch_poster(movie_id)
    with cols_top[i]:
        if poster_url:
            st.image(poster_url, width=150)
        st.write(movie_title)

# Movie selection
selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    # Create a 2x5 grid layout
    cols = st.columns(5)  # Create 5 columns for the first row

    # Display the first row of 5 recommendations
    for i in range(5):
        if i < len(recommendations):
            movie_title = recommendations[i]
            movie_id = movies[movies['title'] == movie_title].iloc[0]['movie_id']
            poster_url = fetch_poster(movie_id)
            with cols[i]:
                if poster_url:
                    st.image(poster_url, width=130)
                st.write(movie_title)

    # Create the second row of 5 recommendations
    cols2 = st.columns(5)  # Create 5 columns for the second row

    # Display the second row of 5 recommendations
    for i in range(5, 10):
        if i < len(recommendations):
            movie_title = recommendations[i]
            movie_id = movies[movies['title'] == movie_title].iloc[0]['movie_id']
            poster_url = fetch_poster(movie_id)
            with cols2[i - 5]:
                if poster_url:
                    st.image(poster_url, width=130)
                st.write(movie_title)
