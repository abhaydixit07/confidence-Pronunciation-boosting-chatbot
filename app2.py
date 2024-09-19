import streamlit as st
from groq import Groq
from apiKey import GROQ_API_KEY
import speech_recognition as sr
from gtts import gTTS
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import matplotlib.pyplot as plt
import base64

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

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
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            response_text += chunk.choices[0].delta.content or ""

    # Add the response to the conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})

    return response_text

def speak_text(text):
    """Convert text to speech using gTTS and return it as a byte stream."""
    tts = gTTS(text)
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)  # Reset the stream pointer to the beginning
    return audio_data

def generate_analysis_report():
    """Generate a brief report on behavior and learning based on the conversation history."""
    user_responses = [msg['content'] for msg in st.session_state.conversation_history if msg['role'] == 'user']
    
    # Define the report prompt for generating a summary
    prompt = (
        "You are a conversation analyser bot so Based on the following conversation, generate a brief report focusing on the user's behavior and learning. "
        "Identify key themes, concerns, and learning strategies mentioned. Provide a summary of the user's educational needs and any suggestions for improvement. \n\n"
        "Conversation:\n"
    )
    
    for msg in st.session_state.conversation_history:
        prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
    
    try:
        # Generate a response based on the conversation
        response_text = generate_response(prompt)
        
        if not response_text.strip():
            raise ValueError("The generated response is empty. Check the API response or prompt.")
        
        # Create a PDF document
        pdf_filename = "analysis_report.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom styles for the report
        title_style = ParagraphStyle(name="TitleStyle", fontSize=28, alignment=1, spaceAfter=20)
        header_style = ParagraphStyle(name="HeaderStyle", fontSize=16, spaceAfter=10, bold=True)
        body_style = ParagraphStyle(name="BodyStyle", fontSize=12, spaceAfter=6, leading=15)

        # Build the story for the PDF
        story = []

        # Add the cover page
        story.append(Paragraph("User Learning Analysis Report", title_style))
        story.append(Spacer(1, 12))  # Space after the cover page content
        
        # Add the introduction section
        story.append(Paragraph("Introduction", header_style))
        story.append(Paragraph(
            "This report is based on the user's interaction with the chatbot. "
            "The following sections summarize key themes from the conversation and provide insights into learning behaviors and strategies.", 
            body_style))
        story.append(Spacer(1, 12))

        # Add the analysis section
        story.append(Paragraph("Analysis and Insights", header_style))
        story.append(Paragraph(response_text, body_style))

        # Generate a sample pie chart
        labels = ['Key Theme 1', 'Key Theme 2', 'Key Theme 3']
        sizes = [30, 45, 25]  # Just for illustration; replace with actual data
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the plot to a byte stream
        pie_image = io.BytesIO()
        plt.savefig(pie_image, format='png')
        pie_image.seek(0)
        
        # Add the pie chart to the report
        story.append(Spacer(1, 12))
        pie_chart = Image(pie_image)
        pie_chart.drawWidth = 400
        pie_chart.drawHeight = 400
        story.append(pie_chart)
        
        # Build and save the document
        doc.build(story)

        # Read the PDF file to return as a byte stream
        with open(pdf_filename, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        return pdf_data, pdf_filename

    except Exception as e:
        st.write(f"Error generating report: {e}")
        return None, "An error occurred while generating the report."

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

    st.markdown('<h1 class="centered-title">🤖Voice Chatbot🗣️</h1>', unsafe_allow_html=True)

    if len(st.session_state.conversation_history) == 0:
        introduction = "Hello! I'm Edusync's chatbot. I'm here to help you with your learning journey. How are you feeling today about your studies?"
        st.session_state.conversation_history.append({"role": "assistant", "content": introduction})
        st.write(introduction)

    st.subheader("Conversation")
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.conversation_history:
        if msg['role'] == 'user':
            chat_html += f'<div class="chat-bubble user-bubble">You: {msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-bubble bot-bubble">Bot: {msg["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    st.subheader("Speak to the chatbot")
    
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
                st.write("Sorry, I could not understand your speech. Please try again.")
                st.session_state.listening = False
            except sr.RequestError as e:
                st.write(f"Error: {e}")
                st.session_state.listening = False

    st.subheader("Analysis Report")
    if st.button("Generate Report"):
        pdf_data, pdf_filename = generate_analysis_report()
        if pdf_data:
            b64_pdf = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}">Download your report</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
