import streamlit as st
import json

st.title("PySpark-Streamlit-Reinforcement POC")
st.write(
    "This is a POC for a PySpark Tutorial web app with multiple questions loaded from a JSON file. "
    "A simulated AI analyzes your answers."
)

# Function to load questions data from a JSON file
@st.cache_resource(show_spinner=False)
def load_question_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

data_path = "data/qa.json"
qa_data = load_question_data(data_path)

if not qa_data or "questions" not in qa_data:
    st.error("No questions available in the provided JSON file.")
    st.stop()

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

current_index = st.session_state.current_index
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

# Simulated AI analysis function
def simulated_ai_analysis(question, expected_answer, user_answer):
    try:
        # Try to evaluate arithmetic expressions
        expected_result = eval(question)
        if str(expected_result) == user_answer.strip():
            return f"Simulated AI: Your answer is correct! (Expected: {expected_result})"
        else:
            return f"Simulated AI: The expected answer is {expected_result}, but you entered {user_answer}."
    except Exception:
        # Fallback: simple string comparison for non-arithmetic questions
        if expected_answer.strip() == user_answer.strip():
            return "Simulated AI: Your answer is correct!"
        else:
            return f"Simulated AI: The expected answer was '{expected_answer}', but you entered '{user_answer}'."

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Display current counters
    st.markdown(
        f"**Questions Completed:** {st.session_state.completed} &emsp; "
        f"**Correct:** {st.session_state.correct} &emsp; **Wrong:** {st.session_state.wrong}"
    )

    # If answer not yet submitted, display a form to gather the answer
    if not st.session_state.answer_submitted:
        with st.form(key="answer_form", clear_on_submit=True):
            user_answer = st.text_input("Enter your answer here:")
            submit_button = st.form_submit_button("Submit Answer")
            if submit_button_
