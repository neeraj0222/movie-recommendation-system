import streamlit as st
import pandas as pd
import pickle
import requests
import time


st.set_page_config(
    page_title="Movie Recommendation",layout="wide")

session = requests.Session()
session.headers.update({"User_Agent":"Movie_App/1.0"})

def fetch_poster(movie_id):
    url=f"https://api.themoviedb.org/3/movie/{movie_id}"
    params={
        "api_key":"cc8956f9e0c895ba017154cc97008381",
        "language":"en-US",
    }

    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data=response.json()

            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + data['poster_path']
            else:
                return "https://image.tmdb.org/t/p/w500"

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
                continue
            else:
                return "https://via.placeholder.com/300x450?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances= similarity[movie_index]
    movie_list = sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x: x[1])[1:6]


    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title
st.markdown("<h1>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)


# Selectbox FIRST
selected_movie_name = st.selectbox("Enter the name of a movie",movies['title'].values)

# Button BELOW selectbox
if st.button("Recommend"):
    with st.spinner("Finding best movies for you 🎥"):
        name, posters = recommend(selected_movie_name)


    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])



