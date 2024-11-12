import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import io
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.colors import HexColor

# Initialize the Groq client
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize conversation history and input state in Streamlit session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = 'response.mp3'
if 'listening' not in st.session_state:
    st.session_state.listening = False

def generate_response(user_input):
    """Generate a response using Llama 3 and maintain conversation context."""
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Create a completion with the conversation history
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.conversation_history,
        temperature=0.7,
        max_tokens=200,
        top_p=0.9,
        stream=True,
        stop=None,
    )

    response_text = ""
    for chunk in completion:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            response_text += chunk.choices[0].delta.content or ""

    st.session_state.conversation_history.append({"role": "assistant", "content": response_text})
    return response_text

# def speak_text(text):
#     """Convert text to speech, adjust speech rate for clarity, and save it to a file."""
#     engine.setProperty('rate', 125)  # Adjust this value to control the speed (lower for slower speech)
#     engine.setProperty('volume', 1.0)  # Set the volume level (1.0 is max)
    
#     audio_filename = st.session_state.audio_file
#     engine.save_to_file(text, audio_filename)
#     engine.runAndWait()
    
#     # Return the audio data for Streamlit
#     with open(audio_filename, 'rb') as audio_file:
#         audio_data = audio_file.read()
#     return audio_data

def speak_text(text):
    """Convert text to speech using a female voice, adjust speech rate for clarity, and save it to a file."""
    # Select the female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
    engine.setProperty('rate', 125)  # Adjust speech rate for clarity
    engine.setProperty('volume', 1.0)  # Set volume to maximum
    
    audio_filename = st.session_state.audio_file
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()
    
    # Return the audio data for Streamlit
    with open(audio_filename, 'rb') as audio_file:
        audio_data = audio_file.read()
    return audio_data




