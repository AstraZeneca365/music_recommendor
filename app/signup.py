import streamlit as st
import os


def save_user_info(username, password):
    with open("../users.txt", "a") as file:
        file.write(f"{username},{password}\n")


def username_exists(username):
    if not os.path.exists("../users.txt"):
        return False
    with open("../users.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(",")
            if stored_username == username:
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
        else:
            save_user_info(username, password)
            st.success("You have successfully signed up! You can now log in.")
            st.session_state.page = "login"  # Automatically switch to login page


if __name__ == "__main__":
    main()
