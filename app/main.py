import streamlit as st
import signup
import login
import bot
from datetime import datetime
import base64


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background():
    # Get the current hour
    hour = datetime.now().hour

    # Determine which background to use based on the time of day
    if hour >= 5 and hour < 8:
        bg_image = "backgrounds/1.png"  # Early Morning
    elif hour >= 8 and hour < 12:
        bg_image = "backgrounds/2.png"  # Morning
    elif hour >= 12 and hour < 15:
        bg_image = "backgrounds/3.png"  # Afternoon
    elif hour >= 15 and hour < 17:
        bg_image = "backgrounds/4.png"  # Post Noon
    elif hour >= 17 and hour < 19:
        bg_image = "backgrounds/5.png"  # Almost Sunset
    elif hour >= 19 and hour < 21:
        bg_image = "backgrounds/6.png"  # After Sunset
    elif hour >= 21 or hour < 5:
        bg_image = "backgrounds/7.png"  # Night
    else:
        bg_image = "backgrounds/8.png"  # Early Morning (Moon still out)

    # Convert image to base64 and set as background
    with open(bg_image, 'rb') as f:
        bin_str = base64.b64encode(f.read()).decode()

    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;  /* Change text color if needed */
    }}
    
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)


def get_text_color():
    hour = datetime.now().hour
    if hour >= 5 and hour < 15:
        text_color = "#000000"  # Black during day
    else:
        text_color = "#FFFFFF"  # White during night
    return text_color


def main():
    # Set the background before rendering anything else
    set_background()

    if "page" not in st.session_state:
        st.session_state.page = "signup"

    text_color = get_text_color()  # Get the text color based on the time of day

    if st.session_state.page == "signup":
        signup.main()  # Call the signup function from signup.py
        
        st.markdown(f'<p style="color:{text_color}; font-size:25px;">Already have an account?</p>', unsafe_allow_html=True)

        if st.button("Go to Login Page"):
            st.session_state.page = "login"
            st.rerun()

    elif st.session_state.page == "login":
        login.main()  # Call the login function from login.py

    elif st.session_state.page == "bot":
        bot.main() 

if __name__ == "__main__":
    main()
