import streamlit as st
import json

st.title("PySpark-Streamlit-Reinforcement POC")
st.write(
    "This is a POC for a PySpark Tutorial web app with multiple questions loaded from a JSON file. "
    "A simulated AI analyzes your answers."
)

# -------------------------------
# Load Question Data from JSON
# -------------------------------
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

# -------------------------------
# Initialize Session State
# -------------------------------
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

# -------------------------------
# Top Section: Question Panel
# -------------------------------
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

# -------------------------------
# Helper Functions
# -------------------------------
def validate_pyspark_code(question_text, user_code):
    # For a DataFrame creation question, require spark.createDataFrame and df.show(
    if "DataFrame" in question_text:
        required_tokens = ["spark.createDataFrame", "df.show("]
        return all(token in user_code for token in required_tokens)
    # For a SparkSession question, require SparkSession.builder and getOrCreate
    elif "SparkSession" in question_text:
        required_tokens = ["SparkSession.builder", "getOrCreate"]
        return all(token in user_code for token in required_tokens)
    else:
        return user_code.strip() == current_q.get("expected_answer", "").strip()

def simulated_ai_analysis(question, expected_answer, user_answer, category):
    if category == "Arithmetic":
        try:
            expected_result = eval(question)
            if str(expected_result) == user_answer.strip():
                return f"Simulated AI: Your answer is correct! (Expected: {expected_result})"
            else:
                return f"Simulated AI: The expected answer is {expected_result}, but you entered {user_answer}."
        except Exception:
            return "Simulated AI: Could not evaluate the arithmetic expression."
    elif category == "PySpark":
        if validate_pyspark_code(question, user_answer):
            return "Simulated AI: Your PySpark code appears correct!"
        else:
            return "Simulated AI: Your PySpark code is incorrect. Please check your code."
    else:
        return "Simulated AI: Your answer is correct!" if expected_answer.strip() == user_answer.strip() else f"Simulated AI: Incorrect! Expected answer: {expected_answer}"

def submit_answer_callback():
    user_answer = st.session_state.user_answer
    category = current_q.get("category", "General")
    feedback = simulated_ai_analysis(
        current_q.get("question", ""),
        current_q.get("expected_answer", ""),
        user_answer,
        category
    )
    st.session_state.last_feedback = feedback
    st.session_state.answer_submitted = True

    if category == "Arithmetic":
        try:
            expected = eval(current_q.get("question", ""))
            if str(expected) == user_answer.strip():
                st.session_state.correct += 1
            else:
                st.session_state.wrong += 1
        except Exception:
            st.session_state.wrong += 1
    elif category == "PySpark":
        if validate_pyspark_code(current_q.get("question", ""), user_answer):
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
    else:
        if current_q.get("expected_answer", "").strip() == user_answer.strip():
            st.session_state.correct += 1
        else:
            st.session_state.wrong += 1
    st.session_state.completed += 1

def next_question_callback():
    st.session_state.current_index += 1
    st.session_state.answer_submitted = False
    st.session_state.last_feedback = ""
    st.session_state.user_answer = ""

# -------------------------------
# Bottom Section: Answer Panel
# -------------------------------
with st.container():
    st.header("Answer Panel")
    st.markdown(
        f"**Questions Completed:** {st.session_state.completed} &emsp; "
        f"**Correct:** {st.session_state.correct} &emsp; **Wrong:** {st.session_state.wrong}"
    )
    
    if not st.session_state.answer_submitted:
        # Use a simple text area (outside a form) and a button with an on_click callback.
        st.text_area("Enter your answer here:", key="user_answer", height=200)
        st.button("Submit Answer", on_click=submit_answer_callback, key="submit_answer")
    else:
        st.markdown(st.session_state.last_feedback)
        with st.expander("Show Expected Answer Code"):
            st.code(current_q.get("expected_answer", ""), language="python")
        st.button("Next Question", on_click=next_question_callback, key="next_question")
