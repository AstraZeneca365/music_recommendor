import streamlit as st
import mysql.connector, time
from app import form


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
        'password': '1234',
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
        return songs
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return None



# Emotion ID mapping
emotion_ids = ["CLM", "ENR", "SAD", "FCS", "MTV", "LOV", "HBR", "CHL", "PRT", "ANG", "HPY"]
emotions = ["Calm", "Energetic", "Sad", "Focused", "Motivational", "Love", "Heartbreak", "Chill", "Party", "Angry", "Happy"]

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
    "Happy": ["happy", "good", "joyful", "cheerful", "content", "elated", "delighted", "glad", "pleased", "ecstatic", "jubilant", "upbeat"],
    "Sad": ["sad", "unhappy", "down", "gloomy", "depressed", "melancholy", "sorrowful", "heartbroken", "miserable", "dejected", "mournful"],
    "Love": ["love", "affection", "romance", "adore", "passion", "infatuation", "fondness", "devotion", "caring", "enamored", "tenderness"],
    "Energetic": ["energetic", "lively", "vibrant", "active", "dynamic", "enthusiastic", "spirited", "vigorous", "peppy", "bouncy", "animated"],
    "Motivational": ["motivational", "inspiring", "uplifting", "encouraging", "driven", "ambitious", "determined", "empowering", "stimulating", "motivating", "rousing"],
    "Heartbreak": ["heartbreak", "devastated", "broken", "sorrowful", "pained", "hurt", "anguished", "crushed", "grief-stricken", "despondent", "forlorn"],
    "Chill": ["chill", "relaxed", "laid-back", "mellow", "easygoing", "calm", "tranquil", "serene", "peaceful", "untroubled", "composed"],
    "Calm": ["calm", "serene", "peaceful", "tranquil", "composed", "still", "placid", "quiet", "relaxed", "soothing", "unruffled"],
    "Party": ["party", "celebration", "festivity", "gathering", "bash", "rave", "fiesta", "shindig", "soiree", "jamboree", "carnival"],
    "Focused": ["focused", "concentrated", "attentive", "alert", "determined", "intent", "engaged", "immersed", "fixated", "dedicated", "absorbed"],
    "Angry": ["angry", "furious", "mad", "irate", "enraged", "outraged", "livid", "annoyed", "fuming", "infuriated", "aggravated"]
}

# Function to fetch songs based on emotion ID
def fetch_songs_by_emotion(cursor, emotion_id, limit=5):
    try:
        query = f"""
            SELECT *
            FROM songs 
            WHERE emotion_id like '%{emotion_id}%'
            ORDER BY RAND() 
            LIMIT {limit};
        """
        cursor.execute(query)
        songs = cursor.fetchall()
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

