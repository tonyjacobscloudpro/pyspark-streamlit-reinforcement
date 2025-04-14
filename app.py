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
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

current_index = st.session_state.current_index
if current_index >= len(questions):
    st.write("You have completed all the questions!")
    st.write(f"Questions Completed: {st.session_state.completed}")
    st.write(f"Correct Answers: {st.session_state.correct}")
    st.write(f"Wrong Answers: {st.session_state.wrong}")
    st.stop()

current_q = questions[current_index]

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

# Callback for the Submit Answer button
def submit_answer():
    current_q = questions[st.session_state.current_index]
    user_ans = st.session_state.user_answer
    feedback = simulated_ai_analysis(
        current_q.get("question", ""),
        current_q.get("expected_answer", ""),
        user_ans
    )
    st.session_state.last_feedback = feedback
    st.session_state.answer_submitted = True
    # Update counters based on answer evaluation
    try:
        expected = eval(current_q.get("question", ""))
        if str(expected) == user_ans.strip():
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
    except Exception:
        if current_q.get("expected_answer", "").strip() == user_ans.strip():
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
    st.session_state.completed += 1

# Callback for the Next Question button
def next_question():
    st.session_state.current_index += 1
    st.session_state.answer_submitted = False
    st.session_state.last_feedback = ""
    st.session_state.user_answer = ""  # Clear the answer field

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Display counters
    st.markdown(
        f"**Questions Completed:** {st.session_state.completed} &emsp; "
        f"**Correct:** {st.session_state.correct} &emsp; **Wrong:** {st.session_state.wrong}"
    )
    
    if not st.session_state.answer_submitted:
        # Answer input and submit button
        st.text_input("Enter your answer here:", key="user_answer")
        st.button("Submit Answer", on_click=submit_answer, key="submit_answer")
    else:
        st.markdown(st.session_state.last_feedback)
        st.button("Next Question", on_click=next_question, key="next_question")
