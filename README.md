# Pronunciation & Confidence-Boosting Chatbot 🗣️🤖

An AI-powered chatbot designed to help users improve their pronunciation, build confidence, and practice communication skills. The chatbot provides personalized feedback, interactive conversations, and generates detailed progress reports.

---

## Features ✨

- **Interactive Chat:** Engage in meaningful conversations to practice communication skills.
- **Phoneme Practice:** Focused exercises to improve pronunciation of specific sounds.
- **Text-to-Speech:** Audio feedback with adjustable speed and clarity.
- **Speech Recognition:** Converts spoken words into text for interaction.
- **Progress Analysis:** Generate a PDF report with conversation insights, progress charts, and user details.
- **Custom Styling:** Visually appealing chat bubbles and user interface.

---

## Technologies Used 💻

- **Frontend:**
  - [Streamlit](https://streamlit.io/) for building the user interface.
  - Custom CSS for styling chat bubbles and buttons.

- **Backend:**
  - [Groq API](https://groq.com/) for AI-generated responses.
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for handling voice input.
  - [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech conversion.
  - [Python](https://www.python.org/) as the primary programming language.

- **PDF Generation:**
  - [ReportLab](https://www.reportlab.com/) for creating detailed progress reports.
  - Charts generated with [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/).

- **Speech & Audio:**
  - [Py Audio](https://pypi.org/project/pyaudio/) for capturing and playing back audio on Raspberry Pi or compatible devices.

- **Version Control:**
  - [Git](https://git-scm.com/) for version control and collaboration.
  - [GitHub](https://github.com/) for hosting the repository and managing issues.

- **Visualization & Reporting:**
  - [Matplotlib](https://matplotlib.org/) for generating charts and graphs in reports.
  - [Seaborn](https://seaborn.pydata.org/) for enhanced data visualization.


---

## Installation 🛠️

1. **Clone the Repository:**
   ```bash
   https://github.com/abhaydixit07/confidence-Pronunciation-boosting-chatbot.git
   cd confidence-Pronunciation-boosting-chatbot

2. **Set Up the Environment:**
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Add API Key:**
   - Create a file named `apiKey.py` in the root directory.
   - Add your Groq API key:
     ```python
     GROQ_API_KEY = "your-groq-api-key"
     ```

4. **Run the Application:**
   ```bash
   streamlit run Conversational AI.py
   ```

5. **Access the App:**
   Open your browser and navigate to `http://localhost:8501`.

---

## How to Use 📖

1. **Start the Chatbot:**
   - Launch the application and interact with the chatbot.
   - You can type messages or use the "Start Listening" button to speak.

2. **Practice Pronunciation:**
   - Follow the bot's guidance for phoneme exercises like "p" and "b," or "s" and "sh."

3. **Generate Progress Reports:**
   - After a session, click on "Generate Report" to download a detailed PDF analysis.

4. **Listen to Feedback:**
   - Use the integrated text-to-speech feature for audio responses.


---

## License 📜

This project is licensed under the [MIT License](https://github.com/abhaydixit07/confidence-Pronunciation-boosting-chatbot/blob/main/LICENSE).

---

## Acknowledgments 🙏

- The [Groq API](https://groq.com/) for enabling advanced conversational capabilities.
- The [Streamlit](https://streamlit.io/) team for an excellent framework for building interactive apps.
- Open-source libraries like [ReportLab](https://www.reportlab.com/) and [SpeechRecognition](https://pypi.org/project/SpeechRecognition/).
