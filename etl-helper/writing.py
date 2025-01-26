import time
from vertexai.generative_models import GenerativeModel
import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai.preview.language_models import TextGenerationModel
credentials = service_account.Credentials.from_service_account_file("D:/BU/Fall 24/Web Mining/Term Project/ept-helper-442122-e21a06ec1cd4.json")

aiplatform.init(credentials=credentials, project="ept-helper-442122", location="us-central1")   # Initialize the Vertex AI client

#Function to evaluate the writing passage
def evaluate_writing_passage(passage):

    prompt = f"""
    You are an expert evaluator for TOEFL writing tasks. Evaluate the following response based on the following criteria:
    1. Task Achievement: Does the response effectively answer the question? Is the argument convincing and well-supported?
    2. Coherence and Cohesion: Is the structure logical and easy to follow? Are transitions between ideas smooth?
    3. Lexical Resource: How diverse and appropriate is the vocabulary? Are there any repetitions or inappropriate word choices?
    4. Grammatical Range and Accuracy: Are there grammatical errors? Is there a variety of sentence structures?
    5. Overall Impression: Provide an overall score from 0 to 5. Let your grading be according to TOEFL/IELTS standards

    Response:
    {passage}

    Provide feedback in the following format:
    - Task Achievement: [Feedback]
    - Coherence and Cohesion: [Feedback]
    - Lexical Resource: [Feedback]
    - Grammatical Range and Accuracy: [Feedback]
    - Overall Impression: [Feedback]
    - Suggested Score: [Score out of 5]
    """

    model = GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


def handle_writing_section():
    st.header("Writing Section")

    # Instructions for the writing section
    st.markdown("""
        ### Instructions:
        - You will be given two writing prompts. You have 20 minutes to answer each one.
        - After 5 seconds, a timer will start and you will have 20 minutes to complete your response for each task.
        - You can submit your responses at any time before the timer ends. Once you submit, your answers will be reviewed and evaluated.
    """)

    # placeholder for the timer
    timer_placeholder = st.empty()

    #display writing tasks
    st.subheader("Task 1: Write about the following topic:")
    prompt1 = "Do you agree or disagree with the following statement? It is better to live in a small town than a large city."
    st.markdown(f"**{prompt1}**")

    response1 = st.text_area("Your response for Task 1:", key="task_1_response")

    st.subheader("Task 2: Write about the following topic:")
    prompt2 = "Do you think the benefits of online learning outweigh the drawbacks?"
    st.markdown(f"**{prompt2}**")

    response2 = st.text_area("Your response for Task 2:", key="task_2_response")

    # Countdown timer (5 seconds before the timer starts)
    st.markdown("### Timer will start in 5 seconds... Please be ready!")
    countdown_time = 5
    for t in range(countdown_time, 0, -1):
        st.write(f"Starting timer in {t} seconds...")
        time.sleep(1)

    # Timer starts
    st.write("Timer started! You have 20 minutes to complete both tasks.")
    total_time = 20 * 60  # 20 minutes in seconds
    start_time = time.time()
    end_time = start_time + total_time

    # Submit button outside the loop, accessible at all times
    submit_button = st.button("Submit Writing Responses")

    # Timer loop
    while time.time() < end_time:
        if submit_button:
            break  # Break the loop if the button is clicked

        remaining_time = int(end_time - time.time())
        minutes, seconds = divmod(remaining_time, 60)
        timer_placeholder.markdown(
            f'<span style="color:red; font-weight:bold; font-size:40px;">**Time remaining:** {minutes} minutes {seconds} seconds</span>',
            unsafe_allow_html=True)
        time.sleep(1)

    # Evaluation when the button is clicked or when the timer ends
    if submit_button:
        st.write("Thank you for your responses. Your answers will now be evaluated.")
        feedback = evaluate_writing_passage(response1)
        st.write("Feedback for Task 1:", feedback)
        feedback = evaluate_writing_passage(response2)
        st.write("Feedback for Task 2:", feedback)
    else:
        st.write("Time's up! Submitting your responses now.")
        feedback = evaluate_writing_passage(response1)
        st.write("Feedback for Task 1:", feedback)
        feedback = evaluate_writing_passage(response2)
        st.write("Feedback for Task 2:", feedback)





