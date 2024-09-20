import streamlit as st




# Single correct bubble option
"""genre = st.radio(
     "What's your favorite movie genre",
     [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
     index=None,
 )

st.write("You selected:", genre)



genre = st.radio(
     "What's your favorite movie genre",
     [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
     captions=[
         "Laugh out loud.",
         "Get the popcorn.",
         "Never stop learning.",
     ],
 )
if genre == ":rainbow[Comedy]":
     st.write("You selected comedy.")
else:
     st.write("You didn't select comedy.")




import streamlit as st
import time

def f(x):
    with st.spinner(f"{x}."):
        for i in range(10):  # Adjust the range for how long you want the spinner to run
            # Dynamic text with dots
            dots = '.' * ((i % 4) + 1)  # Generates 1 to 4 dots
            st.spinner(f"{x}{dots}")  # Display the spinner with updated text
            time.sleep(0.5)  # Simulating some processing time
        # Final output after spinner completes
    st.success(f"{x} completed!")

# Call the function with your desired text
f("submitting")
st.toast('Your edited image was saved!', icon='😍')
st.text("Hello")
"""


import streamlit as st
import time

with st.empty():
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success("Done!")

st.spinner()