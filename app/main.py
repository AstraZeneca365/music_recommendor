import streamlit as st
import signup
from app import bot, login


def main():
    if "page" not in st.session_state:
        st.session_state.page = "signup"

    if st.session_state.page == "signup":
        st.title("Sign Up for the Song Recommender Chatbot")
        signup.main()  # Call the signup function from signup.py
        st.write("Already have an account?")
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    elif st.session_state.page == "login":
        st.title("Login to Your Account")
        login.main()  # Call the login function from login.py

    elif st.session_state.page == "bot":
        bot.main()  # Call the main bot function from bot.py
        if st.button("Log Out"):
            st.session_state.page = "login"
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()


if __name__ == "__main__":
    main()
