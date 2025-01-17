import streamlit as st
import mysql.connector, time
import form
import chatbot
import random
from datetime import datetime

def decoder(s):
    s.strip()
    for i in emotion_map:
        s = s.replace(i,emotion_map[i]+",")
    s = s.strip()
    s = s[0:len(s)-1]
    return s

def connect_to_database():
    # Database connection configuration
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'comp_project'
    }
    try:
        connection = mysql.connector.connect(**db)
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

def search_song_by_title_or_artist(cursor, tora):
    try:
        query = f"""
            SELECT *
            FROM songs
            WHERE name LIKE '%{tora}%' or artist like '%{tora}%' 
            ORDER BY name;
        """
        cursor.execute(query)
        songs = cursor.fetchall()
        
        query = f"""
            SELECT *
            FROM rc_songs
            WHERE name LIKE '%{tora}%' or artist like '%{tora}%' 
            ORDER BY name;
        """
        cursor.execute(query)
        songs += cursor.fetchall()
        
        return songs
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return None

# Emotion ID mapping
emotion_map = {
    "HPY": "Happy",
    "SAD": "Sad",
    "MTV": "Motivational",
    "CLM": "Calm",
    "ENR": "Energetic",
    "FCS": "Focused",
    "LOV": "Love",
    "HBR": "Heartbreak",
    "CHL": "Chill",
    "PRT": "Party",
    "ANG": "Angry"
}

# Synonym mapping for identifying emotions
emotion_synonyms = {
    "Happy": ["happy","lovely", "good", "joyful", "cheerful","amazing", "content", "elated", "delighted", "glad", "pleased", "ecstatic", "jubilant", "upbeat"],
    "Sad": ["sad", "unhappy", "down", "gloomy", "depressed", "melancholy", "sorrowful", "heartbroken", "miserable", "dejected", "mournful"],
    "Love": ["love", "affection", "romance", "adore", "passion", "infatuation", "fondness", "devotion", "caring", "enamored", "tenderness"],
    "Energetic": ["energetic", "lively", "vibrant", "active", "dynamic", "enthusiastic", "spirited", "vigorous", "peppy", "bouncy", "animated"],
    "Motivational": ["motivational", "inspiring", "uplifting", "encouraging", "driven", "ambitious", "determined", "empowering", "stimulating", "motivating", "rousing"],
    "Heartbreak": ["heartbreak", "devastated", "broken", "sorrowful", "pained", "hurt", "anguished", "crushed", "grief-stricken", "despondent", "forlorn"],
    "Chill": ["chill", "relaxed", "laid-back", "mellow", "easygoing", "calm", "tranquil", "serene", "peaceful", "untroubled", "composed"],
    "Calm": ["calm", "serene", "peaceful", "tranquil", "composed", "still", "placid", "quiet", "relaxed", "soothing", "unruffled"],
    "Party": ["party", "celebration", "festivity", "gathering", "bash", "rave", "fiesta", "shindig", "soiree", "jamboree", "carnival"],
    "Focused": ["focused", "concentrated", "attentive", "alert", "determined", "intent", "engaged", "immersed", "fixated", "dedicated", "absorbed"],
    "Angry": ["irritated","angry", "furious", "mad", "irate", "enraged", "outraged", "livid", "annoyed", "fuming", "infuriated", "aggravated"]
}

# Function to fetch songs based on emotion ID
def fetch_songs_by_emotion(cursor, emotion_id, limit=5):
    try:
        query = f"""
            SELECT *
            FROM songs 
            WHERE emotion_id like '%{emotion_id}%'
            ORDER BY RAND() 
            LIMIT {limit}
        """
        cursor.execute(query)
        songs = cursor.fetchall()

        query = f"""
            SELECT *
            FROM rc_songs
            WHERE emotion_id like '%{emotion_id}%' 
            ORDER BY rand()
            LIMIT {limit}
        """
        cursor.execute(query)
        songs += cursor.fetchall()
        random.shuffle(songs)
        songs = songs[0:limit]

        return songs
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return None

# Function to identify emotion and synonym from sentence
def identify_emotion_from_sentence(sentence):
    sentence = sentence.lower()
    for emotion, synonyms in emotion_synonyms.items():
        for synonym in synonyms:
            if synonym in sentence:
                return emotion, synonym
    return None, None

def get_text_color():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
        text_color = "#000000"  # Black for daytime
    else:
        text_color = "#FFFFFF"  # White for nighttime
    return text_color

def get_text_color_for_desc():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
        text_color = "#555555" 
    else:
        text_color = "#DDDDDD"
    return text_color

