import streamlit as st
import mysql.connector as mc

def form():

    st.title("Recommend some of your Favourites!!")

    with st.form(key='question_form'):

        name = st.text_input("Enter the name of the song",placeholder="e.g., I Ain't Worried")

        artist = st.text_input("Enter the name of the artist",placeholder="e.g., One Republic")

        emotion_id = st.text_input("""Describe the emotion of your song--- \n 
Available emotions - [Happy, Energetic, Love, Motivational, Focused, HeartBreak, Angry, Calm, Sad, Chill, Party]     
         """)

        genre = st.text_input("Enter the genre of your song", placeholder="e.g., Pop    ")

        spotify_link = st.text_input("Paste the spotify link of the song")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if not (name and artist and emotion_id and genre and spotify_link):
            st.error("Please fill all the fields.")



        else:
            db = {
                'host': 'localhost',
                'user': 'root',
                'password': '1234',
                'database': 'comp_project'
            }
            connection = mc.connect(**db)
            cursor = connection.cursor()

            query = f"""
                            create table if not exists rc_songs(
                            name varchar(50),
                            artist varchar(100),
                            emotion_id char(20),
                            genre varchar(20),
                            spotify_link varchar(80));
                        """
            cursor.execute(query)

            cursor.execute("select *  from rc_songs")
            l = cursor.fetchall()
            if (eval(f"(\"{name}\", \"{artist}\", \"{emotion_id}\", \"{genre}\", \"{spotify_link}\")")) not in l:
                    cursor.execute(f"insert into rc_songs values(\"{name}\", \"{artist}\", \"{emotion_id}\", \"{genre}\", \"{spotify_link}\")")
            connection.commit()

