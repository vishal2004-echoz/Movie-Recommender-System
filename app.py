import pickle
import streamlit as st
import requests
import time
from googleapiclient.discovery import build
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore", category=FutureWarning)
# ----------------- CONFIG -----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

API_KEY = "bf34d9a"  # OMDb API Key
YOUTUBE_API_KEY = "AIzaSyCtRmuczhLVye3FA7c3j1wvfjXoykoyg_g"  # YouTube Data API Key
BASE_URL = "http://www.omdbapi.com/"
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"
# ----------------- LOAD DATA -----------------
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------- LOAD DATA -----------------
def load_data():
    # Load movies DataFrame
    movies = pickle.load(open('data/movie_list.pkl', 'rb'))

    # Ensure 'tags' column exists
    if 'tags' not in movies.columns:
        feature_cols = [col for col in ['genres', 'cast', 'description'] if col in movies.columns]
        if feature_cols:
            movies['tags'] = movies[feature_cols].fillna('').agg(' '.join, axis=1)
        else:
            movies['tags'] = movies['title'].fillna('')

    # Compute similarity matrix dynamically
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vector)

    return movies, similarity

# Load movies and similarity
movies, similarity = load_data()
# ----------------- CSS -----------------
st.markdown("""
<style>
.stApp { background-color: #141414; color: #fff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
@keyframes fadeIn { from {opacity:0; transform: translateY(20px);} to {opacity:1; transform: translateY(0);} }
.fade-in { animation: fadeIn 0.8s ease forwards; }
.card { background-color: #1c1c1c; border-radius: 10px; overflow: hidden; text-align: center; margin: 5px; transition: transform 0.3s ease, box-shadow 0.3s ease; position: relative; cursor: pointer; }
.card:hover { transform: scale(1.08); box-shadow: 0 10px 25px rgba(229,9,20,0.7); }
.card .overlay { position: absolute; bottom: 0; background: rgba(0,0,0,0.85); color: #fff; width: 100%; padding: 10px; opacity: 0; transition: opacity 0.3s ease; }
.card:hover .overlay { opacity: 1; }
.title { color: #e50914; font-weight: bold; margin: 8px 0 4px 0; }
.details { font-size: 0.85rem; color: #aaa; }
.carousel { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 10px; }
.carousel::-webkit-scrollbar { height: 8px; }
.carousel::-webkit-scrollbar-thumb { background: #e50914; border-radius: 4px; }
.carousel::-webkit-scrollbar-track { background: #222; }
input[type="text"] { padding: 10px; width: 100%; border-radius: 5px; border: none; font-size: 1rem; }
.selected-movie { animation: fadeIn 1s ease forwards; }
</style>
""", unsafe_allow_html=True)


# ----------------- SESSION STATE -----------------
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []

# ----------------- FETCH MOVIE -----------------
@st.cache_data
def fetch_movie(title):
    try:
        params = {"t": title, "apikey": API_KEY}
        data = requests.get(BASE_URL, params=params).json()
        if data.get("Response") == "True":
            return {
                "poster": data.get("Poster") if data.get("Poster") != "N/A" else PLACEHOLDER,
                "rating": data.get("imdbRating", "N/A"),
                "year": data.get("Year", ""),
                "genre": data.get("Genre", "").split(",")[0],
                "plot": data.get("Plot", "No description available")
            }
    except:
        pass
    return {"poster": PLACEHOLDER, "rating": "N/A", "year": "", "genre": "", "plot": "No description available"}

# ----------------- YOUTUBE TRAILER -----------------
def fetch_youtube_trailer(movie_title):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            q=f"{movie_title} official trailer",
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()
        items = response.get("items", [])
        if not items:
            return None
        video_id = items[0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    except:
        return None

# ----------------- RECOMMEND -----------------
def recommend(movie, n):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters, ratings, years, genres = [], [], [], [], []
    for i in distances[1:n+1]:
        title = movies.iloc[i[0]].title
        info = fetch_movie(title)
        names.append(title)
        posters.append(info["poster"])
        ratings.append(info["rating"])
        years.append(info["year"])
        genres.append(info["genre"])
        time.sleep(0.05)
    return names, posters, ratings, years, genres

# ----------------- UI -----------------
st.markdown("<h1 style='color:#e50914;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("---")

# ----------------- SEARCH BAR -----------------
search_query = st.text_input("Search for a movie:")
if search_query:
    filtered_movies = movies[movies['title'].str.contains(search_query, case=False)]
else:
    filtered_movies = movies

if len(filtered_movies) > 0:
    selected_movie = st.selectbox("Select a movie:", filtered_movies['title'].values)
else:
    st.warning("No movies found. Please try a different search.")
    selected_movie = None

if selected_movie:
    selected_info = fetch_movie(selected_movie)

    # ----------------- SELECTED MOVIE -----------------
    st.markdown("## Selected Movie")
    c1, c2 = st.columns([1, 3])
    with c1:
        st.image(selected_info["poster"], width=300)
    with c2:
        st.markdown(f"<div class='selected-movie'><h2 style='color:#e50914'>{selected_movie}</h2></div>", unsafe_allow_html=True)
        st.write(f"📅 {selected_info['year']} | 🎭 {selected_info['genre']}")
        st.write(f"⭐ {selected_info['rating']}")
        st.write("📖", selected_info["plot"])
        if st.button(f"❤️ Add to Favorites"):
            if selected_movie not in st.session_state['favorites']:
                st.session_state['favorites'].append(selected_movie)

        # ----------------- TRAILER -----------------
        trailer_url = fetch_youtube_trailer(selected_movie)
        if trailer_url:
            st.markdown("### 🎥 Trailer")
            st.video(trailer_url)
        else:
            st.write("🎥 Trailer not found.")

    # ----------------- RECOMMENDATIONS -----------------
    n = st.slider("Number of recommendations:", 1, 10, 5)
    names, posters, ratings, years, genres = recommend(selected_movie, n)
    st.markdown("## Recommended for You")
    st.markdown("<div class='carousel'>", unsafe_allow_html=True)
    cards_html = ""
    for i in range(n):
        cards_html += f"""
        <div class="card" style="width:150px; display:inline-block;">
            <img src="{posters[i]}" width="100%">
            <div class="overlay">
                <div class="title">{names[i]}</div>
                <div class="details">{years[i]} | {genres[i]} | ⭐ {ratings[i]}</div>
                <div style="font-size:0.75rem;">{fetch_movie(names[i])["plot"]}</div>
            </div>
        </div>
        """
    st.markdown(cards_html + "</div>", unsafe_allow_html=True)

# ----------------- FAVORITES -----------------
if st.session_state['favorites']:
    st.markdown("## My Favorites")
    st.markdown("<div class='carousel'>", unsafe_allow_html=True)
    fav_html = ""
    for fav in st.session_state['favorites']:
        info = fetch_movie(fav)
        fav_html += f"""
        <div class="card" style="width:150px; display:inline-block;">
            <img src="{info['poster']}" width="100%">
            <div class="overlay">
                <div class="title">{fav}</div>
                <div class="details">{info['year']} | {info['genre']} | ⭐ {info['rating']}</div>
                <div style="font-size:0.75rem;">{info['plot']}</div>
            </div>
        </div>
        """
    st.markdown(fav_html + "</div>", unsafe_allow_html=True)

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("<p style='color:#aaa; text-align:center;'>Powered by OMDb API 🎬</p>", unsafe_allow_html=True)
