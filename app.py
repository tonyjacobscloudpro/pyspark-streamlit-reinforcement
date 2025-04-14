import streamlit as st
import json

st.title("PySpark-Streamlit-Reinforcement POC")
st.write("This is a simple proof of concept for a PySpark Tutorial web app with questions loaded from a JSON file and simulated AI-based answer analysis.")

# Function to load the question data from a JSON file
@st.cache_resource(show_spinner=False)
def load_question_data(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data from {file_path}: {e}")
        return None

# Define the path to your JSON file (ensure the file exists in the specified location)
data_path = "data/qa.json"
qa_data = load_question_data(data_path)

# Stop the app if there was an error loading the file
if not qa_data:
    st.stop()

# Extract the question text from the JSON data
question_text = qa_data.get("question", "No question provided.")

# Function to simulate AI analysis using Python's eval for arithmetic expressions.
def simulated_ai_analysis(question, user_answer):
    try:
        # Evaluate the question if it's a valid arithmetic expression
        expected_result = eval(question)
        # Compare with the user's input
        if str(expected_result) == user_answer.strip():
            return "Simulated AI Analysis: Your answer is correct!"
        else:
            return f"Simulated AI Analysis: The expected result is {expected_result} but you entered {user_answer}."
    except Exception:
        return "Simulated AI Analysis: Unable to evaluate the question automatically. Please check your input."

# --- Top Section: Question Panel ---
with st.container():
    st.header("Question Panel")
    st.write(question_text)

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Input widget for the user to enter their answer.
    user_answer = st.text_input("Enter your answer here:")
    # When the user clicks the submit button, perform the simulated AI analysis.
    if st.button("Submit Answer"):
        analysis = simulated_ai_analysis(question_text, user_answer)
        st.markdown(analysis)
