import streamlit as st
import pickle
import requests

API_KEY = '27e670863b89edeb19b2ab90a15de05a'

def set_background():
    st.markdown(
        """
        <style>
        /* App Background */
        .stApp {
            background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
            color: #e0e0e0;
            font-family: 'Arial', sans-serif;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00c853, #009688);
            color: white;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #009688, #00796b);
            transform: scale(1.05);
        }

        /* Selectbox */
        .stSelectbox>div>div>select {
            background-color: #222;
            color: #e0e0e0;
            border-radius: 8px;
            padding: 8px;
            border: 1px solid #444;
            transition: all 0.3s ease-in-out;
        }
        .stSelectbox>div>div>select:hover {
            background-color: #333;
        }

        /* Images */
        .stImage>img {
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 255, 128, 0.4);
            transition: all 0.3s ease-in-out;
        }
        .stImage>img:hover {
            transform: scale(1.03);
        }

        /* Titles and Headers */
        h1, h2, h3, h4 {
            text-shadow: 2px 2px 8px rgba(0, 255, 128, 0.4);
            color: #00e676;
        }

        /* Inputs */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #181818;
            color: #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #555;
            transition: all 0.3s ease-in-out;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            border-color: #00c853;
            outline: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background
set_background()

def get_movie_poster(movie_title):
    # Step 1: Search for the movie by title
    search_url = f'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': API_KEY,
        'query': movie_title
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    # Check if any results were found
    if data['results']:
        # Get the first movie's ID
        movie_id = data['results'][0]['id']

        # Step 2: Get movie details (including poster path)
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        movie_params = {
            'api_key': API_KEY
        }
        movie_response = requests.get(movie_url, params=movie_params)
        movie_data = movie_response.json()

        # Construct the full poster URL
        base_image_url = 'https://image.tmdb.org/t/p/original'
        poster_path = movie_data.get('poster_path')
        if poster_path:
            poster_url = base_image_url + poster_path
            return poster_url
        else:
            return "No poster available for this movie."
    else:
        return "Movie not found."



# Load the movie data and recommender list
movie = pickle.load(open('movie.pkl', 'rb'))
recommender_dict = pickle.load(open('recommender_dict', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Enter Movie Name',
    movie['title'].values
)

if st.button('Recommend'):
    recommended_movies = recommender_dict[selected_movie_name]

    # Create a horizontal layout using columns
    columns = st.columns(len(recommended_movies))  # Create a column for each recommendation

    for i, movie_title in enumerate(recommended_movies):
        with columns[i]:  # Use the corresponding column
            st.write(movie_title)  # Display the movie title
            poster_url = get_movie_poster(movie_title)
            if poster_url:
                st.image(poster_url, caption=movie_title, width=150)  # Display the poster image
            else:
                st.write("No poster available.")
