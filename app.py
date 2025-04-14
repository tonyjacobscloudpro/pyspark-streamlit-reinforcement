import streamlit as st

st.title("PySpark-Streamlit-Reinforcement POC")
st.write("This is a simple proof of concept for an PySpark Tutorial web app.")

# --- Top Section: Question Panel ---
with st.container():
    st.header("Question Panel")
    # Display the question
    st.write("4 + 4")

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Input widget for the user to enter the answer
    user_answer = st.text_input("Enter your answer here:")
    
    # Button to submit the answer and check correctness
    if st.button("Submit Answer"):
        if user_answer.strip() == "8":
            st.success("Correct! The answer is 8.")
        else:
            st.error("Incorrect answer. Please try again.")
