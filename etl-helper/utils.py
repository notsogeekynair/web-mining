import openai
from google.oauth2 import service_account
import google.cloud.texttospeech as texttospeech
import random

openai.api_key = "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"
lecture_topics = [
    "The impact of climate change on ecosystems",
    "Space exploration and the history of space missions",
    "The causes and effects of the Industrial Revolution"
    "The history of the Roman Empire",
    "Fundamentals of machine learning",
    "The evolution of human communication",
    "The role of technology in modern education",
    "The process of photosynthesis in plants",
    "The development of quantum computing",
    "The causes and effects of the French Revolution",
    "The principles of economic inflation",
    "The geography of the Amazon Rainforest"
]

def generate_questions_from_passage(passage, num_questions=6):
    try:
        # Prompt to generate questions based on the passage, with JSON formatting
        prompt = f"""
    Given the following lecture passage, generate {num_questions} multiple-choice questions based on the content of the lecture. 
    For each question, provide 1 correct answer and 3 distractors (incorrect answers). Include explanations for the correct answers.
    Format the response as a JSON array where each object contains:
    - "question": The question text.
    - "options": A list of 4 possible answer options.
    - "correct_answer": The correct answer from the options.
    - "explanation": A brief explanation of why the answer is correct.

    Here is the lecture passage:

    {passage}

    Please provide the questions in JSON format:
    """
        # Call OpenAI API to generate questions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that generates TOEFL-style questions based on lecture passages."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the response content and parse it as JSON
        questions_json = response['choices'][0]['message']['content']

        # Return the questions in JSON format
        return questions_json

    except Exception as e:
        return f"Error generating questions: {str(e)}"


def generate_lecture():
    try:
        # Randomly select a lecture topic
        selected_topic = random.choice(lecture_topics)

        # Construct a prompt for generating a lecture
        prompt = f"Generate a TOEFL-style lecture on the following topic. The lecture should be detailed, educational, and around 3-5 minutes in length.\n\nTopic: {selected_topic}\n\nLecture:"

        # Call OpenAI's API to generate the lecture
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates TOEFL-style lectures."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the generated lecture text
        lecture_text = response['choices'][0]['message']['content']

        return lecture_text

    except Exception as e:
        return f"Error generating lecture: {str(e)}"

def text_to_audio(passage, output_file="output.mp3"):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            "D:\BU\Fall 24\Web Mining\Term Project\ept-helper-442122-e21a06ec1cd4.json")
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        synthesis_input = texttospeech.SynthesisInput(text=passage)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name="en-GB-Neural2-F",
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,
            pitch=0,
            volume_gain_db=0.0
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(output_file, "wb") as out_file:
            out_file.write(response.audio_content)
            print(f"Audio content written to '{output_file}'")
        return output_file

    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
def get_reading_passage():
    try:
        selected_topic = random.choice(lecture_topics)  # Randomly select a topic
        # Construct a prompt for generating a lecture
        prompt = f"Generate a TOEFL-style reading passage on the following topic. The passage should be informative, academic in tone, and approximately 500-700 words in length, in 3 to 4 paragraphs. It should focus on providing detailed information, including relevant examples. The passage should be designed to assess the reader's comprehension, inferential reasoning, and ability to identify main ideas and supporting details.\n\nTopic: {selected_topic}"

        # Call OpenAI's API to generate the lecture
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates TOEFL/IELTS styled reading passages"},
                {"role": "user", "content": prompt}
            ]
        )
    # Extract and return the generated lecture text
        lecture_text = response['choices'][0]['message']['content']
        return lecture_text
    except Exception as e:
        return f"Error generating lecture: {str(e)}"

def generate_questions_from_reading_passage(passage, num_questions=6):
    try:
        # Prompt to generate questions based on the passage, with JSON formatting
        prompt = f"""
            Given the following reading passage, generate {num_questions} multiple-choice questions based on the content of the passage. 
            For each question, provide 1 correct answer and 3 distractors (incorrect answers). Ensure the questions test a variety of reading comprehension skills, such as:
            - Understanding main ideas
            - Identifying supporting details
            - Making inferences
            - Understanding vocabulary in context
            - Summarizing information
            - Identifying the author's purpose

            For each question:
            - Provide a brief explanation of why the correct answer is accurate based on the passage.
            - Format the response as a JSON array where each object contains:
                - "question": The question text.
                - "options": A list of 4 possible answer options.
                - "correct_answer": The correct answer from the options.
                - "explanation": A brief explanation of why the answer is correct.

            Here is the reading passage:

            {passage}

            Please provide the questions in JSON format:
        """

        # Call OpenAI API to generate questions
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that generates TOEFL-style questions based on reading passages."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the response as JSON
        questions_json = response['choices'][0]['message']['content']

        # Return the questions in JSON
        return questions_json

    except Exception as e:
        return f"Error generating questions: {str(e)}"
