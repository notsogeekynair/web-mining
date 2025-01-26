# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:05:30 2024

@author: varun
"""
import streamlit as st
from listening import handle_listening_section
from reading import handle_reading_section
from writing import handle_writing_section

def main():
    st.title("TOEFL Practice Application")


    section = st.sidebar.selectbox("Choose Section", ["Listening", "Reading", "Writing"])
    # Display instructions for the selected section
    display_instructions(section)
    # Call the respective section's handler
    if section == "Listening":
        handle_listening_section()
    elif section == "Reading":
        handle_reading_section()
    elif section == "Writing":
        handle_writing_section()

def display_instructions(section):
    if section == "Listening":
        st.sidebar.markdown("""
             ## Listening Section Instructions:
             - In this section, you will listen to a passage and answer questions based on it.
             - You will be given a few questions after the audio, and you will need to select the correct answer.
             - After you submit your answers, you will receive feedback and explanations for each question.
         """)
    elif section == "Reading":
        st.sidebar.markdown("""
             ## Reading Section Instructions:
             - In this section, you will read a passage and answer questions based on the content.
             - There will be multiple-choice questions, and you need to select the correct answer for each one.
             - After submission, you will receive feedback on your answers and explanations.
         """)
    elif section == "Writing":
        st.sidebar.markdown("""
             ## Writing Section Instructions:
             - In this section, you will be asked to write two essays based on the given prompts.
             - Each essay has a time limit, and you will need to type your responses within the given time.
             - After submission, your writing will be evaluated, and feedback will be provided.
         """)


if __name__ == "__main__":
    main()

