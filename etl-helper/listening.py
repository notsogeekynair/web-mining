import streamlit as st
import openai
import json
from google.oauth2 import service_account
from utils import generate_lecture, generate_questions_from_passage, text_to_audio
import google.cloud.texttospeech as texttospeech

openai.api_key = "insert-openai-api-key-here"


def handle_listening_section():
    credentials = service_account.Credentials.from_service_account_file("D:/BU/Fall 24/Web Mining/Term Project/ept-helper-442122-e21a06ec1cd4.json")
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    #generate the passage and questions only once and store them in session state
    if 'passage' not in st.session_state:
        st.session_state.passage = generate_lecture()
        st.session_state.audio_file = text_to_audio(st.session_state.passage)  # Store the audio file path
        st.session_state.questions_json = generate_questions_from_passage(st.session_state.passage, 5)

    #fetch the data from session state
    passage = st.session_state.passage
    audio_file = st.session_state.audio_file
    questions_json = json.loads(st.session_state.questions_json)

    #initialize session state for tracking answers and score
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'score' not in st.session_state:
        st.session_state.score = 0

    st.header("Listening Section", anchor='top')

    # Audio player: Play the generated audio
    st.audio(audio_file, format="audio/mp3")
    st.markdown("""
        <style>
            .question-text {font-size: 18px; font-weight: bold;}
            .answer-text {font-size: 16px; padding: 5px;}
            .correct-answer {color: green; font-weight: bold;}
            .incorrect-answer {color: red; font-weight: bold;}
            .explanation {color: #2f4f4f; font-style: italic;}
            .score {font-size: 20px; color: #4CAF50; font-weight: bold;}
            .btn {background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;}
            .btn:hover {background-color: #45a049;}
        </style>
    """, unsafe_allow_html=True)

    # display questions and answer options
    for idx, q in enumerate(questions_json):
        st.markdown(f'<p class="question-text">Question {idx + 1}: {q["question"]}</p>', unsafe_allow_html=True)

        options = q['options']
        selected_answer = st.session_state.user_answers.get(idx, None)  # Get stored answer
        selected_index = options.index(
            selected_answer) if selected_answer else 0  # Set the selected answer index for the radio button

        user_answer = st.radio(
            label="Choose your answer:",
            options=options,
            key=f"question_{idx}",
            index=selected_index
        )

        st.session_state.user_answers[idx] = user_answer  # Store the user's answer in session state

    #submit all answers and show results
    if st.button("Submit All Answers", key="submit_all_answers", help="Submit all your answers at once"):
        score = 0

        for idx, q in enumerate(questions_json):
            user_answer = st.session_state.user_answers.get(idx, None)
            correct_answer = q['correct_answer']

            question_text = f"Question {idx + 1}: {q['question']}"  # Highlight question based on the answer
            if user_answer == correct_answer:
                question_text = f'<p class="correct-answer">{question_text} ✅</p>'
                score += 1
            else:
                question_text = f'<p class="incorrect-answer">{question_text} ❌</p>'
            st.markdown(question_text, unsafe_allow_html=True)

            # Show the answer and explanation
            if user_answer == correct_answer:
                st.markdown(f'<p class="answer-text">You answered correctly: <b>{user_answer}</b></p>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<p class="answer-text">Your answer: <b>{user_answer}</b>. <br>Correct answer: <b>{correct_answer}</b></p>',
                    unsafe_allow_html=True)

            st.markdown(f'<p class="explanation">Explanation: {q["explanation"]}</p>', unsafe_allow_html=True)

        # Display the final score
        st.markdown(f'<p class="score">Your final score: {score}/{len(questions_json)}</p>', unsafe_allow_html=True)
