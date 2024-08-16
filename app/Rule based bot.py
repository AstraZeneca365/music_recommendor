# Importing modules
import nltk
nltk.download('wordnet')
import re
from nltk.corpus import wordnet
# Building a list of Keywords
list_words=["Calm", "Energetic", "Sad", "Focused", "Motivational", "Love", "Heartbreak", "Chill", "Party", "Angry", "Happy"]
list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove any special characters from synonym strings
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)
#print (list_syn)
keywords={}
keywords_dict={}
keywords['CLM']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Calm']):
    keywords['CLM'].append('.*\\b'+synonym+'\\b.*')
keywords['ENR']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Energetic']):
    keywords['ENR'].append('.*\\b'+synonym+'\\b.*')
keywords['SAD']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Sad']):
    keywords['SAD'].append('.*\\b'+synonym+'\\b.*')
keywords['FCS']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Focused']):
    keywords['FCS'].append('.*\\b'+synonym+'\\b.*')
keywords['MTV']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Motivational']):
    keywords['MTV'].append('.*\\b'+synonym+'\\b.*')
keywords['LOV']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Love']):
    keywords['LOV'].append('.*\\b'+synonym+'\\b.*')
keywords['HBR']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Heartbreak']):
    keywords['HBR'].append('.*\\b'+synonym+'\\b.*')
keywords['CHL']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Chill']):
    keywords['CHL'].append('.*\\b'+synonym+'\\b.*')
keywords['PRT']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Party']):
    keywords['PRT'].append('.*\\b'+synonym+'\\b.*')
keywords['ANG']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Angry']):
    keywords['ANG'].append('.*\\b'+synonym+'\\b.*')
keywords['HPY']=[]
# Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
for synonym in list(list_syn['Happy']):
    keywords['HPY'].append('.*\\b'+synonym+'\\b.*')
for intent, keys in keywords.items():
    # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
    keywords_dict[intent]=re.compile('|'.join(keys))
# Building a dictionary of responses
responses={
    'Calm':'One of the best moods for music',
    'Energetic':'Ready for some action',
    'Sad':'One of the best moods for music',
    'Focused':'One of the best moods for music',
    'Motivational':'One of the best moods for music',
    'Love':'One of the best moods for music',
    'Heartbreak':'One of the best moods for music',
    'Chill':'One of the best moods for music',
    'Party':'One of the best moods for music',
    'Angry':'One of the best moods for music',
    'Happy':'One of the best moods for music',
    'fallback':'I dont quite understand. Could you repeat that?',
}
# While loop to run the chatbot indefinetely
while (True):  
    # Takes the user input and converts all characters to lowercase
    user_input = input().lower()
    # Defining the Chatbot's exit condition
    if user_input == 'quit': 
        print ("Thank you for visiting.")
        break    
    matched_intent = None 
    for intent,pattern in keywords_dict.items():
        # Using the regular expression search function to look for keywords in user input
        if re.search(pattern, user_input): 
            # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
            matched_intent=intent  
    # The fallback intent is selected by default
    key='fallback' 
    if matched_intent in responses:
        # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        key = matched_intent
    # The chatbot prints the response that matches the selected intent
    print (responses[key]) 
    