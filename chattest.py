import streamlit as st
from transformers import pipeline
import nltk
import time
import random
import mysql.connector

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
    "admiration": "trust",
    "amusement": "joy",
    "anger": "anger",
    "annoyance": "anger",
    "disgust": "disgust",
    "fear": "fear",
    "joy": "joy",
    "love": "trust",
    "optimism": "anticipation",
    "pessimism": "sadness",
    "pride": "joy",
    "realization": "surprise",
    "relief": "joy",
    "remorse": "sadness",
    "sadness": "sadness",
    "surprise": "surprise",
    "confusion": "neutral",
    "curiosity": "anticipation",
    "desire": "anticipation",
    "grief": "sadness",
    "envy": "disgust",
    "hate": "anger",
    "shame": "sadness",
    "disappointment": "sadness",
    "excitement": "anticipation",
    "gratitude": "trust",
    "contentment": "joy",
    "betrayal": "anger"
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

def fetch_records():
    """
    Fetch records from MySQL database.

    returns:
        list: fetched records as a list of strings.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="comp_project"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM songs LIMIT 5") 
        records = cursor.fetchall()
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
    if not st.session_state.user_name:
        user_name = st.text_input("Please enter your name to start the conversation:", key="name_input")
        if user_name:
            st.session_state.user_name = user_name.strip().title()
            st.session_state.conversation.append({"role": "assistant", "content": f"Hello, {st.session_state.user_name}! How are you feeling today?"})
            display_conversation()
            st.rerun()  # rerun to display the conversation immediately
    else:
        display_conversation()

        user_input = st.chat_input("Type your message here...")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            display_conversation()

            with st.spinner("Analyzing your message..."):
                emotion, score = detect_emotion(user_input)
                response = get_response(emotion)
                time.sleep(1)  # simulate processing time

                # Fetch records and append to response
                records = fetch_records()
                records_response = "Here are some records from the database:\n" + "\n".join(records)
                full_response = f"{response}\n{records_response}"

            st.session_state.conversation.append({"role": "assistant", "content": full_response})
            display_conversation()
            st.rerun()  # rerun to display the updated conversation immediately

if __name__ == "__main__":
    main()
