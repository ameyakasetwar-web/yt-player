import streamlit as st
from googleapiclient.discovery import build

# Page Config
st.set_page_config(page_title="Streamlit Music Player", layout="wide")

# --- Authentication ---
# Fetches key from .streamlit/secrets.toml
try:
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
except Exception as e:
    st.error("Missing API Key in secrets. Please add 'YOUTUBE_API_KEY'.")
    st.stop()

# --- App UI ---
st.title("🎵 YouTube Music Search & Play")

# Sidebar for Search
with st.sidebar:
    st.header("Search Settings")
    query = st.text_input("Search for music:", placeholder="e.g. Lofi Hip Hop")
    max_results = st.slider("Number of results", 5, 20, 10)
    search_button = st.button("Search")

# --- Search Logic ---
if search_button and query:
    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            videoCategoryId="10" # Music Category
        )
        response = request.execute()
        st.session_state['search_results'] = response.get('items', [])
    except Exception as e:
        st.error(f"API Error: {e}")

# --- Layout: Results and Player ---
col_list, col_player = st.columns([1, 1.5])

with col_list:
    st.subheader("Results")
    if 'search_results' in st.session_state:
        for item in st.session_state['search_results']:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            channel = item['snippet']['channelTitle']
            
            # Using a container for each result
            with st.container(border=True):
                st.write(f"**{title}**")
                st.caption(f"Channel: {channel}")
                if st.button("Select to Play", key=video_id):
                    st.session_state['active_video'] = video_id

with col_player:
    st.subheader("Player")
    if 'active_video' in st.session_state:
        video_url = f"https://www.youtube.com/watch?v={st.session_state['active_video']}"
        st.video(video_url)
    else:
        st.info("Select a song from the list to start playing.")