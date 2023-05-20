import requests
import streamlit as st
from pickle import load

st.set_page_config(
    page_title="Movie Recommender",
    layout='wide',
    page_icon='assets/img/page-icon.png',
    menu_items={
        'About':'Hi, I am Kamesh Kotwani, Data and ML Engineer. You can visit my [GitHub](https://www.github.com/kameshkotwani) page for more awesome projects, and to collaborate as well!'
        
    }
    
)

API_KEY = st.secrets['API_KEY']
IMAGE_FULL_PATH = "https://image.tmdb.org/t/p/w500"

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
    data = response.json()
    return IMAGE_FULL_PATH+data['poster_path']

try:
    # getting the models
    with open("./models/movie_list.pkl",'rb') as f:
        movies_df = load(f)
    with open("./models/similarity.pkl",'rb') as f:
        similarity = load(f)
    movies_titles:list=list(movies_df['title'].values)
except Exception as e:
    st.error("something went wrong from our end, please reload")
    st.stop()

# getting the movie titles
movies_titles.insert(0,None)

def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:6]
    recommended_movies = list() 
    posters = list()
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title) 
        posters.append(fetch_poster(movie_id)) 
    return recommended_movies,posters

st.title('Movie Recommender System')
st.subheader("Recommends top 5 movies of similar content across 5000 movies")

option = st.selectbox('Movies',options=(movies_titles))

try:
    with st.spinner("## Fetching awesome movies!!"):
        if option is not None:
                names,posters = recommend(option)
                col1, col2, col3,col4,col5 = st.columns(5)
                
                with col1:
                    st.text(names[0])
                    st.image(posters[0])
                with col2:
                    st.text(names[1])
                    st.image(posters[1])

                with col3:
                    st.text(names[2])
                    st.image(posters[2])

                with col4:
                    st.text(names[3])
                    st.image(posters[3])
                with col5:
                    st.text(names[4])
                    st.image(posters[4])
        else:
            st.title("Go ahead, try to search some movie!")
            st.write("### Visit my [GitHub](https://www.github.com/kameshkotwani) page for more awesome projects!")
except Exception as e:
    st.info("Perhaps, my database is too small to recommend movies similar to your choice, maybe try some other movie :) ")