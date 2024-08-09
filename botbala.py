import streamlit as st
import mysql.connector
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(jfif_file):
    bin_str = get_base64(jfif_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jfif;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)




set_background('Z:\OIP.jfif')

def connect_to_database():
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'python_connector'
    }
    try:
        connection = mysql.connector.connect(**db)
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Emotion ID mapping
emotion_ids = ["CLM", "ENR", "SAD", "FCS", "MTV", "LOV", "HBR", "CHL", "PRT", "ANG", "HPY"]
emotions = ["Calm", "Energetic", "Sad", "Focused", "Motivational", "Love", "Heartbreak", "Chill", "Party", "Angry", "Happy"]

# Synonym mapping
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
            SELECT name, artist, genre, spotify_link 
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
    # Sample base64 image data; replace with your actual image data
    background_image_base64 = "data:image/jfif;base64,<your-base64-image-data-here>"

    # Use markdown to insert CSS
    st.markdown(
        f"""
        <style>
            .reportview-container {{
                background: url("{background_image_base64}");
                background-size: cover;
                position: relative; /* Allow positioning of overlay */
            }}

            .main {{
                background-color: #ffffff;  /* Solid white background */
                border-radius: 10px; 
                padding: 20px;  
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); 
                position: relative; /* Ensure it layers correctly */
                z-index: 1; /* Bring the box to the front */
                max-width: 800px; /* Optional: set a maximum width for the box */
                margin: auto; /* Center the box horizontally */
                max-height: 100vh; /* Limit height to 90% of the viewport height */
                overflow-y: auto; /* Enable vertical scrolling if content overflows */
            }}

            /* Custom text styles */
            .title {{
                color: #ff6347; /* tomato color */
                font-size: 36px;
                font-weight: bold;
                text-align: center; /* Center the title */
                margin: 0; /* Remove default margin */
            }}
            .header {{
                color: #4682b4; /* steelblue color */
                font-size: 28px;
                margin: 10px 0; /* Add some margin for spacing */
            }}
            .description {{
                color: #32cd32; /* limegreen color */
                font-size: 18px;
                margin: 10px 0; /* Add some margin for spacing */
            }}
            .song-details {{
                background-color: #47a2ec; /* light blue */
                padding: 10px;
                border-radius: 5px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main content area - wrap content in a div with class 'main'
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Title and description
    st.markdown('<p class="title">🎵 Song Recommender Chatbot 🎵</p>', unsafe_allow_html=True)

    st.markdown("""
    <p class="description">
    Describe your mood or enter a sentence that reflects how you're feeling, and we'll recommend some songs that match your mood.
    </p>
    """, unsafe_allow_html=True)

    # Database connection logic (ensure these functions are defined properly)
    connection = connect_to_database()
    if not connection:
        st.error("Failed to connect to database.")
        return

    cursor = connection.cursor()

    with st.form(key='mood_form'):
        user_input = st.text_input("Describe your mood:", placeholder="e.g., I am feeling really joyful today.")
        num_songs = st.selectbox("How many songs would you like?", options=range(1, 11), index=4)
        submit_button = st.form_submit_button("Get Recommendations")

        if submit_button:
            if not user_input.strip():
                st.warning("Please enter something to get recommendations.")
            else:
                mood, synonym = identify_emotion_from_sentence(user_input) or (
                    user_input.capitalize() if user_input.capitalize() in emotions else (None, None))

                if mood:
                    emotion_id = emotion_ids[emotions.index(mood)]

                    songs = fetch_songs_by_emotion(cursor, emotion_id, limit=num_songs)

                    if songs:
                        display_mood = synonym if synonym else mood
                        st.markdown(f'<p class="header">Here are some amazing songs for "{display_mood}":</p>',
                                    unsafe_allow_html=True)
                        for song in songs:
                            st.markdown(f"""
                            <div class="song-details">
                                <strong>Name:</strong> {song[0]}<br>
                                <strong>Artist:</strong> {song[1]}<br>
                                <strong>Genre:</strong> {song[2]}<br>
                                <strong>Spotify Link:</strong> <a href="{song[3]}">{song[0]}</a>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning(f"No songs found for '{mood}'.")
                else:
                    st.error("Sorry, I don't understand that mood. Please try again.")

    cursor.close()
    connection.close()

    # Closing the main content area
    st.markdown('</div>', unsafe_allow_html=True)

# Call the main function to run the app

if __name__ == "__main__":
    main()
