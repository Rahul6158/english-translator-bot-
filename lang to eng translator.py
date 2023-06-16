import streamlit as st
from langdetect import detect
import mtranslate
import requests

# Set up the Telegram bot token
TOKEN = '6260901632:AAHGkEyHuhMMq9i5E4TR_xqUmOS23qpI0cQ'

# Process incoming message
def process_message(update):
    # Get chat ID from the incoming message
    chat_id = update['message']['chat']['id']

    # Ask for the language to translate to
    send_message(chat_id, 'Im a chatbot which can translate text of any language to English. Enter your text:')

# Process incoming message with language to translate
def process_language(update):
    # Get the language code from the incoming message
    language_code = update['message']['text']

    # Ask for the text to translate
    send_message(chat_id_translation, 'Enter the text to translate:')

    # Store the language code for later use
    st.session_state.language_code_translation = language_code

# Process incoming message with text to translate
def process_text(update):
    # Get the text from the incoming message
    text = update['message']['text']

    # Detect the language of the text
    detected_language = detect(text)

    # Translate the text to the selected language
    translated_text = mtranslate.translate(text, to_language=st.session_state.language_code_translation, from_language=detected_language)

    # Send the translated text as a reply
    send_message(update['message']['chat']['id'], f"Detected Language: {detected_language}\nTranslated Text ({st.session_state.language_code_translation}): {translated_text}")

# Send message via Telegram API
def send_message(chat_id, text):
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.get(SEND_MESSAGE_URL, params=params)

# Set up the Streamlit app
def app():
    st.title("Telegram Chatbot Translator")
    st.write("Enter your text and select the language to translate.")

    # Process incoming message
    if 'update' in st.session_state:
        update = st.session_state.update

        if 'message' in update and 'text' in update['message']:
            if 'entities' in update['message'] and update['message']['entities'][0]['type'] == 'bot_command':
                process_message(update)
            elif update['message']['chat']['id'] == st.session_state.chat_id_translation:
                if 'language_code_translation' not in st.session_state:
                    process_language(update)
                else:
                    process_text(update)

    # Get text from the user
    text = st.text_input("Enter the text to translate:")

    # Send the message to the bot
    if text:
        chat_id = st.session_state.chat_id_translation if 'chat_id_translation' in st.session_state else None
        if not chat_id:
            params = {
                'chat_id': 'YOUR_CHAT_ID',  # Replace with your chat ID
                'text': text
            }
            response = requests.get(SEND_MESSAGE_URL, params=params)
        else:
            detected_language = detect(text)
            translated_text = mtranslate.translate(text, to_language=st.session_state.language_code_translation, from_language=detected_language)
            st.write(f"Detected Language: {detected_language}")
            st.write(f"Translated Text ({st.session_state.language_code_translation}): {translated_text}")

# Continuously poll for new updates
def poll_updates():
    offset = None

    while True:
        response = requests.post(f'{API_URL}getUpdates', json={'offset': offset})
        data = response.json()
        if 'result' in data:
            updates = data['result']
            for update in updates:
                st.session_state.update = update
                offset = update['update_id'] + 1

# Start polling for updates
poll_updates()
