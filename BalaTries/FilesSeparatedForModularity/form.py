import streamlit as st
import mysql.connector as mc

def form():
    # Title of the form
    st.title("Recommend Some of Your Favorites!!")

    # Start a form in Streamlit
    with st.form(key='question_form'):
        # Input for the song name
        name = st.text_input("Enter the name of the song", placeholder="e.g., I Ain't Worried")

        # Input for the artist's name
        artist = st.text_input("Enter the name of the artist", placeholder="e.g., One Republic")

        # Input for the emotion of the song, user should provide one of the predefined options
        emotion_id = st.text_input("""
            Describe the emotion of your song--- 
            Available emotions - [happy, energetic, love, motivational, focused, heartbreak, angry, calm, sad, chill, party]
        """)

        # Input for the genre of the song
        genre = st.text_input("Enter the genre of your song", placeholder="e.g., Pop")

        # Input for the Spotify link to the song
        spotify_link = st.text_input("Paste the Spotify link of the song")

        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    # Actions to take after the submit button is pressed
    if submit_button:
        # Validation: check if all fields are filled
        if not (name and artist and emotion_id and genre and spotify_link):
            st.error("Please fill all the fields.")
        else:
            # Database connection details
            db = {
                'host': 'localhost',
                'user': 'root',
                'password': '1234',
                'database': 'comp_project'
            }
            # Establishing a connection to the database
            connection = mc.connect(**db)
            cursor = connection.cursor()

            # Create the table if it doesn't already exist
            query = """
                CREATE TABLE IF NOT EXISTS rc_songs (
                    name VARCHAR(50),
                    artist VARCHAR(100),
                    emotion_id CHAR(20),
                    genre VARCHAR(20),
                    spotify_link VARCHAR(80)
                );
            """
            cursor.execute(query)

            # Fetch all existing songs to check for duplicates
            cursor.execute("SELECT * FROM rc_songs")
            existing_songs = cursor.fetchall()

            # Check if the song is already in the database
            if (name, artist, emotion_id, genre, spotify_link) not in existing_songs:
                # Insert the new song into the database
                cursor.execute("""
                    INSERT INTO rc_songs (name, artist, emotion_id, genre, spotify_link)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, artist, emotion_id, genre, spotify_link))

                # Commit the changes to the database
                connection.commit()
                # Provide feedback to the user that the song was added successfully
                st.success("Song added successfully!")
            else:
                # Notify the user if the song already exists
                st.warning("This song is already in the database.")

            # Clean up: close the cursor and connection
            cursor.close()
            connection.close()