# 🎬 Movie Recommender System

A content-based movie recommendation system with a Netflix-inspired UI built using Streamlit.

Tech Stack: Python | Streamlit | scikit-learn | OMDb API | YouTube API  

---

## 📌 About the Project

This project is a content-based movie recommendation system that suggests movies similar to a selected title. It features a Netflix-inspired dark UI with movie posters, trailers, ratings, and a favorites list.

---

## ✨ Features

- 🔍 Search and select from 4800+ movies  
- 🎯 Content-based filtering using cosine similarity  
- 🖼️ Movie posters, ratings, year, and genre via OMDb API  
- 🎥 YouTube trailer integration  
- ❤️ Add movies to a Favorites list  
- 📱 Responsive Netflix-style dark UI with hover effects  
- 🎠 Horizontal scrollable carousel for recommendations  

---

## 📁 Project Structure

movie-recommender/

├── app.py                        
├── requirements.txt              
├── .env                          

├── data/  
│   ├── movie_list.pkl            
│   └── similarity.pkl            

└── notebooks/  
    └── movie_recommender_system.ipynb   

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OMDb API key → https://www.omdbapi.com/
- YouTube Data API v3 key → Google Cloud Console

---

### 1. Clone the Repository

git clone https://github.com/your-username/movie-recommender.git  
cd movie-recommender  

---

### 2. Install Dependencies

pip install -r requirements.txt  
pip install google-api-python-client  

---

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

OMDB_API_KEY=bf34d9a
YOUTUBE_API_KEY=AIzaSyCtRmuczhLVye3FA7c3j1wvfjXoykoyg_g

Update app.py:

from dotenv import load_dotenv  
import os  

load_dotenv()  

API_KEY = os.getenv("OMDB_API_KEY")  
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  

---

### 4. Generate similarity.pkl

jupyter notebook notebooks/movie_recommender_system.ipynb  

This will create:
- movie_list.pkl  
- similarity.pkl  

Move them into the data/ folder.

---

### 5. Run the App

streamlit run app.py  

Open in browser:  
http://localhost:8501  

---

## 🛠️ Tech Stack

Streamlit – Web UI  
scikit-learn – Cosine similarity  
pandas / numpy – Data processing  
OMDb API – Movie metadata & posters  
YouTube Data API v3 – Trailer fetch  
google-api-python-client – YouTube integration  

---

## 🧠 How It Works

- Data Processing: Combines genres, cast, keywords, and overview into one text field  
- Vectorization: Uses CountVectorizer (Bag-of-Words)  
- Similarity: Computes cosine similarity between movie vectors  
- Recommendation: Returns top N most similar movies  

---

## ⚠️ Known Issues & Fixes

- similarity.pkl missing → Run notebook  
- API keys hardcoded → Move to .env  
- google-api-python-client missing → Install manually  
- App crashes → Check .pkl file paths  

---

## 🤝 Contributing

1. Fork the repository  
2. git checkout -b feature/your-feature  
3. git commit -m "Add your feature"  
4. git push origin feature/your-feature  
5. Open Pull Request  

---

## 📄 License

MIT License  

---

## 🙏 Acknowledgements

- OMDb API  
- YouTube Data API  
- TMDB dataset  
- Streamlit  
