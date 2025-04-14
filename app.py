import streamlit as st
import json

st.title("PySpark-Streamlit-Reinforcement POC")
st.write("This is a simple proof of concept for an PySpark Tutorial web app with content loaded from a JSON file.")

# Function to load the Q&A data from a JSON file
@st.cache_resource(show_spinner=False)
def load_qa_data(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data from {file_path}: {e}")
        return None

# Define the file path (adjust the path as necessary)
data_path = "data/qa.json"
qa_data = load_qa_data(data_path)

# Stop the app if data could not be loaded
if not qa_data:
    st.stop()

# Get the question text and expected answer from the JSON data
question_text = qa_data.get("question", "Question not provided.")
expected_answer = qa_data.get("expected_answer", "")

# --- Top Section: Question Panel ---
with st.container():
    st.header("Question Panel")
    st.write(question_text)

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Input widget for the user to enter the answer
    user_answer = st.text_input("Enter your answer here:")
    # Button to submit the answer and check correctness
    if st.button("Submit Answer"):
        if user_answer.strip() == expected_answer:
            st.success("Correct! Well done.")
        else:
            st.error("Incorrect answer. Please try again.")
