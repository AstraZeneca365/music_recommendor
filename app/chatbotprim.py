from transformers import pipeline
import nltk

# Download NLTK data if not already present
nltk.download('punkt', quiet=True)

# Initialize the emotion classifier pipeline
def load_emotion_classifier():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_classifier()

# Emotion to response mapping
emotion_responses = {
    "joy": "That's wonderful to hear! What made you feel so happy?",
    "sadness": "I'm really sorry you're feeling down. Do you want to talk about what's bothering you?",
    "anger": "I understand you're upset. Sometimes sharing can help. What's on your mind?",
    "fear": "It's completely okay to feel scared. How can I support you?",
    "surprise": "Wow, that sounds surprising! How did you handle it?",
    "disgust": "I'm sorry you're feeling this way. Would you like to discuss it further?",
    "trust": "It's great to hear that you feel confident and trusting. How can I assist you today?",
    "anticipation": "I see you're looking forward to something. What's exciting you right now?",
    "contempt": "It sounds like you're feeling a bit dismissive. Want to share more about that?",
    "shame": "I'm sorry you're feeling this way. Do you want to talk about what's causing these feelings?",
    "guilt": "Feeling guilty can be tough. Would you like to discuss it?",
    "love": "That's lovely! What or who brings you so much joy?",
    "neutral": "I'm here to listen. Feel free to share anything on your mind."
}

default_response = "I'm here to listen. Can you tell me more?"

# Mapping from model labels to desired emotions
model_to_emotion = {
    "admiration": "trust",
    "amusement": "joy",
    "anger": "anger",
    "annoyance": "anger",
    "disgust": "disgust",
    "fear": "fear",
    "joy": "joy",
    "love": "love",
    "optimism": "anticipation",
    "pessimism": "sadness",
    "pride": "joy",
    "realization": "surprise",
    "relief": "joy",
    "remorse": "guilt",
    "sadness": "sadness",
    "surprise": "surprise",
    "confusion": "surprise",
    "curiosity": "anticipation",
    "desire": "anticipation",
    "grief": "sadness",
    "envy": "contempt",
    "hate": "anger",
    "shame": "shame",
    "disappointment": "sadness",
    "excitement": "anticipation",
    "gratitude": "trust",
    "contentment": "joy",
    "betrayal": "anger"
}

# Function to detect emotion
def detect_emotion(text):
    results = emotion_classifier(text)
    if not results:
        return "neutral", 0
    # Get the top 3 emotions with highest scores
    top_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
    mapped_emotions = []
    for emotion in top_emotions:
        model_label = emotion['label'].lower()
        mapped = model_to_emotion.get(model_label, None)
        if mapped:
            mapped_emotions.append((mapped, emotion['score']))
    if not mapped_emotions:
        return "neutral", 0
    # Select the emotion with the highest cumulative score
    emotion_scores = {}
    for emo, score in mapped_emotions:
        if emo in emotion_scores:
            emotion_scores[emo] += score
        else:
            emotion_scores[emo] = score
    # Sort emotions by cumulative score
    sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
    primary_emotion, score = sorted_emotions[0]
    return primary_emotion, score

# Chatbot function without Streamlit
def chat_with_emotion_detection():
    print("😊 Emotion-Recognizing Chatbot")
    print("Type 'exit' to stop the conversation.")

    user_name = input("Hi! What's your name? ")
    print(f"Nice to meet you, {user_name}! How are you feeling today?")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Detect the emotion from the user input
        emotion, score = detect_emotion(user_input)

        # Respond based on the detected emotion
        response = emotion_responses.get(emotion, default_response)

        # Display the response
        print(f"Chatbot: {response}")
        print(f"*Emotion Detected:* {emotion.title()}, Confidence: {score:.2f}")

# Call the chatbot function to start a conversation
chat_with_emotion_detection()
