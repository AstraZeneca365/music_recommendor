import streamlit as st

def display_intro():
    # Displays the introductory screen
    st.title("Home")
    st.write("This is Spots. I love to talk to people and recommend you some cool songs based on your mood.")

    if st.button("Let's chat!"):
        # Set session states for visibility
        st.session_state.intro_visible = False
        st.experimental_rerun()

    elif st.button("Recommend us some songs!"):
        st.session_state.intro_visible = False
        st.session_state.song_form_visible = True
        st.experimental_rerun()

def display_song_recommendation_header():
    # Displays the recommendation header
    st.markdown('<p class="title">🎵 Song Recommender Chatbot 🎵</p>', unsafe_allow_html=True)

def display_mood_input_form():
    # Input form for mood description and number of songs
    user_input = st.text_input("Describe your mood:", placeholder="e.g., I am feeling really joyful today.")
    num_songs = st.selectbox("How many songs would you like?", options=range(1, 11), index=4)
    submit_button = st.form_submit_button("Get Recommendations")
    return user_input, num_songs, submit_button

def display_song_details(songs, display_mood):
    # Displays details of recommended songs
    for song in songs:
        st.markdown(f"""
        <div class="song-details">
            <strong>Name:</strong> {song[0]}<br>
            <strong>Artist:</strong> {song[1]}<br>
            <strong>Genre:</strong> {song[2]}<br>
            <strong>Spotify Link:</strong> <a href="{song[3]}" target="_blank">{song[0]}</a>
        </div>
        """, unsafe_allow_html=True)