import streamlit as st
import json

st.title("PySpark-Streamlit-Reinforcement POC")
st.write(
    "This is a simple proof of concept for a PySpark Tutorial web app with multiple questions loaded from a JSON file. "
    "A simulated AI analyzes your answers."
)

# Function to load questions data from a JSON file
@st.cache_resource(show_spinner=False)
def load_question_data(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data from {file_path}: {e}")
        return None

# Define the path to your JSON file (ensure the file exists at the specified location)
data_path = "data/qa.json"
qa_data = load_question_data(data_path)

if not qa_data or "questions" not in qa_data:
    st.error("No questions available in the provided JSON file.")
    st.stop()

# Retrieve the list of questions
questions = qa_data["questions"]

# Initialize session state for quiz progress if not already set
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "completed" not in st.session_state:
    st.session_state.completed = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

# Get the current question using the session state's current_index
current_index = st.session_state.current_index

# Check if there are still questions available
if current_index < len(questions):
    current_q = questions[current_index]
else:
    st.write("You have completed all the questions!")
    st.write(f"Questions Completed: {st.session_state.completed}")
    st.write(f"Correct Answers: {st.session_state.correct}")
    st.write(f"Wrong Answers: {st.session_state.wrong}")
    st.stop()

# --- Top Section: Question Panel ---
with st.container():
    st.header("Question Panel")
    st.write(f"**Category:** {current_q.get('category', 'General')}")
    st.write(f"**Question:** {current_q.get('question', 'No question provided.')}")

# Function to simulate AI analysis using Python's eval if possible
def simulated_ai_analysis(question, expected_answer, user_answer):
    try:
        # Attempt to evaluate arithmetic expressions
        expected_result = eval(question)
        if str(expected_result) == user_answer.strip():
            return f"Simulated AI Analysis: Your answer is correct! (Expected: {expected_result})"
        else:
            return f"Simulated AI Analysis: The expected answer is {expected_result}, but you entered {user_answer}."
    except Exception:
        # Fallback for non-arithmetic questions
        if expected_answer.strip() == user_answer.strip():
            return "Simulated AI Analysis: Your answer is correct!"
        else:
            return f"Simulated AI Analysis: The expected answer was '{expected_answer}', but you entered '{user_answer}'."

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    
    # Display counters
    st.markdown(
        f"**Questions Completed:** {st.session_state.completed} &emsp; **Correct:** {st.session_state.correct} &emsp; **Wrong:** {st.session_state.wrong}"
    )
    
    # Answer input and submission area
    if not st.session_state.answer_submitted:
        user_answer = st.text_input("Enter your answer here:", key="user_answer")
        if st.button("Submit Answer"):
            feedback = simulated_ai_analysis(
                current_q.get("question", ""), current_q.get("expected_answer", ""), user_answer
            )
            st.session_state.last_feedback = feedback
            st.session_state.answer_submitted = True

            # Update counters based on result using eval for arithmetic questions
            try:
                expected = eval(current_q.get("question", ""))
                if str(expected) == user_answer.strip():
                    st.session_state.correct += 1
                else:
                    st.session_state.wrong += 1
            except Exception:
                # Fallback for non-arithmetic questions
                if current_q.get("expected_answer", "").strip() == user_answer.strip():
                    st.session_state.correct += 1
                else:
                    st.session_state.wrong += 1

            st.session_state.completed += 1
    else:
        st.markdown(st.session_state.last_feedback)
        if st.button("Next Question"):
            st.session_state.current_index += 1
            st.session_state.answer_submitted = False
            st.session_state.last_feedback = ""
            
            # No need for experimental_rerun; the widget interaction already triggers a re-run.
