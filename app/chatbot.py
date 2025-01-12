import streamlit as st  # type: ignore
from transformers import pipeline  # type: ignore
import nltk  # type: ignore
import time
import random
import mysql.connector  # type: ignore
from datetime import datetime

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# initialize session state for conversation history and user name
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

# emotion to response mapping with multiple responses for variety
emotion_responses = {
    
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
    "joy": "HPY",
    "happiness": "HPY",
    "sadness": "SAD",
    "anger": "ANG",
    "love": "LOV",
    "calm": "CLM",
    "neutral": "neutral",
    "excitement": "ENR",
    "focus": "FCS",
    "motivation": "MTV",
    "chill": "CHL",
    "party": "PRT",
    "heartbroken": "HBR"
}




@st.cache_resource
def load_emotion_classifier():
    """
    Load and cache the emotion classification pipeline.
    """
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_classifier()

keyword_overrides = {
    "calm"         : "CLM",
    "peace"        : "CLM",
    "relief"       : "CLM",
    "quiet"        : "CLM",
    "breathe"      : "CLM",
    "calm down"    : "CLM",
    "peaceful"     : "CLM",
    "still"        : "CLM",
    "relieved"     : "CLM",
    "tranquility"  : "CLM",
    "serene"       : "CLM",
    "ease"         : "CLM",

    "angry"        : "ANG",
    "hate"         : "ANG",
    "upset"        : "ANG",
    "mad"          : "ANG",
    "frustrated"   : "ANG",
    "annoyed"      : "ANG",
    "irritated"    : "ANG",
    "furious"      : "ANG",
    "angst"        : "ANG",
    "outburst"     : "ANG",
    "rage"         : "ANG",

    "sad"          : "SAD",
    "tired"        : "SAD",
    "scared"       : "SAD",
    "fear"         : "SAD",
    "sorry"        : "SAD",
    "bad"          : "SAD",
    "horrible"     : "SAD",
    "terrible"     : "SAD",
    "worried"      : "SAD",
    "nervous"      : "SAD",
    "unhappy"      : "SAD",
    "melancholy"   : "SAD",
    "blue"         : "SAD",
    "gloomy"       : "SAD",
    "down"         : "SAD",
    "tearful"      : "SAD",
    "distressed"   : "SAD",
    "weary"        : "SAD",
    "miserable"    : "SAD",
    "exhausted"    : "SAD",
    "anxious"      : "SAD",
    "tough day"    : "SAD",
    "bad day"      : "SAD",

    "love"         : "LOV",
    "grateful"     : "LOV",
    "thankful"     : "LOV",
    "friends"      : "LOV",
    "family"       : "LOV",
    "sweet"        : "LOV",
    "affection"    : "LOV",
    "adoration"    : "LOV",
    "fondness"     : "LOV",
    "cherished"    : "LOV",
    "beloved"      : "LOV",
    "fond"         : "LOV",
    "devotion"     : "LOV",
    "infatuation"  : "LOV",
    "caring"       : "LOV",
    "appreciate"   : "LOV",
    "thank you"    : "LOV",
    "bond"         : "LOV",
    "friend"       : "LOV",
    "bestie"       : "LOV",
    "home"         : "LOV",
    "bonded"       : "LOV",

    "heartbreak"   : "HBR",
    "lonely"       : "HBR",
    "broken"       : "HBR",
    "hurt"         : "HBR",
    "tears"        : "HBR",
    "devastated"   : "HBR",
    "crushed"      : "HBR",
    "despair"      : "HBR",
    "mourning"     : "HBR",
    "painful"      : "HBR",
    "grief"        : "HBR",
    "sorrowful"    : "HBR",
    "shattered"    : "HBR",
    "missing"      : "HBR",
    "betrayed"     : "HBR",
    "cheated"      : "HBR",
    "pain"         : "HBR",
    "breakup"      : "HBR",
    "alone"        : "HBR",

    "happy"        : "HPY",
    "laugh"        : "HPY",
    "smile"        : "HPY",
    "joy"          : "HPY",
    "cheerful"     : "HPY",
    "amazing"      : "HPY",
    "great"        : "HPY",
    "wonderful"    : "HPY",
    "best"         : "HPY",
    "happiness"    : "HPY",
    "laughter"     : "HPY",
    "funny"        : "HPY",
    "comedy"       : "HPY",
    "joke"         : "HPY",
    "smiley"       : "HPY",
    "great day"    : "HPY",
    "bliss"        : "HPY",

    "excited"      : "ENR",
    "awesome"      : "ENR",
    "thrilled"     : "ENR",
    "energized"    : "ENR",
    "buzzed"       : "ENR",
    "exciting"     : "ENR",
    "energy"       : "ENR",

    "party"        : "PRT",
    "fun"          : "PRT",
    "celebrate"    : "PRT",
    "dance"        : "PRT",
    "sing"         : "PRT",
    "surprised"    : "PRT",
    "happy birthday": "PRT",
    "congrats"     : "PRT",
    "wow"          : "PRT",
    "gathering"    : "PRT",
    "event"        : "PRT",
    "joyous"       : "PRT",
    "dancing"      : "PRT",
    "celebration"  : "PRT",
    "merrymaking"  : "PRT",

    "motivated"    : "MTV",
    "strong"       : "MTV",
    "brave"        : "MTV",
    "goals"        : "MTV",
    "dreams"       : "MTV",
    "hope"         : "MTV",
    "plans"        : "MTV",
    "good job"     : "MTV",
    "tough"        : "MTV",
    "inspired"     : "MTV",
    "motivation"   : "MTV",
    "determination": "MTV",
    "achievement"  : "MTV",
    "success"      : "MTV",
    "winning"      : "MTV",
    "victory"      : "MTV",
    "dream big"    : "MTV",
    "hopeful"      : "MTV",
    "goal"         : "MTV",
    "ambition"     : "MTV",
    "determined"   : "MTV",
    "win"          : "MTV",

    "chill"        : "CHL",
    "bored"        : "CHL",
    "relaxed"      : "CHL",
    "free"         : "CHL",
    "lazy"         : "CHL",
    "comfort"      : "CHL",
    "laid-back"    : "CHL",
    "content"      : "CHL",
    "boredom"      : "CHL",
    "relax"        : "CHL",
    "me time"      : "CHL",

     "okay"        : "neutral",
    "fine"        : "neutral",
    "alright"     : "neutral",
    "normal"      : "neutral",
    "average"     : "neutral",
    "indifferent" : "neutral",
    "balanced"    : "neutral",
    "ordinary"    : "neutral",
    "routine"     : "neutral",
    "unsure"      : "neutral",

}

