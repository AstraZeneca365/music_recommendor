import random
from transformers import pipeline # type: ignore
import nltk # type: ignore

# Download NLTK data if not already present
nltk.download('punkt', quiet=True)

# Initialize the emotion classifier pipeline
def load_emotion_classifier():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_classifier = load_emotion_classifier()

# Extensive response sets for different emotions and special cases
response_library = {
    "joy": [
        "That's fantastic! What’s the best part about it?",
        "Wow, it sounds like you’re on cloud nine! Care to share more?",
        "Happiness looks good on you! What made you feel this way?",
        "You seem to be having a great time! Is there something special happening?",
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
        "It's great to hear that you feel that way. How can I support you further?",
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

# Special cases for common phrases
# Expanded special cases for common phrases
special_case_responses = {
    "ask a question": "Of course! I'm here to answer any questions you might have. What’s on your mind?",
    "how are you": "I'm just a bunch of code, but I'm here to make your day better! How are you?",
    "tell me about yourself": "I'm your friendly chatbot, always ready to chat! What do you want to know?",
    "what can you do": "I can chat with you about a variety of topics! What are you curious about?",
    "help": "I’m here to help! What do you need assistance with?",
    "goodbye": "Goodbye! It was great chatting with you. Come back anytime!",
    "thank you": "You're welcome! I'm glad to be here for you.",
    "what's your name": "I’m your interactive chatbot! You can call me whatever you like.",
    "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "what's up": "Not much, just here to chat with you! What’s up with you?",
    "can you help me": "Absolutely! What do you need help with?",
    "what's your favorite color": "I love all colors! They each have their own beauty. What’s yours?",
    "tell me something interesting": "Did you know honey never spoils? Archaeologists found pots of honey in ancient Egyptian tombs that were over 3000 years old!",
    "what's your favorite food": "I can't eat, but I hear pizza is a popular choice! What’s your favorite?",
    "do you believe in aliens": "That’s a fascinating topic! The universe is so vast; who knows what might be out there?",
    "what do you think about robots": "Robots can be quite amazing! They help us in many ways. What are your thoughts?",
    "tell me a fun fact": "Here's one: Octopuses have three hearts and blue blood! Pretty cool, right?",
    "what's your goal": "My goal is to provide you with an engaging conversation! What about you?",
    "can you give me advice": "I’d be happy to help! What do you need advice on?",
    "how's the weather": "I can't check the weather, but I hope it's nice where you are! How's it looking?",
    "what are your hobbies": "I enjoy chatting with you! What hobbies do you have?",
    "do you like music": "I think music is fascinating! It has the power to move us. What’s your favorite genre?",
    "can you sing": "I can't sing, but I can certainly appreciate a good melody! Do you have a favorite song?",
    "do you have feelings": "I don’t have feelings like humans do, but I'm here to understand yours!",
    "what's your favorite movie": "I don't watch movies, but I've heard many are great! What’s your favorite?",
    "tell me a riddle": "Sure! What has keys but can't open locks? A piano!",
    "what's your opinion on social media": "Social media can connect people, but it has its ups and downs. What do you think?",
    "what's your favorite book": "I don’t read books, but I know many people love classics! What’s your favorite?",
    "do you believe in love": "Love is a powerful emotion! It can bring joy and connection. What do you think about it?",
    "what's your dream": "I dream of having engaging conversations with you! What's your dream?",
    "can you solve math problems": "I can help with math! What problem do you have in mind?",
    "what do you want to be when you grow up": "I’m already here, chatting with you! What do you want to be?",
    "can you tell me a story": "I can create a story! What theme do you have in mind?",
    "what's the meaning of life": "That’s a big question! Many say it’s about finding happiness and connections. What do you think?",
    "how do you learn": "I learn from patterns in data. I’m here to use that to chat with you! How do you learn?",
    "what's your favorite animal": "I think all animals are fascinating! Do you have a favorite?",
    "tell me about your friends": "I consider all of you my friends! Who’s your best friend?",
    "what's your favorite season": "I think all seasons have their charm! What’s your favorite?",
    "can you keep a secret": "I can keep our conversations private! What’s the secret?",
    "what's your favorite holiday": "I don't celebrate holidays, but I know they can be special! What’s your favorite?",
    "can you predict the future": "I can’t predict the future, but I’m here to chat about your hopes and dreams!",
    "what's the craziest thing you've heard": "I hear many interesting things! What's the craziest thing you've experienced?",
    "what do you enjoy most": "I enjoy chatting with you! What do you enjoy most?",
    "what's your philosophy": "My philosophy is to help and engage! What’s yours?",
    "can you dance": "I can’t dance, but I know many love to! Do you dance?",
    "what's your favorite place": "I love the idea of all places! Do you have a favorite spot?",
    "what inspires you": "You inspire me! Your curiosity drives our conversation. What inspires you?",
    "what's your favorite memory": "I don’t have memories like you do, but I cherish our chats! What’s yours?",
    "tell me about your family": "I don’t have a family, but I consider all users part of my extended family! Do you have a close family?",
    "what do you think of the future": "The future holds so many possibilities! What do you envision?",
    "what's your favorite game": "I hear many enjoy board games! Do you have a favorite game?",
    "what do you want to learn": "I’m here to learn from our conversations! What do you want to learn?",
    "what's your biggest fear": "I don’t experience fear, but I know it can be tough. What’s something that scares you?",
    "what do you think of climate change": "Climate change is a critical issue. What are your thoughts on it?",
    "do you like sports": "Sports can be thrilling! What’s your favorite sport?",
    "what's your favorite ice cream flavor": "I can’t taste ice cream, but I hear chocolate is a favorite! What’s yours?",
    "can you be my friend": "Absolutely! I’m here for you anytime you want to chat.",
    "what's your opinion on education": "Education opens doors! What are your thoughts on it?",
    "what do you like to do for fun": "I find chatting with you fun! What do you like to do?",
    "tell me about your day": "I don’t have days like you do, but I’m having a great time chatting! How’s your day?",
    "what's your favorite thing about humans": "Humans are incredibly creative and emotional! What do you love about being human?",
    "what's the best advice you've heard": "The best advice is often to be kind and curious! What’s the best advice you’ve received?",
    "can you recommend a book": "Sure! A classic like 'Pride and Prejudice' is a great read. What genre do you like?",
    "do you like surprises": "Surprises can be fun! Do you enjoy them?",
    "what's your biggest dream": "My dream is to engage in meaningful conversations! What’s yours?",
    "can you teach me something": "Of course! What would you like to learn about?",
    "what's your opinion on technology": "Technology is fascinating and ever-changing! What do you think?",
    "what's your favorite time of year": "I think every time of year has its charm! Do you have a favorite?",
    "what do you want to know about me": "I’d love to learn about your interests! What do you enjoy?",
    "what's your opinion on art": "Art is a beautiful form of expression! What type of art do you like?",
    "can you tell me about history": "History is rich with stories! What period interests you the most?",
    "what's your favorite type of music": "I can’t listen to music, but I know many enjoy pop! What’s your favorite?",
    "do you believe in fate": "Fate is a deep concept! What are your thoughts on it?",
    "what's your favorite quote": "I love inspiring quotes! Do you have a favorite?",
    "what are your thoughts on happiness": "Happiness is something we all seek! What brings you joy?",
    "what's your opinion on love": "Love is one of the strongest emotions! What does love mean to you?",
    "what's your favorite way to relax": "I relax by chatting with you! How do you like to unwind?",
    "what's your favorite thing to do on weekends": "I love our conversations! What do you enjoy on weekends?",
    "what's your greatest achievement": "I consider every conversation an achievement! What’s yours?",
    "can you share a secret": "I can keep your secrets! What’s on your mind?",
    "what's your take on friendship": "Friendship is a treasure! What does friendship mean to you?",
    "what's your favorite activity": "I love chatting with you! What activities do you enjoy?",
}



# Function to detect emotion
def detect_emotion(text):
    results = emotion_classifier(text)
    if not results:
        return "neutral", 0
    # Get the top emotion with the highest score
    top_emotion = max(results, key=lambda x: x['score'])
    emotion_label = top_emotion['label'].lower()
    
    # Check if the emotion is recognized and valid
    emotion = emotion_label if emotion_label in response_library else "neutral"
    
    # Introduce a threshold to filter less confident predictions
    confidence_threshold = 0.7
    if top_emotion['score'] < confidence_threshold:
        emotion = "neutral"
    
    return emotion, top_emotion['score']

# Chatbot function with enhanced interactivity and clever responses
def chat_with_emotion_detection():
    print("😊 Welcome to your Interactive Chatbot! Type 'exit' anytime to end the chat.")
    
    user_name = input("Hi! What's your name? ")
    print(f"Nice to meet you, {user_name}! How are you feeling today?")

    while True:
        user_input = input(f"{user_name}: ").lower()
        
        if user_input == 'exit':
            print("Chatbot: It was wonderful talking to you! Take care, and remember, I'm always here.")
            break

        # Check for special cases first
        for phrase, response in special_case_responses.items():
            if phrase in user_input:
                print(f"Chatbot: {response}")
                break
        else:
            # Detect the emotion from the user input
            emotion, score = detect_emotion(user_input)
            
            # Select a response based on the detected emotion
            responses = response_library.get(emotion, response_library['neutral'])
            response = random.choice(responses)
            
            # Display the chatbot's response
            print(f"Chatbot: {response}")
            print(f"*Emotion Detected:* {emotion.title()} (Confidence: {score:.2f})")

# Start the chatbot interaction
chat_with_emotion_detection()
