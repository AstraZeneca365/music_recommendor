import streamlit as st # type: ignore # type: ignore
from transformers import pipeline # type: ignore
import nltk # type: ignore # type: ignore
import time
import random
import mysql.connector # type: ignore

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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
    "HPY": [
        "That's wonderful! What brought you so much joy?",
        "Your happiness is infectious! Tell me more about it.",
        "I'm so glad to hear that! What made your day?",
        "Happiness looks good on you! Care to share what happened?",
        "You seem really cheerful! Is something special going on?",
        "What’s the secret behind your smile today?",
        "Your positivity is uplifting! What’s making you feel this way?",
        "I love your energy! What’s bringing you joy?",
        "Sounds like a great day! What’s been the highlight?",
        "Your happiness is a ray of sunshine! What’s the story?"
    ],
    "SAD": [
        "I'm here for you. Do you want to talk about what's bothering you?",
        "It’s okay to feel sad sometimes. What’s on your mind?",
        "I’m really sorry to hear that you're feeling down. How can I help?",
        "It's normal to have tough days. Want to share what's making you feel this way?",
        "Sadness is part of being human. I'm here to listen if you need.",
        "I'm really sorry you're feeling this way. Is there anything specific troubling you?",
        "Sometimes it helps to talk about it. What’s been weighing on your heart?",
        "It's okay to feel this way. How can I support you through this?",
        "You’re not alone in this. Want to share your thoughts?",
        "Let’s talk about what’s bringing you down, if you’re comfortable."
    ],
    "MTV": [
        "What’s inspiring you to push forward today?",
        "Motivation can be so powerful! What drives you?",
        "I can sense your determination! What are you working towards?",
        "What’s fueling your ambition right now?",
        "I love your enthusiasm! What are you excited to accomplish?",
        "What keeps you motivated on tough days?",
        "Your drive is inspiring! What’s your current goal?",
        "What motivates you to keep moving forward?",
        "How do you stay focused on your goals?",
        "I admire your motivation! What’s the next step for you?"
    ],
    "CLM": [
        "It’s great to hear you’re feeling calm. What’s bringing you peace?",
        "Calmness is such a beautiful state. How did you achieve it?",
        "What do you do to maintain this sense of calm?",
        "Calmness can be hard to find sometimes. What helps you relax?",
        "Your tranquility is inspiring! What’s your secret?",
        "What’s been contributing to your sense of calm lately?",
        "Finding calm is essential. What practices help you?",
        "How do you maintain your peace of mind?",
        "What does a perfect calm day look like for you?",
        "I appreciate your calm demeanor! What keeps you grounded?"
    ],
    "ENR": [
        "Your energy is contagious! What’s fueling your enthusiasm?",
        "I can feel your vibrancy! What’s exciting you today?",
        "What’s making you feel so alive and energized?",
        "Your passion is inspiring! What’s the source of your energy?",
        "How do you keep your energy levels high?",
        "What activities bring out your energetic side?",
        "Your excitement is uplifting! What’s got you buzzing?",
        "What are you celebrating that’s giving you so much energy?",
        "What keeps you motivated and energized throughout the day?",
        "Your lively spirit is refreshing! What are you up to?"
    ],
    "FCS": [
        "You seem really focused! What’s capturing your attention?",
        "How do you maintain your concentration?",
        "What are you currently focused on that excites you?",
        "I admire your dedication! What’s your goal?",
        "How do you tune out distractions?",
        "What helps you stay on track?",
        "You seem really committed! What’s driving your focus?",
        "What’s the key to your concentration right now?",
        "How do you keep your mind sharp and focused?",
        "What’s your strategy for staying productive?"
    ],
    "LOV": [
        "Love is such a beautiful emotion! What’s inspiring it?",
        "What brings you joy and love in your life?",
        "Your love for life is refreshing! What fuels it?",
        "How do you express love in your daily life?",
        "What moments make you feel loved and cherished?",
        "How do you cultivate love in your relationships?",
        "What’s your favorite way to show love to others?",
        "What does love mean to you?",
        "What are the little things that make you feel loved?",
        "Your love is inspiring! How do you share it?"
    ],
    "HBR": [
        "I'm really sorry to hear you're feeling heartbroken. Want to talk about it?",
        "Breakups can be really tough. How are you coping?",
        "It’s okay to grieve the loss of a relationship. What are you feeling?",
        "How can I support you during this tough time?",
        "Heartbreak can be so painful. Want to share your story?",
        "It’s okay to take your time healing. How can I help?",
        "What’s been the hardest part of this experience for you?",
        "I’m here to listen if you want to share your feelings.",
        "How do you find comfort during times like this?",
        "Healing takes time. What helps you feel better?"
    ],
    "CHL": [
        "Chill vibes are the best! What’s helping you relax?",
        "How do you maintain your chill state of mind?",
        "What’s your go-to for a relaxing day?",
        "I love your laid-back attitude! What keeps you calm?",
        "What activities help you unwind?",
        "Your chill demeanor is refreshing! How do you achieve it?",
        "How do you balance relaxation with daily life?",
        "What’s your favorite way to spend a chill day?",
        "What brings you peace in a busy world?",
        "Your chill vibes are contagious! What’s your secret?"
    ],
    "PRT": [
        "Party vibes! What’s the occasion?",
        "I love a good celebration! What are you celebrating?",
        "What’s your favorite way to party?",
        "What events make you feel like partying?",
        "Your enthusiasm for fun is contagious! What’s the plan?",
        "How do you like to let loose and have fun?",
        "What’s your favorite memory from a party?",
        "What’s the best party you’ve ever attended?",
        "What’s your party playlist like?",
        "Your party spirit is inspiring! What’s next on your agenda?"
    ],
    "ANG": [
        "I understand that anger is a natural feeling. What’s causing this frustration?",
        "It’s okay to feel angry sometimes. Want to talk about it?",
        "How do you handle feelings of anger?",
        "What’s been upsetting you lately?",
        "Your feelings are valid. What’s on your mind?",
        "It’s important to express anger healthily. Want to vent?",
        "What triggers your anger, and how do you cope?",
        "How can I support you while you’re feeling this way?",
        "What’s a healthy outlet for your anger?",
        "Your anger is understandable. How can we work through it?"
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
    "confusion": "neutral",            # Mapped to Neutral (no matching predefined category)
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
    "doubt": "neutral",                # Mapped to Neutral (uncertainty doesn't fit other emotions)
    "yearning": "LOV",             # Mapped to Love (a deep longing for someone)
    "hope": "MTV",                 # Mapped to Motivational (a feeling of expectation)
    "indifference": "neutral",         # Mapped to Neutral (lack of interest)
    "contention": "ANG",           # Mapped to Angry (disagreement can cause anger)
    "euphoria": "HPY",             # Mapped to Happy (intense excitement or happiness)
    "frustration": "ANG",          # Mapped to Angry (a response to obstacles)
    "vulnerability": "SAD",        # Mapped to Sad (feeling exposed can lead to sadness)
    "fascination": "FCS",          # Mapped to Focused (a strong interest)
    "serenity": "CLM",             # Mapped to Calm (state of being calm)
    "distraction": "neutral",          # Mapped to Neutral (being unfocused)
    "nostalgia": "CHL",            # Mapped to Chill (sentimental yearning for the past)
    "apathy": "neutral",               # Mapped to Neutral (lack of feeling or interest)
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
    "anticipation": "MTV",         # Mapped to Motivational (looking forward to something)
    "desperation": "SAD",          # Mapped to Sad (extreme need can lead to sadness)
    "disappointment": "SAD",       # Mapped to Sad (unmet expectations)
    "zeal": "ENR",                 # Mapped to Energetic (enthusiasm)
    "ambivalence": "neutral",          # Mapped to Neutral (mixed feelings)
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
    "ennui": "neutral",                # Mapped to Neutral (feeling of boredom)
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
        query = "SELECT name FROM songs WHERE emotion_id like '%"+ emotion + "%' LIMIT 5"
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
    display_conversation()

    if user_input := st.chat_input("Type your message here..."):
        # Save user's message to the session state
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {user_input} </p>", unsafe_allow_html=True)

        with st.spinner("Analyzing your message..."):
            emotion, score = detect_emotion(user_input)
            response = get_response(emotion)
            time.sleep(1)  # simulate processing time

            # Fetch records based on the detected emotion
            records = fetch_records(emotion)
            if records:
                # Format the response with bullet points
                songs_display = "\n".join(f"- {song}" for song in records)  # Create a bullet point list
                assistant_message = f"{response}\n\nHere are some song recommendations based on your mood:\n\n{songs_display}"
            else:
                assistant_message = f"{response}\n\n{records[0]}"  # Display error message if no records found

            # Save assistant's message to the session state
            st.session_state.conversation.append({"role": "assistant", "content": assistant_message})

            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'>"
                    f"<strong>{response}</strong><br>"
                    f"<span style='color: white;'>Here are some songs that match your mood:</span><br>"
                    f"<ul style='margin: 5px 0; padding-left: 20px;'>"
                    f"{''.join(f'<li>{record}</li>' for record in records)}"
                    f"</ul>"
                    "</p>",
                    unsafe_allow_html=True
                )
        st.session_state.chat_history.append(user_input)
        st.session_state.chat_history.append(assistant_message)

if __name__ == "__main__":
    main()
