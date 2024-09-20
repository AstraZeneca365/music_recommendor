import streamlit as st
import os
import re

def save_user_info(username, password):
    with open("users.txt", "a") as file:
        file.write(f"{username} {password}\n")


def username_exists(username):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(" ")
            if stored_username == username:
                return True
    return False


def is_valid_password(password):
    # Check for 8 chars minimum, 1 uppercase, 1 lowercase, 1 digit, 1 special character
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[\W_]', password)):  # \W matches any non-word character, _ is included for underscore
        return True
    return False


def main():
    st.title("Sign Up")

    username = st.text_input("Enter a username")
    password = st.text_input("Enter a password", type="password")

    if st.button("Sign Up"):
        if not username or not password:
            st.error("Please fill out all fields.")
        elif username_exists(username):
            st.error("Username already exists. Please choose a different one.")
        elif not is_valid_password(password):
            st.error("Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        else:
            save_user_info(username, password)
            st.success("You have successfully signed up! You can now log in.")
            st.session_state.page = "login"  # Automatically switch to login page


if __name__ == "__main__":
    main()