from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.units import inch

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def generate_analysis_report():
    """Generate a well-formatted PDF report based on the conversation history."""
    user_responses = [msg['content'] for msg in st.session_state.conversation_history if msg['role'] == 'user']

    prompt = (
        "Based on the following conversation, generate a detailed report focusing on the user's behavior, "
        "phoneme practice, confidence-building progress, and learning strategies. Please avoid filler text like asterisks (*). "
        "\n\nConversation:\n"
    )

    for msg in st.session_state.conversation_history:
        prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

    try:
        response_text = generate_response(prompt)

        if not response_text.strip():
            raise ValueError("The generated response is empty. Check the API response or prompt.")

        # Create a PDF document
        pdf_filename = "analysis_report.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom style for the header text
        header_style = ParagraphStyle(
            name='HeaderStyle',
            fontSize=28,
            leading=32,
            textColor=colors.HexColor("#1F4E79"),
            alignment=1,  # Center alignment
            spaceAfter=20,
            fontName='Helvetica-BoldOblique',
            backColor=colors.lightblue
        )

        # Generate the logo using Matplotlib
        def create_logo_with_matplotlib():
            fig, ax = plt.subplots(figsize=(2, 2), dpi=150)  # Adjust the size and resolution
            ax.axis('off')  # Hide axes
            img = mpimg.imread('recordMic.png')  # Path to your logo image
            ax.imshow(img)
            plt.savefig('logo_mpl.png', bbox_inches='tight', pad_inches=0)  # Save the logo image

        # Call the function to create the logo
        create_logo_with_matplotlib()

        # Add the logo using the same process as the chart
        logo_path = 'logo_mpl.png'
        story = []

        # Insert the logo at the top
        story.append(Image(logo_path, width=1*inch, height=1*inch))
        story.append(Spacer(1, 12))

        # Add the header
        header_text = "ARTICULATEIQ - Conversational AI"
        story.append(Paragraph(header_text, header_style))
        story.append(Spacer(1, 12))
        # Add a title
        title = "User Details Summary"
        title_style = ParagraphStyle(
            name='TitleStyle',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1F4E79"),
            alignment=1,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))

        # Subtitle for Patient Demographics
        subtitle_style = ParagraphStyle(
            name='SubtitleStyle',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#1F4E79"),
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("User Demographics", subtitle_style))

        # Adding a table with patient details
        patient_data = [
            ['Name', 'Celeste Lim'],
            ['Gender', 'Female'],
            ['Location', 'St Rita Ward'],
            ['ID No.', '1234565'],
            ['Date of Birth', 'March 9, 2015'],
            ['Nationality', 'Filipino'],
            ['Visit No.', '2021-9-9-022'],
            ['Age', '7 y, 8 mos'],
            ['Race', 'Chinese']
        ]

        patient_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        patient_table = Table(patient_data, style=patient_table_style)
        story.append(patient_table)
        story.append(Spacer(1, 12))

        # Subtitle for Medical / Surgical / Family History
        story.append(Paragraph("Conversation Analysis Insights ", subtitle_style))
        medical_history_text = "Medical Consultancy needed: N.A."
        story.append(Paragraph(medical_history_text, styles['BodyText']))
        story.append(Spacer(1, 12))

        # Adding another table for Admission details
        admission_data = [
            ['Interaction Date / Time', 'September 8, 2021 / 22:00H'],
            ['User Name', 'John Doe'],
            ['Reason for Interaction', 'Seeking support for neurodiversity and confidence issues'],
            ['Primary Concern', 'Autism Spectrum Disorder'],
            ['Secondary Concern', 'Generalized Anxiety Disorder'],
            ['Other Concerns', 'Low self-esteem, Social anxiety'],
            ['Goals', 'Improve confidence, Enhance social skills, Manage anxiety']
        ]

        admission_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        admission_table = Table(admission_data, style=admission_table_style)
        story.append(admission_table)
        story.append(Spacer(1, 12))

                # Add the generated analysis text
        

        # Define a bold style for headings
        heading_style = ParagraphStyle(name="HeadingStyle", fontSize=14, leading=16, spaceAfter=12, textColor=HexColor("#000000"), fontName="Helvetica-Bold")

        # Add the generated analysis text
        response_text_cleaned = response_text.replace('*', '')  # Remove asterisks
        analysis_paragraphs = response_text_cleaned.strip().split('\n')
        formatted_analysis = []

        for paragraph in analysis_paragraphs:
            if paragraph.strip():
                # Check if the paragraph is a heading (ends with a colon)
                if paragraph.strip().endswith(':'):
                    formatted_analysis.append(Paragraph(paragraph.strip(), heading_style))
                else:
                    formatted_analysis.append(Paragraph(paragraph.strip(), styles['BodyText']))
                formatted_analysis.append(Spacer(1, 12))

        story.extend(formatted_analysis)

        # Add charts and illustrations

        # Example: Bar chart
        data = {'Phoneme Practice': [80, 85, 90, 95, 92],
                'Confidence': [70, 75, 80, 85, 88],
                'Social Skills': [60, 65, 70, 75, 78]}
        df = pd.DataFrame(data, index=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'])
        
        plt.figure(figsize=(8, 4))
        sns.lineplot(data=df)
        plt.title('Progress Over Time')
        plt.ylabel('Percentage')
        plt.xlabel('Weeks')
        plt.grid(True)
        plt.tight_layout()
        chart_path = 'progress_chart.png'
        plt.savefig(chart_path)
        plt.close()
        
        story.append(Image(chart_path, width=6*inch, height=3*inch))
        story.append(Spacer(1, 12))

        # Add a heading for the flowchart
        flowchart_heading = Paragraph("The Four Level Analysis", heading_style)
        story.append(flowchart_heading)
        story.append(Spacer(1, 12))

        # Add the flowchart image
        flowchart_path = 'flowchart.png'  # Path to the flowchart image
        story.append(Image(flowchart_path, width=6*inch, height=4*inch))  # Adjust dimensions as needed
        story.append(Spacer(1, 12))

        # Build the PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.build(story)

        buffer.seek(0)
        pdf_data = buffer.read()
        
        return pdf_data, pdf_filename

    except Exception as e:
        print(f"Error generating report: {e}")
        return None, None
def main():
    st.markdown("""
        <style>
        body {
            background-color: #fff;
            font-family: Arial, sans-serif;
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
            outline: none;
        }

        .stButton>button:hover {
            background-color: #013220;
            transform: scale(1.05);
            color: white;
        }

        .stButton>button:focus,
        .stButton>button:active {
            background-color: #89D85D;
            color: black;
            outline: none;
            box-shadow: none;
        }

        .stAudio {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-chat-area">', unsafe_allow_html=True)  # Open main chat area with white background

    st.markdown('<h1 class="centered-title">🤖 Pronunciation & Confidence-Boosting Chatbot 🗣️</h1>', unsafe_allow_html=True)

    if len(st.session_state.conversation_history) == 0:
        introduction = (
            "Hello! I'm your chatbot, here to help you improve your pronunciation and boost your confidence while you learn. "
            "We will practice some sounds and have fun conversations together. Let’s start! How are you feeling today?"
        )
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
                    # Ask targeted questions to practice phonemes and build confidence
                    question_prompts = [
                        "Great! Now, let's practice saying some sounds. Can you say 'p' and 'b' for me?",
                        "Can you try saying 's' and 'sh'? These are tricky but you're doing amazing!",
                        "How about the sound 'k'? That's the sound in 'cat.' Can you say it?",
                        "Can you tell me about your favorite hobby? Don’t worry, just relax and share anything!"
                    ]

                    response = generate_response(st.session_state.user_input)
                    st.session_state.user_input = ""  # Clear input after sending
                    
                    audio_data = speak_text(response)
                    st.audio(io.BytesIO(audio_data), format="audio/mp3")

                    # Continue boosting confidence
                    encouragement = "You're doing so well! Keep going, I believe in you!"
                    st.session_state.conversation_history.append({"role": "assistant", "content": encouragement})
                    
                    st.session_state.listening = False
                    status_placeholder.empty()

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
                st.session_state.listening = False
                status_placeholder.empty()

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
                st.session_state.listening = False
                status_placeholder.empty()
            except sr.RequestError as e:
                st.write(f"Could not request results; {e}")
                st.session_state.listening = False
                status_placeholder.empty()

    st.subheader("Type to the chatbot")

    # Input box for user to type their input
    st.session_state.user_input = st.text_input("You: ", st.session_state.user_input, key="user_input_box")
    
    if st.session_state.user_input:
        response = generate_response(st.session_state.user_input)
        st.session_state.user_input = ""  # Clear input after sending

        audio_data = speak_text(response)
        st.audio(io.BytesIO(audio_data), format="audio/mp3")

    st.markdown('<br><hr><br>', unsafe_allow_html=True)

    if st.button("Generate Report"):
        pdf_data, pdf_filename = generate_analysis_report()
        if pdf_data:
            st.success("Report generated successfully!")
            st.download_button(
                label="Download Analysis Report",
                data=pdf_data,
                file_name=pdf_filename,
                mime="application/pdf",
            )
        else:
            st.error("Failed to generate report.")

    st.markdown('</div>', unsafe_allow_html=True)  # Close main chat area

if __name__ == "__main__":
    main()
