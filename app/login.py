import streamlit as st  # type: ignore
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

    # Create a container for buttons to control spacing
    button_container = st.container()

    with button_container:
        # Adjust the column widths to reduce spacing
        col1, col2 = st.columns([1, 7])  # First column narrower, second column wider
        error_message = None  # Initialize a variable to store error messages

        with col1:
            if st.button("Log In"):
                if not username or not password:
                    error_message = "Please fill out both fields."
                elif validate_user(username, password):
                    st.success("You have successfully logged in!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state.page = "bot"  # Navigate to bot page
                    st.rerun()  # Refresh to show bot page
                else:
                    error_message = "Invalid username or password. Please try again."

        with col2:
            if st.button("Back to Signup"):
                st.session_state.page = "signup"  # Navigate back to signup page
                st.session_state.logged_in = False  # Reset login status
                st.rerun()  # Refresh to show signup page

        # Display error message outside the column layout
        if error_message:
            st.error(error_message)

if __name__ == "__main__":
    main()
