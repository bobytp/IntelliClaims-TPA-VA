import streamlit as st
from io import BytesIO
import PyPDF2
import google.generativeai as genai
import time
from datetime import datetime

# Set up the page configuration
st.set_page_config(
    page_title="Intelli.Claims: The AI virtual agent for Insurance TPA's",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define the sidebar content
with st.sidebar:
    st.header("Intelli.Claims powered by Google Gemini")
    st.markdown(
        """
        <span ><font size=2>1. Enter your Gemini API Key.</font></span>
        <span ><font size=2>2. To ask questions related to an Insurance claim, Upload the claim and start chatting</font></span>
        <span ><font size=2>3. To interact with the TPA Virtual Agent, Remove any uploaded document and start chatting.</font></span>
        """,
        unsafe_allow_html=True,
    )

    # Get the Gemini API key from the user
    google_api_key = st.text_input(
        "Enter your Gemini API Key", key="chatbot_api_key", type="password"
    )
    "[Get Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)"

    # Allow the user to upload a claim document
    uploaded_file = st.file_uploader(
        "Please select the claim for evaluation",
        accept_multiple_files=False,
        type=["pdf"],
    )

    # Button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        st.session_state.chat_history.clear()
        st.experimental_rerun()

    st.divider()

    # Sidebar powered & links section
    st.markdown(
        """<span ><font size=2>Intelli.Claims powered by Google Gemini</font></span>""",
        unsafe_allow_html=True,
    )
    "[Visit us](www.intelli.claims)"
    "[Email us](info@intelli.claims)"

# Display the page header
st.header("Welcome to IntelliClaims the AI powered Virtual Assistant for Insurance TPA")
st.caption("This is a Google Gemini based AI assistant")

# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Welcome to IntelliClaim TPA Virtual Assistant! I'm ready to help you streamline your claims process. To get started, tell me about the claim you'd like to evaluate. If you'd like to submit a claim, upload the document for me to review.",
        }
    ]

# Initialize the chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to format timestamp
def format_timestamp(timestamp):
    return timestamp.strftime("%H:%M:%S")

# Display the chat history with visual enhancements and timestamps
for msg in st.session_state.messages:
    timestamp = datetime.now()  # Get the timestamp here
    if msg["role"] == "assistant":
        with st.chat_message(msg["role"], avatar="🤖"):
            st.markdown(
                f'<div style="font-size: 10px; color: #888; margin-bottom: 5px;">{format_timestamp(timestamp)}</div>'
            )
            st.write(msg["content"])
    else:
        with st.chat_message(msg["role"], avatar="🧑‍💼"):
            st.markdown(
                f'<div style="font-size: 10px; color: #888; margin-bottom: 5px;">{format_timestamp(timestamp)}</div>'
            )
            st.write(msg["content"])

# Process the uploaded PDF file if any
if uploaded_file:
    # Get the PDF content as bytes
    pdf_content = uploaded_file.getvalue()

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))

    # Extract text from all pages
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    # Get the user's prompt from the chat input
    if prompt := st.chat_input(placeholder="Ask your question about the claim..."):
        # Check if the API key is provided
        if not google_api_key:
            st.info("Please enter a valid Google Gemini API key to continue.")
            st.stop()

        # Configure the Google Gemini API
        genai.configure(api_key=google_api_key)

        # Create a Gemini model object
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", )

        # Add user's prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="🧑‍💼").write(prompt)

        # Visual Cues:  Progress bar and Typing Indicator
        with st.chat_message("assistant", avatar="🤖"):
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(101):
                time.sleep(0.02)
                progress_bar.progress(i)

            # Typing indicator
            st.text("Thinking...")
            for i in range(4):
                time.sleep(0.2)
                st.text("Thinking" + "." * (i + 1))

            # Generate a response from the model
            response = model.generate_content(
                f"{pdf_text} \n\n{prompt}", stream=True
            )
            response.resolve()
            msg = response.text

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.text(msg)

# If no file is uploaded, handle user interaction
else:
    # Get the user's prompt from the chat input
    if prompt := st.chat_input(
        placeholder="Ask your question or enter a claim request..."
    ):
        # Check if the API key is provided
        if not google_api_key:
            st.info("Please enter a valid Google Gemini API key to continue.")
            st.stop()

        # Configure the Google Gemini API
        genai.configure(api_key=google_api_key)

        # Create a Gemini model object
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", )

        # Add user's prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="🧑‍💼").write(prompt)

        # Visual Cues:  Progress bar and Typing Indicator
        with st.chat_message("assistant", avatar="🤖"):
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(101):
                time.sleep(0.02)
                progress_bar.progress(i)

            # Typing indicator
            st.text("Thinking...")
            for i in range(4):
                time.sleep(0.2)
                st.text("Thinking" + "." * (i + 1))

            # Generate a response from the model
            response = model.generate_content(
                prompt, stream=True
            )
            response.resolve()
            msg = response.text

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.text(msg)
