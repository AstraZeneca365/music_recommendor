import streamlit as st  # type: ignore
import os
import bcrypt # type: ignore

# Function to save a new user with a hashed password
def save_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with open("users.txt", "a") as file:
        file.write(f"{username} {hashed_password}\n")

# Function to validate user credentials
def validate_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_hashed_password = line.strip().split(" ")
            if stored_username == username and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return True
    return False

# Function for the signup process
def signup():
    st.title("Sign Up")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    
    if st.button("Sign Up"):
        if not username or not password:
            st.error("Please fill out both fields.")
        else:
            save_user(username, password)
            st.success("You have successfully signed up! You can now log in.")

# Main function to run the Streamlit app
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    if st.session_state.page == "login":
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

    elif st.session_state.page == "signup":
        signup()

if __name__ == "__main__":
    main()
