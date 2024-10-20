import streamlit as st # type: ignore # type: ignore
from transformers import pipeline # type: ignore
import nltk # type: ignore # type: ignore
import time
import random
import mysql.connector # type: ignore

# download nltk data if not already present
nltk.download('punkt', quiet=True)

# set streamlit page configuration
st.set_page_config(
    page_title="Emotion-recognizing chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

# title of the app
st.title("🤖 Emotion-recognizing chatbot")

# initialize session state for conversation history and user name
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

# emotion to response mapping with multiple responses for variety
emotion_responses = {
    "joy": [
        "That's fantastic! What made you feel so happy?",
        "Wow, it sounds like you’re on cloud nine! Care to share more?",
        "Happiness looks good on you! What made you feel this way?",
        "You seem to be having a great time! Is something special happening?",
        "Your happiness is contagious! Tell me more!"
    ],
    "sadness": [
        "I'm here for you. Do you want to talk about what's on your mind?",
        "It’s okay to feel sad sometimes. What's been bothering you lately?",
        "I'm really sorry to hear that you're feeling this way. Is there anything I can do?",
        "Life has its ups and downs. Do you want to share what's bringing you down?",
        "I understand how tough it can be. Let's talk about it together."
    ],
    "anger": [
        "It's natural to feel angry. Want to vent a bit?",
        "I hear you, and your feelings are valid. What’s causing this frustration?",
        "It sounds like something really upset you. I'm here to listen if you want to share.",
        "Let it all out. Sometimes expressing it can be quite a relief.",
        "Your feelings matter, and I'm here to support you. What's been bothering you?"
    ],
    "fear": [
        "It’s okay to be afraid sometimes. Do you want to talk about it?",
        "We all have fears. Is there anything I can do to help you feel safer?",
        "Facing fear is never easy. I’m here if you need to share.",
        "I'm here for you. What's been making you feel this way?",
        "You’re not alone in this. Let's get through it together."
    ],
    "surprise": [
        "That’s unexpected! How did it make you feel?",
        "Wow! I didn’t see that coming either. What happened next?",
        "Surprises can be both good and bad. How do you feel about this one?",
        "That sounds interesting! Care to elaborate?",
        "Unexpected moments can be the best stories. Tell me more!"
    ],
    "disgust": [
        "I can understand why you'd feel that way. Want to share more?",
        "It must have been unpleasant. What happened?",
        "That sounds really tough. How did you handle it?",
        "Sometimes, things just leave a bad taste, don’t they?",
        "I'm here to listen if you need to get it off your chest."
    ],
    "trust": [
        "It's great to hear that you feel confident and trusting. How can I assist you today?",
        "I appreciate your trust! How can I assist you today?",
        "You can always count on me. Is there anything you want to share?",
        "I’m glad you feel confident. What would you like to talk about?",
        "Your trust means a lot. How can I be of help?"
    ],
    "anticipation": [
        "It sounds like you have something exciting coming up! Want to share?",
        "I can sense your excitement! What are you looking forward to?",
        "Anticipation is such a powerful feeling. Tell me more about it!",
        "It's always great to have something to look forward to. What’s the story?",
        "I love your enthusiasm! What’s got you so eager?"
    ],
    "neutral": [
        "I'm here to listen. Feel free to share whatever’s on your mind.",
        "What else is going on in your life?",
        "Anything interesting you'd like to talk about?",
        "I’m all ears! Tell me what’s up.",
        "You have my full attention. What would you like to discuss?",
        "That's a good question! What else would you like to know?",
        "Ask me anything! I'm here to chat with you.",
        "Let's keep the conversation going. What’s on your mind?",
        "Feel free to steer this chat in any direction you like!",
        "If you're unsure, I can suggest some topics too!"
    ]
}

default_response = "I'm here to listen. Can you tell me more?"

# mapping from model labels to desired emotions
model_to_emotion = {
    "admiration": "LOV",           # Mapped to Love
    "amusement": "HPY",            # Mapped to Happy
    "anger": "ANG",                # Mapped to Angry
    "annoyance": "ANG",            # Mapped to Angry
    "disgust": "ANG",              # Mapped to Angry
    "fear": "SAD",                 # Mapped to Sad (fearful state can lead to sadness)
    "joy": "HPY",                  # Mapped to Happy
    "love": "LOV",                 # Mapped to Love
    "optimism": "MTV",             # Mapped to Motivational (uplifting feeling)
    "pessimism": "SAD",            # Mapped to Sad
    "pride": "HPY",                # Mapped to Happy
    "realization": "FCS",          # Mapped to Focused
    "relief": "CLM",               # Mapped to Calm (relief brings calmness)
    "remorse": "SAD",              # Mapped to Sad
    "sadness": "SAD",              # Mapped to Sad
    "surprise": "PRT",             # Mapped to Party
    "confusion": "NTR",            # Mapped to Neutral (no matching predefined category)
    "curiosity": "FCS",            # Mapped to Focused
    "desire": "MTV",               # Mapped to Motivational
    "grief": "HBR",                # Mapped to Heartbreak
    "envy": "ANG",                 # Mapped to Angry
    "hate": "ANG",                 # Mapped to Angry
    "shame": "SAD",                # Mapped to Sad
    "disappointment": "SAD",       # Mapped to Sad
    "excitement": "ENR",           # Mapped to Energetic
    "gratitude": "LOV",            # Mapped to Love
    "contentment": "CLM",          # Mapped to Calm
    "betrayal": "HBR",             # Mapped to Heartbreak
    "nervousness": "SAD",          # Mapped to Sad (anxiety can lead to sadness)
    "reluctance": "SAD",           # Mapped to Sad (unwillingness can lead to disappointment)
    "doubt": "NTR",                # Mapped to Neutral (uncertainty doesn't fit other emotions)
    "yearning": "LOV",             # Mapped to Love (a deep longing for someone)
    "hope": "MTV",                 # Mapped to Motivational (a feeling of expectation)
    "indifference": "NTR",         # Mapped to Neutral (lack of interest)
    "contention": "ANG",           # Mapped to Angry (disagreement can cause anger)
    "euphoria": "HPY",             # Mapped to Happy (intense excitement or happiness)
    "frustration": "ANG",          # Mapped to Angry (a response to obstacles)
    "vulnerability": "SAD",        # Mapped to Sad (feeling exposed can lead to sadness)
    "fascination": "FCS",          # Mapped to Focused (a strong interest)
    "serenity": "CLM",             # Mapped to Calm (state of being calm)
    "distraction": "NTR",          # Mapped to Neutral (being unfocused)
    "nostalgia": "CHL",            # Mapped to Chill (sentimental yearning for the past)
    "apathy": "NTR",               # Mapped to Neutral (lack of feeling or interest)
    "satisfaction": "HPY",         # Mapped to Happy (contentment with a situation)
    "discontent": "SAD",           # Mapped to Sad (unhappiness with a situation)
    "rejuvenation": "ENR",         # Mapped to Energetic (feeling refreshed)
    "contemplation": "FCS",        # Mapped to Focused (deep thought about something)
    "disdain": "ANG",              # Mapped to Angry (feeling of contempt)
    "fury": "ANG",                 # Mapped to Angry (intense anger)
    "worry": "SAD",                # Mapped to Sad (anxiety leads to sadness)
    "reluctance": "SAD",           # Mapped to Sad (feeling unwilling)
    "betrayal": "HBR",             # Mapped to Heartbreak
    "embarrassment": "SAD",        # Mapped to Sad (feeling self-conscious)
    "exasperation": "ANG",         # Mapped to Angry (intense annoyance)
    "longing": "LOV",              # Mapped to Love (deep desire for someone)
    "hostility": "ANG",            # Mapped to Angry (unfriendly feelings)
    "relaxation": "CLM",           # Mapped to Calm (state of relaxation)
    "anticipation": "MTV",        # Mapped to Motivational (looking forward to something)
    "desperation": "SAD",          # Mapped to Sad (extreme need can lead to sadness)
    "disappointment": "SAD",       # Mapped to Sad (unmet expectations)
    "zeal": "ENR",                 # Mapped to Energetic (enthusiasm)
    "ambivalence": "NTR",          # Mapped to Neutral (mixed feelings)
    "overwhelm": "SAD",            # Mapped to Sad (feeling flooded by emotions)
    "intrigue": "FCS",             # Mapped to Curiosity (a strong interest)
    "tranquility": "CLM",          # Mapped to Calm (peaceful state)
    "disillusionment": "SAD",      # Mapped to Sad (loss of belief)
    "regret": "SAD",               # Mapped to Sad (feeling sorry for something)
    "ecstasy": "HPY",              # Mapped to Happy (intense joy)
    "compassion": "LOV",           # Mapped to Love (feeling for others)
    "fascination": "FCS",          # Mapped to Curiosity (a strong interest)
    "reluctance": "SAD",           # Mapped to Sad (feeling unwilling)
    "thrill": "HPY",               # Mapped to Happy (excitement)
    "elation": "HPY",              # Mapped to Happy (extreme joy)
    "apprehension": "SAD",         # Mapped to Sad (fear of what may happen)
    "ennui": "NTR",                # Mapped to Neutral (feeling of boredom)
    "delight": "HPY",              # Mapped to Happy (great pleasure)
    "melancholy": "SAD",           # Mapped to Sad (deep, persistent sadness)
    "anticipation": "MTV",         # Mapped to Motivational (excitement about the future)
    "dismay": "SAD",               # Mapped to Sad (disappointment mixed with shock)
    "ecstasy": "HPY",              # Mapped to Happy (overwhelming joy)
    "revulsion": "ANG",            # Mapped to Angry (strong disgust)
    "irritation": "ANG",           # Mapped to Angry (mild anger)
    "betrayal": "HBR",             # Mapped to Heartbreak (sense of treachery)
    "nostalgia": "CHL",            # Mapped to Chill (yearning for the past)
    "sorrow": "SAD",               # Mapped to Sad (deep sadness)
    "conflict": "ANG"              # Mapped to Angry (internal struggle)
}



@st.cache_resource
def load_emotion_classifier():
    """
    Load and cache the emotion classification pipeline.
    """
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_classifier()

def detect_emotion(text):
    """
    Detect the primary emotion in the given text.

    parameters:
        text (str): the input text from the user.

    returns:
        tuple: (primary_emotion, confidence_score)
    """
    results = emotion_classifier(text)
    if not results:
        return "neutral", 0.0

    # get the top emotion with the highest score
    top_emotion = max(results, key=lambda x: x['score'])
    emotion_label = top_emotion['label'].lower()

    # map the model's label to our predefined emotions
    emotion = model_to_emotion.get(emotion_label, "neutral")

    # confidence threshold to ensure reliable detection
    confidence_threshold = 0.7
    if top_emotion['score'] < confidence_threshold:
        emotion = "neutral"

    return emotion, top_emotion['score']

def get_response(emotion):
    """
    Get the chatbot response based on the detected emotion.

    parameters:
        emotion (str): the detected emotion.

    returns:
        str: the corresponding response message.
    """
    return random.choice(emotion_responses.get(emotion, [default_response]))

def fetch_records(emotion):
    """
    Fetch records from MySQL database based on the detected emotion.

    parameters:
        emotion (str): the detected emotion to filter songs.

    returns:
        list: fetched records as a list of song names.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="comp_project"
        )
        cursor = connection.cursor()
        # Query to fetch songs based on the detected emotion
        query = "SELECT name FROM songs WHERE emotion_id like '%"+ emotion + "%' ORDER BY RAND() LIMIT 5"
        cursor.execute(query)
        records = cursor.fetchall()
        if not records:  # If no records are found for the emotion
            return [f"No songs found for the emotion '{emotion}'."]
        return [record[0] for record in records] 
    except Exception as e:
        return [f"Error fetching records: {str(e)}"]
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_conversation():
    """
    Display the entire conversation history with transparent message boxes.
    """
    for msg in st.session_state.conversation:
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {msg['content']} </p>",
                    unsafe_allow_html=True
                )
        else:
            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {msg['content']} </p>",
                    unsafe_allow_html=True
                )

def main():
    """
    Main function to run the Streamlit chatbot app.
    """
    # Check if the user name is already set
    if "user_name" not in st.session_state:
        st.session_state.user_name = st.text_input("Please enter your name to start chatting:", key="name_input")
    
    # Display the greeting only once when the user name is entered
        if st.session_state.user_name and "greeted" not in st.session_state:
            st.session_state.greeted = True  # Set a flag to indicate the greeting has been displayed
            greeting_message = f"Hello {st.session_state.user_name}, how can I assist you today?"
            st.chat_message("assistant").markdown(greeting_message)
            st.session_state.conversation.append({"role": "assistant", "content": greeting_message})
            return  # Stop further execution until user input is provided

    # Display the conversation
    display_conversation()

    # Process user input
    if user_input := st.chat_input("Type your message here..."):
        # Save user's message to the session state
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {user_input} </p>", unsafe_allow_html=True)

        with st.spinner("Analyzing your message..."):
            emotion, score = detect_emotion(user_input)
            response = get_response(emotion)
            time.sleep(1)  # Simulate processing time

            records = fetch_records(emotion)

            # Prepare the response
            if records:
                records_display = "\n".join(f"- {record}" for record in records)  # Format for bullet points
                records_response = f"Here are some songs that match your mood:\n{records_display}"
            else:
                records_response = "No songs found for the detected emotion."

            # Full response
            full_response = f"{response}\n{records_response}"

            # Save assistant's response to the session state
            st.session_state.conversation.append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'>"
                    f"<strong>{response}</strong><br>"
                    f"<span style='color: white;'>Here are some songs that match your mood:</span><br>"  # Changed to white
                    f"<ul style='margin: 5px 0; padding-left: 20px;'>"
                    f"{''.join(f'<li>{record}</li>' for record in records)}"
                    f"</ul>"
                    "</p>",
                    unsafe_allow_html=True
                )


if __name__ == "__main__":
    main()

