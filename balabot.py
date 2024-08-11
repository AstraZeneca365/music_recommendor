import streamlit as st
import mysql.connector
import time
import form

# Function to connect to the MySQL database
def connect_to_database():
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'comp_project'
    }
    try:
        connection = mysql.connector.connect(**db)
        return connection  # Return the connection object if successful
    except mysql.connector.Error as err:
        st.error(f"error: {err}")  # Display error message if connection fails
        return None  # Return None if connection fails

# Emotion ID and name mapping
emotion_ids = ["clm", "enr", "sad", "fcs", "mtv", "lov", "hbr", "chl", "prt", "ang", "hpy"]
emotions = ["calm", "energetic", "sad", "focused", "motivational", "love", "heartbreak", "chill", "party",
            "angry", "happy"]

# Synonym mapping for different emotions
emotion_synonyms = {
    "happy": ["happy", "good", "joyful", "cheerful", "content", "elated", "delighted", "glad", "pleased", "ecstatic", "jubilant", "upbeat"],
    "sad": ["sad", "unhappy", "down", "gloomy", "depressed", "melancholy", "sorrowful", "heartbroken", "miserable", "dejected", "mournful"],
    "love": ["love", "affection", "romance", "adore", "passion", "infatuation", "fondness", "devotion", "caring", "enamored", "tenderness"],
    "energetic": ["energetic", "lively", "vibrant", "active", "dynamic", "enthusiastic", "spirited", "vigorous", "peppy", "bouncy", "animated"],
    "motivational": ["motivational", "inspiring", "uplifting", "encouraging", "driven", "ambitious", "determined", "empowering", "stimulating", "motivating", "rousing"],
    "heartbreak": ["heartbreak", "devastated", "broken", "sorrowful", "pained", "hurt", "anguished", "crushed", "grief-stricken", "despondent", "forlorn"],
    "chill": ["chill", "relaxed", "laid-back", "mellow", "easygoing", "calm", "tranquil", "serene", "peaceful", "untroubled", "composed"],
    "calm": ["calm", "serene", "peaceful", "tranquil", "composed", "still", "placid", "quiet", "relaxed", "soothing", "unruffled"],
    "party": ["party", "celebration", "festivity", "gathering", "bash", "rave", "fiesta", "shindig", "soiree", "jamboree", "carnival"],
    "focused": ["focused", "concentrated", "attentive", "alert", "determined", "intent", "engaged", "immersed", "fixated", "dedicated", "absorbed"],
    "angry": ["angry", "furious", "mad", "irate", "enraged", "outraged", "livid", "annoyed", "fuming", "infuriated", "aggravated"]
}

# Function to fetch songs based on the given emotion ID
def fetch_songs_by_emotion(cursor, emotion_id, limit=5):
    try:
        query = f"""
            SELECT name, artist, genre, spotify_link 
            FROM songs 
            WHERE emotion_id LIKE '%{emotion_id}%'
            ORDER BY RAND() 
            LIMIT {limit};
        """
        cursor.execute(query)
        songs = cursor.fetchall()  # Fetch all matching songs
        return songs  # Return the list of songs
    except mysql.connector.Error as err:
        st.error(f"mysql error: {err}")  # Display error message if query fails
        return None  # Return None if query fails

# Function to identify emotion and its synonym from the given sentence
def identify_emotion_from_sentence(sentence):
    sentence = sentence.lower()  # Convert the sentence to lowercase
    for emotion, synonyms in emotion_synonyms.items():  # Check each emotion and its synonyms
        for synonym in synonyms:
            if synonym in sentence:  # If a synonym is found, return the emotion and synonym
                return emotion, synonym
    return None, None  # Return None if no emotion is identified

def main():
    # CSS for fade-out animation
    fade_style = """
    <style>
    .fade-out {
        animation: fadeout 1s forwards;
    }

    @keyframes fadeout {
        0% { opacity: 1; }
        100% { opacity: 0; }
    }
    </style>
    """

    st.markdown(fade_style, unsafe_allow_html=True)  # Apply fade-out style
    intro_visible = st.session_state.get('intro_visible', True)  # Track the intro visibility
    song_form_visible = st.session_state.get('song_form_visible', False)  # Track the song form visibility

    # Intro screen
    if intro_visible and not song_form_visible:
        st.title("Home")  # Set the title of the app
        st.write("This is Spots. I love to talk to people and recommend you some cool songs based on your mood.")

        # Button to start chat
        if st.button("Let's chat!"):
            st.session_state.intro_visible = False  # Hide intro
            time.sleep(1)  # Create a small delay
            st.experimental_rerun()  # Rerun the app

        # Button to recommend songs
        elif st.button("Recommend us some songs!"):
            st.session_state.intro_visible = False  # Hide intro
            st.session_state.song_form_visible = True  # Show song form
            time.sleep(1)  # Create a small delay
            st.experimental_rerun()  # Rerun the app

    # Song recommendation form
    elif song_form_visible:
        form.form()  # Call the form function

    else:
        # Custom CSS for styling
        st.markdown("""
        <style>
            .title {
                color: #ff6347; /* tomato color */
                font-size: 36px;
                font-weight: bold;
            }
            .header {
                color: #4682b4; /* steelblue color */
                font-size: 28px;
            }
            .description {
                color: #32cd32; /* limegreen color */
                font-size: 18px;
            }
            .song-details {
                background-color: #f0e68c; /* khaki color */
                padding: 10px;
                border-radius: 5px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
        </style>
        """, unsafe_allow_html=True)

        # Display the song recommender title
        st.markdown('<p class="title">🎵 Song Recommender Chatbot 🎵</p>', unsafe_allow_html=True)

        # Describe how to use the app
        st.markdown("""
        <p class="description">
        <br> 
        Describe your mood or enter a sentence that reflects how you're feeling, and we'll recommend some songs that match your mood.
        </p>
        """, unsafe_allow_html=True)

        connection = connect_to_database()  # Connect to the database
        if not connection:
            st.error("Failed to connect to database.")  # Show error if connection fails
            return  # Exit the function

        cursor = connection.cursor()  # Create a cursor to interact with the database

        # Form to get user input
        with st.form(key='mood_form'):
            user_input = st.text_input("Describe your mood:", placeholder="e.g., I am feeling really joyful today.")
            num_songs = st.selectbox("How many songs would you like?", options=range(1, 11), index=4)  # Default is 5 songs
            submit_button = st.form_submit_button("Get recommendations")  # Submit button

            if submit_button:
                if not user_input.strip():  # Check if the input is empty
                    st.warning("Please enter something to get recommendations.")
                else:
                    # Identify mood and synonym from the user input
                    mood, synonym = identify_emotion_from_sentence(user_input) or (
                        user_input.capitalize() if user_input.capitalize() in emotions else (None, None)
                    )

                    if mood:  # If a mood is identified
                        emotion_id = emotion_ids[emotions.index(mood)]  # Get the corresponding emotion ID

                        songs = fetch_songs_by_emotion(cursor, emotion_id, limit=num_songs)  # Fetch songs

                        if songs:  # If songs are found
                            display_mood = synonym if synonym else mood  # Set display mood
                            # Show the songs
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
                                """, unsafe_allow_html=True)  # Display each song's details
                        else:
                            st.warning(f"No songs found for '{mood}'.")  # No songs found message
                    else:
                        st.error("Sorry, I don't understand that mood. Please try again.")  # Mood not understood message

        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection

# Run the main function
if __name__ == "__main__":
    main()
