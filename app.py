import streamlit as st
from io import BytesIO
import PyPDF2
import google.generativeai as genai
import json
import time
from streamlit_lottie import st_lottie  # Import the library here
from streamlit_lottie import st_lottie_spinner

# Set up the page configuration
st.set_page_config(
    page_title="Intelli.Claims: The AI virtual agent for Insurance TPA's",
    page_icon="🏥",
    layout="wide",
)

# Initialize user profile globally
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {"preferred_format": "Structured"}

# Function to search chat history (define outside the sidebar)
def search_chat_history(query):
    """Searches the chat history for conversations containing the query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of matching chat history entries.
    """
    matches = []
    for entry in st.session_state.chat_history:
        if query.lower() in entry["content"].lower() or query.lower() in entry[
            "response"
        ].lower():
            matches.append(entry)
    return matches


# Define the sidebar content
with st.sidebar:
    st.subheader("How to use Intelli.Claims powered by Google Gemini")
    st.markdown(
        """<span ><font size=2>1. Enter your Gemini API Key.</font></span>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<span ><font size=2>2. To ask questions related to an Insurance claim, Upload the claim and start chatting</font></span>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<span ><font size=2>3. To interact with the TPA Virtual Agent, Remove any uploaded document and start chatting.</font></span>""",
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
        st.session_state.chat_history.clear()  # Clear chat history
        st.session_state.claim_status = {}  # Clear claim status

    st.divider()

    # Sidebar powered & links section
    st.markdown(
        """<span ><font size=2>Intelli.Claims powered by Google Gemini</font></span>""",
        unsafe_allow_html=True,
    )
    "[Visit us](www.intelli.claims)"
    "[Email us](info@intelli.claims)"

    # Search chat history
    st.subheader("Search Chat History")
    search_query = st.text_input("Enter your search query")
    if search_query:
        matches = search_chat_history(search_query)  # Now search_chat_history is accessible
        if matches:
            st.subheader("Matching Conversations")
            for entry in matches:
                st.write(f"**User:** {entry['content']}")
                st.write(f"**Assistant:** {entry['response']}")
        else:
            st.info("No matching conversations found.")

    # User profile
    st.subheader("User Profile")
    preferred_format_options = ("Structured", "Bullet Points", "Conversation")
    preferred_format_index = preferred_format_options.index(
        st.session_state.user_profile.get("preferred_format", preferred_format_options[0])
    )
