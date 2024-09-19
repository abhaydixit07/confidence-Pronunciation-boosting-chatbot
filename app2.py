import streamlit as st
from groq import Groq
from apiKey import GROQ_API_KEY

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize conversation history and input state in Streamlit session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

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
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            response_text += chunk.choices[0].delta.content or ""

    # Add the response to the conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})

    return response_text

def main():
    st.markdown("""
        <style>
        body {
            background-color: #fff;
        }
        .centered-title {
            text-align: center;
            color: #333;
        }
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
        }
        .bot-bubble {
            background-color: #f3e5ab;
            text-align: right;
            color: #000;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.15);
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .chat-container .bot-bubble {
            align-self: flex-end;
        }
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
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-chat-area">', unsafe_allow_html=True)

    st.markdown('<h1 class="centered-title">🤖 Text-based Chatbot</h1>', unsafe_allow_html=True)

    # If conversation history is empty, start with an introductory message
    if len(st.session_state.conversation_history) == 0:
        introduction = "Hello! I'm Edusync's chatbot. I'm here to help you with your learning journey. How are you feeling today about your studies?"
        st.session_state.conversation_history.append({"role": "assistant", "content": introduction})
        st.write(introduction)

    st.subheader("Conversation")
    # Display the conversation history
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.conversation_history:
        if msg['role'] == 'user':
            chat_html += f'<div class="chat-bubble user-bubble">You: {msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-bubble bot-bubble">Bot: {msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input field for the user to type a message
    st.subheader("Type your message:")
    user_input = st.text_area("", st.session_state.user_input, height=100, key="user_input")

    # Button to submit the message
    if st.button("Send"):
        if user_input.strip():  # Ensure the input is not empty
            response = generate_response(user_input.strip())
            st.session_state.user_input = ""  # Clear input after sending
            # Clear the input field
            st.session_state['user_input'] = ""
            st.experimental_rerun()  # Rerun the app to clear the text area

if __name__ == "__main__":
    main()
