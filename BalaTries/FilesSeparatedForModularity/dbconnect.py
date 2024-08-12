import mysql.connector
import streamlit as st

def connect_to_database():
    # Database connection configuration
    db = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'comp_project'
    }
    try:
        connection = mysql.connector.connect(**db)
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None