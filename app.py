import streamlit as st
from groq import Groq  # Importing the Groq library
from apikey import GROQ_API_KEY
import speech_recognition as sr
import pyttsx3
import io

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize conversation history and input state in Streamlit session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = 'response.mp3'  # Default filename for audio
if 'listening' not in st.session_state:
    st.session_state.listening = False  # Track listening state

def generate_response(user_input):
    """Generate a response using Llama 3 and maintain conversation context."""
    # Add the current user input to the conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Create a completion with the conversation history
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.conversation_history,  # Send the entire conversation history
        temperature=0.7,
        max_tokens=150,
        top_p=0.9,
        stream=True,
        stop=None,
    )

    # Gather the response text
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    # Add the response to the conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})

    return response_text

def speak_text(text):
    """Convert text to speech and save it to a file."""
    # Use a fixed filename for the audio response
    audio_filename = st.session_state.audio_file
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()
    with open(audio_filename, 'rb') as audio_file:
        audio_data = audio_file.read()
    return audio_data

def main():
    # Custom CSS for a minimalist background with blue and green dots
    st.markdown("""
        <style>
        /* White background with blue and green dots */
        body {
            background-color: #fff;
            font-family: Arial, sans-serif;
        }
        .centered-title {
            text-align: center;
            color: #333;
        }

        /* Chat bubbles styling */
        .chat-bubble {
            padding: 15px;
            border-radius: 20px;
            max-width: 70%;
            margin-bottom: 15px;
            font-size: 1.1rem;
            line-height: 1.4;
        }
        .user-bubble {
            background-color: #2D8CFF;
            text-align: left;
            color: white;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.15);
            animation: userBubbleAnimation 0.5s ease;
        }
        .bot-bubble {
            background-color: #f3e5ab;
            text-align: right;
            color: #000;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.15);
            animation: botBubbleAnimation 0.5s ease;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .chat-container .bot-bubble {
            align-self: flex-end;
        }

        

        /* Modern button styles */
        .stButton>button {
    background-color: #89D85D;
    color: black;
    font-weight: bold;
    border: none;
    padding: 12px 28px;
    text-align: center;
    font-size: 18px;
    margin: 6px 2px;
    cursor: pointer;
    border-radius: 12px;
    transition: all 0.3s ease;
    outline: none;  /* Remove default outline */
}

.stButton>button:hover {
    background-color: #013220;
    transform: scale(1.05);
    color: white;
}

.stButton>button:focus,
.stButton>button:active {
    background-color: #89D85D;  /* Ensure the background color remains consistent */
    color: black;  /* Ensure the font color remains consistent */
    outline: none;  /* Remove default outline */
    box-shadow: none;  /* Remove any box shadow */
}

        .stAudio {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-chat-area">', unsafe_allow_html=True)  # Open main chat area with white background

    st.markdown('<h1 class="centered-title">🤖Voice Chatbot🗣️</h1>', unsafe_allow_html=True)

    # Display the conversation history
    st.subheader("Conversation")
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.conversation_history:
        if msg['role'] == 'user':
            chat_html += f'<div class="chat-bubble user-bubble">You: {msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-bubble bot-bubble">Bot: {msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Audio input from the user
    st.subheader("Speak to the chatbot")
    
    # Create a placeholder for the status message
    status_placeholder = st.empty()
    
    if st.button("Start Listening"):
        st.session_state.listening = True
        status_placeholder.text("Listening...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                st.session_state.user_input = recognizer.recognize_google(audio)
                st.write(f"You said: {st.session_state.user_input}")
                if st.session_state.user_input:
                    response = generate_response(st.session_state.user_input)
                    st.session_state.user_input = ""  # Clear input after sending
                    audio_data = speak_text(response)
                    st.audio(io.BytesIO(audio_data), format="audio/mp3")
                    st.session_state.listening = False
                    status_placeholder.empty()  # Clear the status message
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
                st.session_state.listening = False
                status_placeholder.empty()  # Clear the status message
            except sr.RequestError:
                st.write("Sorry, there was an error with the speech recognition service.")
                st.session_state.listening = False
                status_placeholder.empty()  # Clear the status message

    # JavaScript to handle Enter key press for text input
    st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const input = document.querySelector('input[type="text"]');
            const button = document.querySelector('button');

            input.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    event.preventDefault();  // Prevent the default form submission
                    button.click();         // Trigger the button click
                }
            });
        });
        </script>
    """, unsafe_allow_html=True)

    # Scroll to the latest message
    st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close main chat area

if __name__ == "__main__":
    main()