def main():

    # CSS for fade-out animation
    fade_style = """
    <style>
    .fade-out {
        animation: fadeOut 1s forwards;
    }

    @keyframes fadeOut {
        0% { opacity: 1; }
        100% { opacity: 0; }
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
        st.write("This is Spots. I love to talk to people and recommend you some cool songs based on your mood.")
        if st.button("LET'S CHAT!"):
            st.session_state.intro_visible = False
            time.sleep(1)
            st.rerun()

        elif st.button("Recommend us some songs!"):
            st.session_state.intro_visible = False
            st.session_state.song_form_visible = True
            time.sleep(1)
            st.rerun()

        elif st.button("Search for a Song"):
            st.session_state.intro_visible = False
            st.session_state.search_form_visible = True
            time.sleep(1)
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
            search_input = st.text_input("Search for a specific song:", placeholder="Enter song title/artist")
            search_button = st.form_submit_button("Search")
            
            if search_button:
                if not search_input.strip():
                    st.warning("Please enter something to search for.")
                else:
                    # Fetch songs by title
                    songs = search_song_by_title(cursor, search_input)
                    
                    if songs:
                        st.markdown(f'<p class="header">Search results for "{search_input}":</p>', unsafe_allow_html=True)
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
                        st.warning(f"No songs found for '{search_input}'.")

        cursor.close()
        connection.close()

        # Add a Go To Home Page button
        if st.button("Go To Home Page"):
            st.session_state.search_form_visible = False
            st.session_state.intro_visible = True
            st.rerun()

    else:
        # Display the mood input and song recommendation section
        st.markdown("""
        <style>
            .title {
                color: #FF6347; /* Tomato color */
                font-size: 36px;
                font-weight: bold;
            }
            .header {
                color: #4682B4; /* SteelBlue color */
                font-size: 28px;
            }
            .description {
                color: #32CD32; /* LimeGreen color */
                font-size: 18px;
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
        """, unsafe_allow_html=True)


        st.markdown('<p class="title">🎵 Song Recommender Chatbot 🎵</p>', unsafe_allow_html=True)

        st.markdown("""
        <p class="description">
        <br> 
        Describe your mood or enter a sentence that reflects how you're feeling, and we'll recommend some songs that match your mood.
        </p>
        """, unsafe_allow_html=True)

        connection = connect_to_database()
        if not connection:
            st.error("Failed to connect to database.")
            return

        cursor = connection.cursor()

        with st.form(key='mood_form'):
            user_input = st.text_input("Describe your mood:", placeholder="e.g., I am feeling really joyful today.")
            num_songs = st.selectbox("How many songs would you like?", options=range(1, 11), index=4)

            # Add two columns for buttons
            col1, col2 = st.columns([2, 1])
            with col1:
                submit_button = st.form_submit_button("Get Recommendations")
            with col1:
                random_fun_button = st.form_submit_button("Random Song Generator!")

            button_pressed = False
            
            if submit_button:
                button_pressed =  True
                if not user_input.strip():
                    st.warning("Please enter something to get recommendations.")
                else:
                    # Identify the mood and corresponding synonym
                    mood, synonym = identify_emotion_from_sentence(user_input) or (
                        user_input.capitalize() if user_input.capitalize() in emotions else (None, None))

                    if mood:
                        # Get the corresponding emotion ID
                        emotion_id = emotion_ids[emotions.index(mood)]

                        # Fetch songs based on the identified emotion
                        songs = fetch_songs_by_emotion(cursor, emotion_id, limit=num_songs)

                        if songs:
                            display_mood = synonym if synonym else mood
                            st.markdown(f'<p class="header">Here are some amazing songs for "{display_mood}":</p>',
                                        unsafe_allow_html=True)
                            
                            for song in songs:
                                ei = song[2]
                                ei = ei.replace(emotion_id,"")
                                ei = decoder(ei)
                                if ei == "":
                                    ei = "N/A"

                                st.markdown(f"""
                                <div class="song-details">
                                    <strong>Name:</strong> {song[0]}<br>
                                    <strong>Artist:</strong> {song[1]}<br>
                                    <strong>Alternate Emotion:</strong> {ei}<br>
                                    <strong>Genre:</strong> {song[3]}<br>
                                    <strong>Spotify Link:</strong> <a href="{song[4]}">{song[0]}</a>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.warning(f"No songs found for '{mood}'.")
                    else:
                        st.error("Sorry, I don't understand that mood. Please try again.")

            elif random_fun_button:
                # Fetch a random song
                button_pressed = True
                query = """
                    SELECT *  
                    FROM songs 
                    ORDER BY RAND() 
                    LIMIT 1;
                """
                # name artist, em_id, genre, spotify

                cursor.execute(query)
                random_song = cursor.fetchone()
                ei = decoder(random_song[2])

                if random_song:
                    st.markdown(f'<p class="header">Here is a random song for you:</p>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="song-details">
                        <strong>Name:</strong> {random_song[0]}<br>
                        <strong>Artist:</strong> {random_song[1]}<br>
                        <strong>Emotion:</strong> {ei}<br>
                        <strong>Genre:</strong> {random_song[3]}<br>
                        <strong>Spotify Link:</strong> <a href="{random_song[4]}">{random_song[0]}</a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No songs found.")

            cursor.close()
            connection.close()

        # Add a Go To Home Page button
        if st.button("Go To Home Page"):
            st.session_state.song_form_visible = False
            st.session_state.intro_visible = True
            st.rerun()


if __name__ == "__main__":
    main()
