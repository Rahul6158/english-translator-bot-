import streamlit as st
from translate import Translator
from gtts import gTTS
import os
import base64

# Define the language mapping
language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "hi": "Hindi",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-cn": "Simplified Chinese",
    "ru": "Russian",
    "ar": "Arabic",
    "th": "Thai",
    "tr": "Turkish",
    "pl": "Polish",
    "cs": "Czech",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "el": "Greek",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "no": "Norwegian",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "ro": "Romanian",
    "bn": "Bengali",
    "fa": "Persian",
    "iw": "Hebrew",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "hr": "Croatian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "is": "Icelandic",
    "ga": "Irish",
    "sq": "Albanian",
    "mk": "Macedonian",
    "hy": "Armenian",
    "ka": "Georgian",
    "mt": "Maltese",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "ne": "Nepali",
    "si": "Sinhala",
    "km": "Khmer",
    "lo": "Lao",
    "my": "Burmese",
    "jw": "Javanese",
    "mn": "Mongolian",
    "zu": "Zulu",
    "xh": "Xhosa"
}

# Function to translate text
def translate_text(text, target_language):
    if target_language in language_mapping:
        translator = Translator(to_lang=target_language)
        translation = translator.translate(text)
        return translation
    else:
        return "Language not found in the mapping"

# Function to convert text to speech and save as an MP3 file
def convert_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)
    else:
        st.warning("No text to speak")

def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

def main():
    st.image("jangirii.png", width=50)
    st.title("Text Translation and Conversion to speech")
    
    # Get user input
    text = st.text_area("Enter text to translate and convert to speech:")
    target_language = st.selectbox("Select target language:", list(language_mapping.values()))

    # Check if the target language is in the mapping
    target_language_code = [code for code, lang in language_mapping.items() if lang == target_language][0]

    # Translate the input text
    translated_text = translate_text(text, target_language_code)

    # Display translated text
    if translated_text:
        st.subheader(f"Translated text ({target_language}):")
        st.write(translated_text)
    else:
        st.warning("Translation result is empty. Please check your input text.")

    # Convert the translated text to speech
    if st.button("Convert to Speech"):
        output_file = "translated_speech.mp3"
        convert_text_to_speech(translated_text, output_file, language=target_language_code)

          # Play the generated speech
        audio_file = open(output_file, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')

        # Play the generated speech (platform-dependent)
        if os.name == 'posix':  # For Unix/Linux
            os.system(f"xdg-open {output_file}")
        elif os.name == 'nt':  # For Windows
            os.system(f"start {output_file}")
        else:
            st.warning("Unsupported operating system")

        # Provide download link for the MP3 file
        st.markdown(get_binary_file_downloader_html("Download Audio File", output_file, 'audio/mp3'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
