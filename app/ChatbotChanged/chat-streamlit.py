import streamlit as st # type: ignore
from transformers import pipeline # type: ignore
import nltk # type: ignore
import time
import random

# download nltk data if not already present
nltk.download('punkt', quiet=True)

# set streamlit page configuration
st.set_page_config(
    page_title="😊 emotion-recognizing chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto",
)

# title of the app
st.title("😊 emotion-recognizing chatbot 🤖")

# initialize session state for conversation history and user name
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

# emotion to response mapping with multiple responses for variety
emotion_responses = {
    "joy": [
        "that's fantastic! what made you feel so happy?",
        "wow, it sounds like you’re on cloud nine! care to share more?",
        "happiness looks good on you! what made you feel this way?",
        "you seem to be having a great time! is there something special happening?",
        "your happiness is contagious! tell me more!"
    ],
    "sadness": [
        "i'm here for you. do you want to talk about what's on your mind?",
        "it’s okay to feel sad sometimes. what's been bothering you lately?",
        "i'm really sorry to hear that you're feeling this way. is there anything i can do?",
        "life has its ups and downs. do you want to share what's bringing you down?",
        "i understand how tough it can be. let's talk about it together."
    ],
    "anger": [
        "it's natural to feel angry. want to vent a bit?",
        "i hear you, and your feelings are valid. what’s causing this frustration?",
        "it sounds like something really upset you. i'm here to listen if you want to share.",
        "let it all out. sometimes expressing it can be quite a relief.",
        "your feelings matter, and i'm here to support you. what's been bothering you?"
    ],
    "fear": [
        "it’s okay to be afraid sometimes. do you want to talk about it?",
        "we all have fears. is there anything i can do to help you feel safer?",
        "facing fear is never easy. i’m here if you need to share.",
        "i'm here for you. what's been making you feel this way?",
        "you’re not alone in this. let's get through it together."
    ],
    "surprise": [
        "that’s unexpected! how did it make you feel?",
        "wow! i didn’t see that coming either. what happened next?",
        "surprises can be both good and bad. how do you feel about this one?",
        "that sounds interesting! care to elaborate?",
        "unexpected moments can be the best stories. tell me more!"
    ],
    "disgust": [
        "i can understand why you'd feel that way. want to share more?",
        "it must have been unpleasant. what happened?",
        "that sounds really tough. how did you handle it?",
        "sometimes, things just leave a bad taste, don’t they?",
        "i'm here to listen if you need to get it off your chest."
    ],
    "trust": [
        "it's great to hear that you feel confident and trusting. how can I assist you today?",
        "i appreciate your trust! how can I assist you today?",
        "you can always count on me. is there anything you want to share?",
        "i’m glad you feel confident. what would you like to talk about?",
        "your trust means a lot. how can I be of help?"
    ],
    "anticipation": [
        "it sounds like you have something exciting coming up! want to share?",
        "i can sense your excitement! what are you looking forward to?",
        "anticipation is such a powerful feeling. tell me more about it!",
        "it's always great to have something to look forward to. what’s the story?",
        "i love your enthusiasm! what’s got you so eager?"
    ],
    "neutral": [
        "i'm here to listen. feel free to share whatever’s on your mind.",
        "what else is going on in your life?",
        "anything interesting you'd like to talk about?",
        "i’m all ears! tell me what’s up.",
        "you have my full attention. what would you like to discuss?",
        "that's a good question! what else would you like to know?",
        "ask me anything! i'm here to chat with you.",
        "let's keep the conversation going. what’s on your mind?",
        "feel free to steer this chat in any direction you like!",
        "if you're unsure, i can suggest some topics too!"
    ]
}

default_response = "i'm here to listen. can you tell me more?"

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
    load and cache the emotion classification pipeline.
    """
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_classifier()

def detect_emotion(text):
    """
    detect the primary emotion in the given text.

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
    get the chatbot response based on the detected emotion.

    parameters:
        emotion (str): the detected emotion.

    returns:
        str: the corresponding response message.
    """
    return random.choice(emotion_responses.get(emotion, [default_response]))

def display_conversation():
    """
    Display the entire conversation history with transparent message boxes.
    """
    for msg in st.session_state.conversation:
        if msg['role'] == 'user':
            # Display user message with transparent background
            with st.chat_message("user"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {msg['content']} </p>",
                    unsafe_allow_html=True
                )
        else:
            # Display assistant message with transparent background
            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px; margin: -10px 0 0 0;'> {msg['content']} </p>",
                    unsafe_allow_html=True
                )

def main():
    """
    main function to run the streamlit chatbot app.
    """
    # prompt user for their name if not already provided
    if not st.session_state.user_name:
        user_name = st.text_input("please enter your name to start the conversation:", key="name_input")
        if user_name:
            st.session_state.user_name = user_name.strip().title()
            st.session_state.conversation.append({"role": "assistant", "content": f"hello, {st.session_state.user_name}! how are you feeling today?"})
            display_conversation()
            st.rerun()  # rerun to display the conversation immediately
    else:
        # display conversation history
        display_conversation()

        # user input
        user_input = st.chat_input("type your message here...")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            display_conversation()

            # show spinner while processing
            with st.spinner("analyzing your message..."):
                emotion, score = detect_emotion(user_input)
                response = get_response(emotion)
                response_with_emotion = f"{response}"
                time.sleep(1)  # simulate processing time

            # append assistant response to conversation
            st.session_state.conversation.append({"role": "assistant", "content": response_with_emotion})
            display_conversation()
            st.rerun()  # rerun to display the updated conversation immediately


def main():
    """
    main function to run the streamlit chatbot app.
    """
    # prompt user for their name if not already provided
    if not st.session_state.user_name:
        user_name = st.text_input("please enter your name to start the conversation:", key="name_input")
        if user_name:
            st.session_state.user_name = user_name.strip().title()
            st.session_state.conversation.append({"role": "assistant", "content": f"hello, {st.session_state.user_name}! how are you feeling today?"})
            display_conversation()
            st.rerun()  # rerun to display the conversation immediately
    else:
        # display conversation history
        display_conversation()

        # user input
        user_input = st.chat_input("type your message here...")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            display_conversation()

            # show spinner while processing
            with st.spinner("analyzing your message..."):
                emotion, score = detect_emotion(user_input)
                response = get_response(emotion)
                response_with_emotion = f"{response}"
                time.sleep(1)  # simulate processing time

            # append assistant response to conversation
            st.session_state.conversation.append({"role": "assistant", "content": response_with_emotion})
            display_conversation()
            st.rerun()  # rerun to display the updated conversation immediately

if __name__ == "__main__":
    main()
