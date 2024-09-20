import streamlit as st
import os

def validate_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(" ")
            if stored_username == username and stored_password == password:
                return True
    return False

def main():
    st.title("Log In")

    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")

    if st.button("Log In"):
        if not username or not password:
            st.error("Please fill out both fields.")
        elif validate_user(username, password):
            st.success("You have successfully logged in!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state.page = "bot"  # Navigate to bot page
            st.rerun()  # Refresh to show bot page
        else:
            st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