def main():
    # CSS for fade-out animation and styling
    fade_style = """
    <style>
    .fade-out {
        animation: fadeOut 1s forwards;
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        100% { opacity: 0; }
    }
    .song-details {
        color: black; /* Main text color */
        background-color: #ADD8E6; /* Light Blue box color */
        padding: 10px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;  /* Add margin at the bottom */
    }
    .song-details a {
        color: #003366; /* Darker hyperlink color */
    }
    </style>
    """
    
    st.markdown(fade_style, unsafe_allow_html=True)
    intro_visible = st.session_state.get('intro_visible', True)
    song_form_visible = st.session_state.get('song_form_visible', False)
    search_form_visible = st.session_state.get('search_form_visible', False)

    if intro_visible and not song_form_visible and not search_form_visible:
        # Display the home page
        st.title("Home")
        text_color = get_text_color()
        text_color_for_desc = get_text_color_for_desc()
        st.markdown(f'<p style="color:{text_color}; font-size: 24px; font-family: Arial, sans-serif;">This is Spots. I love to talk to people and recommend some cool songs based on your mood!</p>', unsafe_allow_html=True)        

        # Layout for the chat button and description
        col1, col2 = st.columns([1, 3])  # Adjust the column ratios as needed

        with col1:
            if st.button("LET'S CHAT!", key="chat_button", use_container_width=False):
                st.session_state.chat_history = []
                st.session_state.conversation = []
                st.session_state.intro_visible = False
                st.rerun()
        with col2:
            st.markdown(f"""
                <p style="color: {text_color_for_desc}; font-size: 16px; font-family: Arial, sans-serif;">
                Engage in a conversation with our chatbot and find song recommendations tailored to your mood.
                </p>
            """, unsafe_allow_html=True)

        # Layout for the song recommendation button and description
        col1, col2 = st.columns([1, 3])  # Reusing columns

        with col1:
            if st.button("Recommend us some songs!", key="recommend_button", use_container_width=False):
                st.session_state.intro_visible = False
                st.session_state.song_form_visible = True
                time.sleep(1)
                st.rerun()
        with col2:
            st.markdown(f"""
                <p style="color: {text_color_for_desc}; font-size: 16px; font-family: Arial, sans-serif;">
                Have a song in mind that's not listed? You can add it here! Let's build the perfect playlist together!
                </p>
            """, unsafe_allow_html=True)

        # Layout for the search button and description
        col1, col2 = st.columns([1, 3])  # Reusing columns

        with col1:
            if st.button("Search for a Song", key="search_button", use_container_width=False):
                st.session_state.intro_visible = False
                st.session_state.search_form_visible = True
                time.sleep(1)
                st.rerun()
        with col2:
            st.markdown(f"""
                <p style="color: {text_color_for_desc}; font-size: 16px; font-family: Arial, sans-serif;">
                Looking for a specific song? Enter its title or artist name, and we’ll help you find it!
                </p>
            """, unsafe_allow_html=True)

        # Button for logging out
        if st.button("Log Out", key="logout_button", use_container_width=False):
            st.session_state.page = "login"
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    elif song_form_visible:
        # Display the song recommendation form
        form.form()

        # Add a Go To Home Page button
        if st.button("Go To Home Page"):
            st.session_state.song_form_visible = False
            st.session_state.intro_visible = True
            st.rerun()

    elif search_form_visible:
        # Display the search form for searching a specific song
        connection = connect_to_database()
        if not connection:
            st.error("Failed to connect to database.")
            return

        cursor = connection.cursor()

        with st.form(key='search_form'):
            text_color = get_text_color()
            st.markdown(f"""
            <style>
            .input-label {{
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: Arial, sans-serif; /* You can change the font family */
                margin-bottom: -35px; /* No space between the label and input field */
                color: {text_color}; /* Dynamic color based on time */
            }}
            .input-label-for-search-results {{
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: Arial, sans-serif; /* You can change the font family */
                margin-bottom: -5px; /* No space between the label and input field */
                color: {text_color}; /* Dynamic color based on time */
            }}
            </style>
            """, unsafe_allow_html=True)
            st.markdown('<p class="input-label">Search for a specific song:</p>', unsafe_allow_html=True)
            search_input = st.text_input("", placeholder="Enter song title/artist")
            search_button = st.form_submit_button("Search")
            
            if search_button:   
                if not search_input.strip():
                    st.toast("Please enter something to search for.")
                else:
                    # Fetch songs by title
                    songs = search_song_by_title_or_artist(cursor, search_input)
                    
                    if songs:
                        st.markdown(f'<p class="input-label-for-search-results">Search results for "{search_input}":</p>', unsafe_allow_html=True)
                        for song in songs:
                            ei = decoder(song[2])
                            st.markdown(f"""
                            <div class="song-details">
                                <strong>Name:</strong> {song[0]}<br>
                                <strong>Artist:</strong> {song[1]}<br>
                                <strong>Emotion:</strong> {ei}<br>
                                <strong>Genre:</strong> {song[3]}<br>
                                <strong>Spotify Link:</strong> <a href="{song[4]}">{song[0]}</a>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.toast(f"No songs found for '{search_input}'.")

        cursor.close()
        connection.close()

        # Add a Go To Home Page button
        if st.button("Go To Home Page"):
            st.session_state.search_form_visible = False
            st.session_state.intro_visible = True
            st.rerun()

    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ''
            
        st.title("🤖 Emotion-recognizing chatbot")
        chatbot.main()

        if st.button("Go To Home Page"):
            st.session_state.song_form_visible = False
            st.session_state.search_form_visible = False
            st.session_state.intro_visible = True
            st.rerun()

if __name__ == "__main__":
    main()

