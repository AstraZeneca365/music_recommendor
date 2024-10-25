import streamlit as st # type: ignore
import mysql.connector as mc # type: ignore

# Define emotion mappings
valid_emotions = {
    "CLM": "Calm", "ENR": "Energetic", "SAD": "Sad", "FCS": "Focused", 
    "MTV": "Motivational", "LOV": "Love", "HBR": "Heartbreak", 
    "CHL": "Chill", "PRT": "Party", "ANG": "Angry", "HPY": "Happy"
}

def get_selected_emotion_ids(selected_emotions):
    selected_ids = [emotion_id for emotion_id, emotion in valid_emotions.items() if emotion in selected_emotions]
    return " " + ' '.join(selected_ids) + " "

def form():
    st.title("Recommend some of your Favourites!!")

    with st.form(key='recommendation_form'):
        name = st.text_input("Enter the name of the song", placeholder="e.g., I Ain't Worried")
        artist = st.text_input("Enter the name of the artist", placeholder="e.g., One Republic")
        
        # Horizontal grouped checkboxes for emotions
        st.write("Select the mood(s) of your song:")
        selected_emotions = []
        cols = st.columns(3)  # Create 3 columns for horizontal checkboxes
        for idx, (emotion_id, emotion_name) in enumerate(valid_emotions.items()):
            with cols[idx % 3]:  # Iterate through each emotion, assigning to columns
                if st.checkbox(emotion_name):
                    selected_emotions.append(emotion_name)

        genre = st.text_input("Enter the genre of your song", placeholder="e.g., Pop")
        spotify_link = st.text_input("Paste the Spotify link of the song")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if not (name and artist and selected_emotions and genre and spotify_link):
            st.error("Please fill all the fields.")
        else:
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

            cursor.execute(f"SELECT * FROM rc_songs WHERE name = %s AND artist = %s", (name, artist))
            result = cursor.fetchone()

            if not result:
                cursor.execute(
                    "INSERT INTO rc_songs (name, artist, emotion_id, genre, spotify_link) VALUES (%s, %s, %s, %s, %s)",
                    (name, artist, emotion_id, genre, spotify_link)
                )
                connection.commit()
                st.toast('Thanks for the recommendation', icon='😍')
            else:
                st.warning("This song has already been recommended.")

            cursor.close()
            connection.close()

