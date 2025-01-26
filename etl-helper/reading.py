# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:06:00 2024

@author: varun
"""

import streamlit as st
import streamlit as st
import openai
import json
from google.oauth2 import service_account
import google.cloud.texttospeech as texttospeech
from utils import get_reading_passage, generate_questions_from_reading_passage


def handle_reading_section():
     #generate the passage and questions only once, store them in session state
    if 'reading_passage' not in st.session_state:
        st.session_state.reading_passage = get_reading_passage()  # Generate the reading passage
        st.session_state.reading_questions_json = generate_questions_from_reading_passage(st.session_state.reading_passage, 6)

    # retrieve passage and questions from session state
    passage = st.session_state.reading_passage
    questions_json = json.loads(st.session_state.reading_questions_json)

    # initialize session state for tracking answers and score
    if 'reading_user_answers' not in st.session_state:
        st.session_state.reading_user_answers = {}
    if 'reading_score' not in st.session_state:
        st.session_state.reading_score = 0
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
    #display the reading passage
    st.header("Reading Section")
    st.markdown(f"<div style='padding: 10px; border-radius: 5px;'>{passage}</div>",
                unsafe_allow_html=True)

    #display questions and options
    for idx, q in enumerate(questions_json):
        st.markdown(f'<p class="question-text">Question {idx + 1}: {q["question"]}</p>', unsafe_allow_html=True)

        options = q['options']
        selected_answer = st.session_state.reading_user_answers.get(idx, None)
        selected_index = options.index(selected_answer) if selected_answer else 0

        #display the radio button for answer selection
        user_answer = st.radio(
            label="Choose your answer:",
            options=options,
            key=f"reading_question_{idx}",
            index=selected_index
        )

        st.session_state.reading_user_answers[idx] = user_answer


    if st.button("Submit Reading Answers", key="submit_reading_answers", help="Submit all your answers at once"):
        score = 0

        for idx, q in enumerate(questions_json):
            user_answer = st.session_state.reading_user_answers.get(idx, None)
            correct_answer = q['correct_answer']

            question_text = f"Question {idx + 1}: {q['question']}"
            if user_answer == correct_answer:
                question_text = f'<p class="correct-answer">{question_text} ✅</p>'
                score += 1
            else:
                question_text = f'<p class="incorrect-answer">{question_text} ❌</p>'
            st.markdown(question_text, unsafe_allow_html=True)

            # Show the correct answer and explanation
            if user_answer == correct_answer:
                st.markdown(f'<p class="answer-text">You answered correctly: <b>{user_answer}</b></p>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<p class="answer-text">Your answer: <b>{user_answer}</b>. Correct answer: <b>{correct_answer}</b></p>',
                    unsafe_allow_html=True)

            st.markdown(f'<p class="explanation">Explanation: {q["explanation"]}</p>', unsafe_allow_html=True)


        st.session_state.reading_score = score
        st.markdown(f'<p class="score">Your final score: {score}/{len(questions_json)}</p>', unsafe_allow_html=True)

