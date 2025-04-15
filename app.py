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
if current_index >= len(questions):
    st.write("You have completed all the questions!")
    st.write(f"Questions Completed: {st.session_state.completed}")
    st.write(f"Correct Answers: {st.session_state.correct}")
    st.write(f"Wrong Answers: {st.session_state.wrong}")
    st.stop()

current_q = questions[current_index]

# --- Top Section: Question Panel (with colored background) ---
with st.container():
    st.markdown(
        f"""
        <div style="background-color: #e0f7fa; padding: 15px; border-radius: 5px;">
            <h3>Question Panel</h3>
            <p><strong>Category:</strong> {current_q.get('category', 'General')}</p>
            <p><strong>Question:</strong> {current_q.get('question', 'No question provided.')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            return f"Simulated AI: The expected answer was:\n{expected_answer}"

# --- Bottom Section: Answer Panel ---
with st.container():
    st.header("Answer Panel")
    # Display current counters
    st.markdown(
        f"**Questions Completed:** {st.session_state.completed} &emsp; "
        f"**Correct:** {st.session_state.correct} &emsp; **Wrong:** {st.session_state.wrong}"
    )
    
    if not st.session_state.answer_submitted:
        with st.form(key="answer_form", clear_on_submit=True):
            user_answer = st.text_area("Enter your answer here:", key="user_answer", height=200)
            submit_button = st.form_submit_button("Submit Answer")
            if submit_button:
                feedback = simulated_ai_analysis(
                    current_q.get("question", ""),
                    current_q.get("expected_answer", ""),
                    user_answer
                )
                st.session_state.last_feedback = feedback
                st.session_state.answer_submitted = True
                # Update counters based on answer evaluation
                try:
                    expected = eval(current_q.get("question", ""))
                    if str(expected) == user_answer.strip():
                        st.session_state.correct += 1
                    else:
                        st.session_state.wrong += 1
                except Exception:
                    if current_q.get("expected_answer", "").strip() == user_answer.strip():
                        st.session_state.correct += 1
                    else:
                        st.session_state.wrong += 1
                st.session_state.completed += 1
    else:
        st.markdown(st.session_state.last_feedback)
        # Display the expected answer code block for reference
        with st.expander("Show Expected Answer Code"):
            st.code(current_q.get("expected_answer", ""), language="python")
        if st.button("Next Question", key="next_question"):
            st.session_state.current_index += 1
            st.session_state.answer_submitted = False
            st.session_state.last_feedback = ""
