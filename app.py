import streamlit as st
from openai import OpenAI
from gtts import gTTS
import os
import PyPDF2

# Function to call OpenAI's GPT-3.5 API for translation
def translate_text(text, target_language):
    client = OpenAI()
    
    prompt = f"Translate the following text to {target_language}: \"{text}\""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful translator."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Function to generate Text-to-Speech
def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language)
    audio_path = "translated_audio.mp3"
    tts.save(audio_path)
    return audio_path

# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":  # TXT file
        return str(uploaded_file.read(), "utf-8")
    
    elif uploaded_file.type == "application/pdf":  # PDF file
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    
    return ""


# The main app UI start...

# Title
st.title("Simple GPT Translation App")

# Logic to allowing users to either enter text directly or upload a file
options = ["Enter text directly", "Upload document"]
selection = st.segmented_control(
    "Choose input", options, selection_mode="single", default=options[0]
)


if selection is options[0]:
    # Text area to input text 
    text_to_translate = st.text_area("Enter text to translate:")

elif selection is options[1]:
    # File upload
    uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])
    file_text = ""
    if uploaded_file is not None:
        file_text = extract_text_from_file(uploaded_file)
        text_to_translate = st.text_area("Extracted Text:", file_text, height=150)




# Dropdown menu to select languages 
languages = {"French": "fr", "Spanish": "es", "German": "de", "Chinese": "zh", "Japanese": "ja"}
target_language = st.selectbox("Select target language:", options=list(languages.keys()))

# Translate button
if st.button("Translate"):
    if text_to_translate.strip():
        translated_text = translate_text(text_to_translate, languages[target_language])
        st.success("Translation:")
        st.write(translated_text)

        # Generate and display speech
        audio_file = text_to_speech(translated_text, languages[target_language])
        st.audio(audio_file, format="audio/mpeg")
        
    else:
        st.warning("Please enter text to translate.")

# End main app UI.