import streamlit as st

# Emotion ID and Synonym Mapping
emotion_ids = ["clm", "enr", "sad", "fcs", "mtv", "lov", "hbr", "chl", "prt", "ang", "hpy"]
emotions = ["calm", "energetic", "sad", "focused", "motivational", "love", "heartbreak", "chill", "party", "angry", "happy"]

# Synonym mapping for identifying emotions
emotion_synonyms = {
    # Add your synonym mappings here
}

def identify_emotion_from_sentence(sentence):
    # Identify the emotion from the user's input
    sentence = sentence.lower()
    for emotion, synonyms in emotion_synonyms.items():
        if any(synonym in sentence for synonym in synonyms):
            return emotion, synonyms[0]
    return None, None

def fetch_songs_by_emotion(cursor, emotion_id, limit=5):
    # Fetch songs based on the identified emotion
    try:
        query = "SELECT name, artist, genre, spotify_link FROM songs WHERE emotion_id = %s ORDER BY RAND() LIMIT %s;"
        cursor.execute(query, (emotion_id, limit))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"MySQL error: {err}")
        return None