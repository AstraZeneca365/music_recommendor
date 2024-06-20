import streamlit as st
import mysql.connector


def connect_to_database(username, password): #inputs your username and password to connect to your mysql DB
    db = {
        'host': 'localhost',
        'user': username,
        'password': password,
        'database': 'comp_project'
    }
    try:
        connection = mysql.connector.connect(**db)
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

emotion_ids = ["CLM", "ENR", "SAD", "FCS", "MTV", "LOV", "HBR", "CHL", "PRT", "ANG", "HPY"]
emotions = ["Calm", "Energetic", "Sad", "Focused", "Motivational", "Love", "Heartbreak", "Chill", "Party",
            "Angry", "Happy"]

def fetch_songs_by_emotion(cursor, emotion_id): #fetch 5 random songs from the songs table based on what you enter
    try:
        query = f"""
            SELECT name, artist, genre, spotify_link 
            FROM songs 
            WHERE emotion_id like '%{emotion_id}%'
            ORDER BY RAND() 
            LIMIT 5;
        """
        cursor.execute(query)
        songs = cursor.fetchall()
        return songs
    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
        return None

def main():
    st.title("Song Recommender Chatbot")

    #displays the side menu for accepting mysql credentials
    st.sidebar.subheader("MySQL Database Credentials")
    username = st.sidebar.text_input("Enter MySQL Username", key="username")
    password = st.sidebar.text_input("Enter MySQL Password", type="password", key="password")

    if username and password:
        connection = connect_to_database(username, password)
        if not connection:
            st.error("Failed to connect to database.")
            return

        cursor = connection.cursor()

        user_mood = st.text_input("Hello! How are you feeling today? Enter your mood:")
        user_mood = user_mood.strip().capitalize()

        if user_mood:
            if user_mood in emotions:
                emotion_id = emotion_ids[emotions.index(user_mood)]

                songs = fetch_songs_by_emotion(cursor, emotion_id)

                if songs:
                    st.header(f"Here are some amazing songs for you:")
                    for song in songs:
                        st.markdown(f"**Name:** {song[0]}")
                        st.markdown(f"**Artist:** {song[1]}")
                        st.markdown(f"**Genre:** {song[2]}")
                        st.markdown(f"**Spotify Link:** [{song[0]}]({song[3]})")
                        st.markdown("---")
                else:
                    st.warning(f"No songs found for '{user_mood}'.")
            else:
                st.error("Sorry, I don't understand that mood. Please try again.")

        cursor.close()
        connection.close()
    else:
        st.sidebar.warning("Please enter MySQL username and password.")

if __name__ == "__main__":
    main()
