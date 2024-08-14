import streamlit as st

# Emotion ID and Synonym Mapping
emotion_ids = ["clm", "enr", "sad", "fcs", "mtv", "lov", "hbr", "chl", "prt", "ang", "hpy"]
emotions = ["calm", "energetic", "sad", "focused", "motivational", "love", "heartbreak", "chill", "party", "angry", "happy"]

# Synonym mapping for identifying emotions
emotion_synonyms = {
    "Happy": ["happy", "good", "joyful", "cheerful", "content", "elated", "delighted", "glad", "pleased", "ecstatic", "jubilant", "upbeat"],
    "Sad": ["sad", "unhappy", "down", "gloomy", "depressed", "melancholy", "sorrowful", "heartbroken", "miserable", "dejected", "mournful"],
    "Love": ["love", "affection", "romance", "adore", "passion", "infatuation", "fondness", "devotion", "caring", "enamored", "tenderness"],
    "Energetic": ["energetic", "lively", "vibrant", "active", "dynamic", "enthusiastic", "spirited", "vigorous", "peppy", "bouncy", "animated"],
    "Motivational": ["motivational", "inspiring", "uplifting", "encouraging", "driven", "ambitious", "determined", "empowering", "stimulating", "motivating", "rousing"],
    "Heartbreak": ["heartbreak", "devastated", "broken", "sorrowful", "pained", "hurt", "anguished", "crushed", "grief-stricken", "despondent", "forlorn"],
    "Chill": ["chill", "relaxed", "laid-back", "mellow", "easygoing", "calm", "tranquil", "serene", "peaceful", "untroubled", "composed"],
    "Calm": ["calm", "serene", "peaceful", "tranquil", "composed", "still", "placid", "quiet", "relaxed", "soothing", "unruffled"],
    "Party": ["party", "celebration", "festivity", "gathering", "bash", "rave", "fiesta", "shindig", "soiree", "jamboree", "carnival"],
    "Focused": ["focused", "concentrated", "attentive", "alert", "determined", "intent", "engaged", "immersed", "fixated", "dedicated", "absorbed"],
    "Angry": ["angry", "furious", "mad", "irate", "enraged", "outraged", "livid", "annoyed", "fuming", "infuriated", "aggravated"]
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
