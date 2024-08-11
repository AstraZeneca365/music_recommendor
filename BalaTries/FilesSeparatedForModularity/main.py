import streamlit as st
from db import connect_to_database
from ui import display_intro, display_song_recommendation_header, display_mood_input_form, display_song_details
from recommend import identify_emotion_from_sentence, fetch_songs_by_emotion

def main():
    # Session state management
    if 'intro_visible' not in st.session_state:
        st.session_state.intro_visible = True
    if 'song_form_visible' not in st.session_state:
        st.session_state.song_form_visible = False

    # Intro Display Logic
    if st.session_state.intro_visible and not st.session_state.song_form_visible:
        display_intro()

    elif st.session_state.song_form_visible:
        display_song_recommendation_header()

        connection = connect_to_database()
        if not connection:
            st.error("Failed to connect to the database.")
            return

        cursor = connection.cursor()

        with st.form(key='mood_form'):
            user_input, num_songs, submit_button = display_mood_input_form()

            if submit_button:
                if not user_input.strip():
                    st.warning("Please enter something to get recommendations.")
                else:
                    mood, synonym = identify_emotion_from_sentence(user_input)
                    if mood:
                        emotion_id = emotion_ids[emotions.index(mood)]
                        songs = fetch_songs_by_emotion(cursor, emotion_id, limit=num_songs)

                        if songs:
                            display_mood = synonym if synonym else mood
                            st.markdown(f'Here are some amazing songs for "{display_mood}":')
                            display_song_details(songs, display_mood)
                        else:
                            st.warning(f"No songs found for '{mood}'.")
                    else:
                        st.error("Sorry, I don't understand that mood. Please try again.")

        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()