def detect_emotion(text):
    # First, check for keyword-based overrides
    for keyword, emotion in keyword_overrides.items():
        if keyword in text.lower():
            return emotion, 1.0  # Return the override emotion with high confidence

    # Otherwise, use the model prediction
    results = emotion_classifier(text)
    print(results)
    if not results:
        return "neutral", 0.0

    # Find the emotion with the highest confidence
    top_emotion = max(results, key=lambda x: x['score'])
    model_emotion = top_emotion['label'].lower()
    confidence_score = top_emotion['score']

    # Map to desired emotions, default to "neutral" if no match is found
    custom_emotion = model_to_emotion.get(model_emotion, "neutral")
    
    return custom_emotion, confidence_score

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
    Display the entire conversation history without the extra background box.
    """
    text_color = get_text_color()
    for msg in st.session_state.conversation:
        if msg['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(
                    f"<p style='margin: -10px 0 0 0;'> {msg['content']} </p>", 
                    unsafe_allow_html=True
                )
        else:
            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='margin: -10px 0 0 0; color: {text_color};'> {msg['content']} </p>", 
                    unsafe_allow_html=True
                )
def get_text_color():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
       return "#000000" 
    elif hour >= 15 and hour < 5:
        return "#FFFFFF"
def get_text_color_for_desc():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
       return "#4C444A" 
    elif hour >= 15 and hour < 5:
        return "#A9A9A9"
    

def main():
    """
    Main function to run the Streamlit chatbot app.
    """
    text_color = get_text_color()
    text_color_for_desc = get_text_color_for_desc()
    if st.session_state.conversation:
        display_conversation()  # Show chat history if messages exist
    else:
        st.markdown(f"""
            <style>
            .input-label-for-chatbot-desc {{
                font-size: 18px; /* Change this value to adjust the font size */
                font-family: "Roboto", sans-serif; /* You can change the font family */
                color: {text_color_for_desc}; /* Dynamic color based on time */
            }}
            </style>
            """, unsafe_allow_html=True)
        # If no conversation yet, display prompt
        st.markdown("""
        <p class="input-label-for-chatbot-desc">        
        To get the conversation going, you can just type a message like:<br><br>
        - <i>“I'm feeling good today!”</i> (If that's how you feel)<br><br><br>
        Feel free to try out a few different kinds of questions. Just remember, this chatbot does its best, but sometimes it might say things that sound a little off. Thanks for your patience, and enjoy the chat!
        </p>
        """, unsafe_allow_html=True)

    
    if user_input := st.chat_input("Type your message here..."):
        # Save user's message to the session state
        st.session_state.conversation.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"<p style='margin: -10px 0 0 0;'> {user_input} </p>", unsafe_allow_html=True)

        with st.spinner("Analyzing your message..."):
            emotion,score = detect_emotion(user_input)
            print(emotion)
            response = get_response(emotion)
            time.sleep(1)  # simulate processing time
        

            assistant_message = response  # Default message without song recommendations

            # Only fetch records if the emotion is not neutral
            if emotion.lower() != "neutral":
                # Fetch records based on the detected emotion
                records = fetch_records(emotion)
                if records:
                    # Format the response with bullet points
                    songs_display = f"<ul style='color: {text_color};'>" + "".join(f"<li>{song}</li>" for song in records) + "</ul>"
                    recommendation_message = f"<span style='color: {text_color}; font-size: 18px;'><strong>Here are some song recommendations based on your mood:</strong></span>"                    
                    assistant_message += f"<br>{recommendation_message}<br>{songs_display}"


            # Display message (for both with/without song recommendations)
            with st.chat_message("assistant"):
                st.markdown(
                    f"<p style='margin: -10px 0 0 0; color: {text_color}'> {assistant_message} </p>",
                    unsafe_allow_html=True
                )
            # Save assistant's message to the session state
            st.session_state.conversation.append({"role": "assistant", "content": assistant_message, "color":text_color})
            st.rerun()

        st.session_state.chat_history.append(user_input)
        st.session_state.chat_history.append(assistant_message)
