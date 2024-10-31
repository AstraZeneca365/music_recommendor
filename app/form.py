import streamlit as st  # type: ignore
import mysql.connector as mc  # type: ignore
from datetime import datetime  # Import datetime for time-based color changes

# Define emotion mappings
valid_emotions = {
    "CLM": "Calm", "ENR": "Energetic", "SAD": "Sad", "FCS": "Focused",
    "MTV": "Motivational", "LOV": "Love", "HBR": "Heartbreak",
    "CHL": "Chill", "PRT": "Party", "ANG": "Angry", "HPY": "Happy"
}

# Define genres
genres = [
    "Pop", "Rock", "Jazz", "EDM","Indie-Pop","Funk","Rap", 
    "Bollywood","Carnatic","Hindustani","Ghazal", "Indie"
]

def get_selected_emotion_ids(selected_emotions):
    selected_ids = [emotion_id for emotion_id, emotion in valid_emotions.items() if emotion in selected_emotions]
    return " " + ' '.join(selected_ids) + " "

def get_text_color():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
        return "#000000"  # Black for daytime
    else:
        return "#FFFFFF"  # White for nighttime

def form():
    st.title("Recommend Some Songs! 🎶", anchor="top")

    text_color = get_text_color()  # Get the appropriate text color based on time

    # Custom CSS for input field labels and mood options
    st.markdown(f"""
        <style>
            .input-label {{
                font-size: 18px;
                font-family: Arial, sans-serif;
                margin-bottom: -15px;
                color: {text_color}; 
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.form(key='recommendation_form'):
        # Song name input
        st.markdown('<p class="input-label">Enter the name of the song:</p>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="e.g., I Ain't Worried")

        # Artist name input
        st.markdown('<p class="input-label">Enter the name of the artist:</p>', unsafe_allow_html=True)
        artist = st.text_input("", placeholder="e.g., One Republic")
        
        # Emotion checkboxes using Streamlit's st.checkbox
        st.markdown('<p class="input-label">Select the mood(s) of your song:</p>', unsafe_allow_html=True)
        selected_emotions = []
        cols = st.columns(3)  # Create 3 columns for horizontal checkboxes
        for idx, (emotion_id, emotion_name) in enumerate(valid_emotions.items()):
            with cols[idx % 3]:  # Distribute across columns
                if st.checkbox(emotion_name):
                    selected_emotions.append(emotion_name)

        # Genre dropdown
        st.markdown('<p class="input-label">Select the genre of your song:</p>', unsafe_allow_html=True)
        genre = st.selectbox("", genres)  # Dropdown with genre options

        # Spotify link input
        st.markdown('<p class="input-label">Paste the Spotify link of the song:</p>', unsafe_allow_html=True)
        spotify_link = st.text_input("")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if not (name and artist and selected_emotions and genre and spotify_link):
            st.toast("Please fill all the fields.", icon="❗")
        else:
            # Get emotion_id from selected emotions
            emotion_id = get_selected_emotion_ids(selected_emotions)
            
            db = {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'database': 'comp_project'
            }
            connection = mc.connect(**db)
            cursor = connection.cursor()

            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS rc_songs(
                    name VARCHAR(50),
                    artist VARCHAR(100),
                    emotion_id CHAR(20),
                    genre VARCHAR(20),
                    spotify_link VARCHAR(80)
                );
            """)

            cursor.execute("SELECT * FROM rc_songs WHERE name = %s AND artist = %s", (name, artist))
            result1 = cursor.fetchone()
            cursor.execute("SELECT * FROM songs WHERE name = %s AND artist = %s", (name, artist))
            result2 = cursor.fetchone()

            if (not result1) and (not result2):
                cursor.execute(
                    "INSERT INTO rc_songs (name, artist, emotion_id, genre, spotify_link) VALUES (%s, %s, %s, %s, %s)",
                    (name, artist, emotion_id, genre, spotify_link)
                )
                connection.commit()
                st.toast('Thanks for the recommendation! 😊')
            else:
                st.toast("This song has already been recommended.", icon="❗")

            cursor.close()
            connection.close()

if __name__ == "__main__":
    form()
