import streamlit as st  # type: ignore
import mysql.connector as mc  # type: ignore
from datetime import datetime  # Import datetime for time-based color changes

# Define emotion mappings
valid_emotions = {
    "CLM": "Calm", "ENR": "Energetic", "SAD": "Sad", "FCS": "Focused",
    "MTV": "Motivational", "LOV": "Love", "HBR": "Heartbreak",
    "CHL": "Chill", "PRT": "Party", "ANG": "Angry", "HPY": "Happy"
}

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
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: Arial, sans-serif; /* You can change the font family */
                margin-bottom: -35px; /* No space between the label and input field */
                color: {text_color}; /* Dynamic color based on time */
            }}
            .input-label-select-mood {{
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: Arial, sans-serif; /* You can change the font family */
                margin-bottom: 0px; /* No space between the label and input field */
                color: {text_color}; /* Dynamic color based on time */
            }}
            .mood-label {{
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: Arial, sans-serif; /* You can change the font family */
                color: {text_color}; /* Dynamic color based on time */
                display: inline; /* Ensures the label is inline with the checkbox */
                margin-left: 5px; /* Space between checkbox and label */
            }}
            .checkbox-container {{
                display: inline-block; /* Allows checkboxes to be inline */
                margin-right: 20px; /* Space between checkboxes */
            }}
        </style>
    """, unsafe_allow_html=True)

    with st.form(key='recommendation_form'):
        # Song name input with spacing
        st.markdown('<p class="input-label">Enter the name of the song:</p>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="e.g., I Ain't Worried")
        st.markdown("<br>", unsafe_allow_html=True)  # Add a line break for spacing

        # Artist name input with spacing
        st.markdown('<p class="input-label">Enter the name of the artist:</p>', unsafe_allow_html=True)
        artist = st.text_input("", placeholder="e.g., One Republic")
        st.markdown("<br>", unsafe_allow_html=True)  # Add a line break for spacing
        
        # Horizontal grouped checkboxes for emotions with no label
        st.markdown('<p class="input-label-select-mood">Select the mood(s) of your song:</p>', unsafe_allow_html=True)
        selected_emotions = []
        cols = st.columns(3)  # Create 3 columns for horizontal checkboxes
        for idx, (emotion_id, emotion_name) in enumerate(valid_emotions.items()):
            with cols[idx % 3]:  # Iterate through each emotion, assigning to columns
                checkbox_container = f"""
                    <div class="checkbox-container">
                        <input type="checkbox" id="{emotion_id}" class="mood-checkbox" />
                        <label for="{emotion_id}" class="mood-label">{emotion_name}</label>
                    </div>
                """
                st.markdown(checkbox_container, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)  

        st.markdown('<p class="input-label">Enter the genre of your song:</p>', unsafe_allow_html=True)
        genre = st.text_input("", placeholder="e.g., Pop")
        st.markdown("<br>", unsafe_allow_html=True)  
        st.markdown('<p class="input-label">Paste the Spotify link of the song:</p>', unsafe_allow_html=True)
        spotify_link = st.text_input("")
        st.markdown("<br>", unsafe_allow_html=True)  
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if not (name and artist and selected_emotions and genre and spotify_link):
            st.toast("Please fill all the fields.", icon="❗")
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
                st.toast('Thanks for the recommendation! 😊', icon='😍')  
            else:
                st.toast("This song has already been recommended.",icon="❗")

            cursor.close()
            connection.close()

# Call the form function to run the app
if __name__ == "__main__":
    form()
