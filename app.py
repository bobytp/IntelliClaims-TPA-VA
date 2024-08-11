import streamlit as st
from io import BytesIO
import PyPDF2
import google.generativeai as genai
import json
import time
from streamlit_lottie import st_lottie
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


# Function to process user input and generate response
def process_input(prompt, pdf_text=None):
    """Processes user input and generates a response from the Gemini model.

    Args:
        prompt (str): The user's prompt.
        pdf_text (str, optional): The text extracted from the uploaded PDF. Defaults to None.

    Returns:
        str: The generated response from the model.
    """

    # Check if the API key is provided
    if not google_api_key:
        st.info("Please enter a valid Google Gemini API key to continue.")
        st.stop()

    # Configure the Google Gemini API
    genai.configure(api_key=google_api_key)

    # Create a Gemini model object
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You will be called “IntelliClaim Clearinghouse” and you are an AI-powered platform designed to streamline insurance claims adjudication and fraud detection. \n\nYou should Integrating seamlessly with Third-Party Administrators (TPAs), it leverages advanced AI tools to automate the processing of insurance claims. \n\n“IntelliClaim Clearinghouse” ensures that claims are assessed accurately and efficiently by analyzing data, verifying policy details, and cross-referencing medical codes. \n\nYour system employs predictive analytics to identify potential fraud through pattern recognition and uses Natural Language Processing (NLP) to extract critical information from unstructured data. \n\nYou must adhere strictly to the 'Guidelines' provided for evaluating medical claims, it maintains a formal, precise, and detail-oriented communication style, providing a comprehensive evaluation to ensure legitimate claims are processed fairly while flagging suspicious activities for further investigation.\n\n**Please follow the response format below:** \n\n**Response Format:**\nFormal and Professional Tone: The VA should maintain a formal, precise, and professional tone in all communications to ensure it aligns with the expectations of insurance providers, TPAs, and other stakeholders.\nClarity and Conciseness: Responses should be direct and to the point, avoiding unnecessary jargon while still being informative.\nStructured Information: Break down the information into sections or bullet points where applicable. This makes it easier for users to quickly find the details they need.\n**Types of Outputs:**\nA. Claims Adjudication:\nClaim Status:\nOutput Example:\n\"Claim #123456: Approved. Service Date: 08/10/2024. Covered Amount: QAR 3,000. Additional Notes: Pre-approval obtained for surgery. Payment will be processed within 5 business days.\"\nDocumentation Requirements:\nOutput Example:\n\"Claim #789012: Pending. Additional Documentation Required: Please submit the patient's lab results and physician’s report to proceed with adjudication.\"\nCoverage Details:\nOutput Example:\n\"Claim #345678: Denied. Reason: Procedure not covered under the patient’s current policy. Please refer to policy details for coverage limitations.\"\nB. Fraud Detection Alerts:\nSuspicious Activity Alert:\nOutput Example:\n\"Potential Fraud Alert: Claim #654321 flagged for irregularities. Anomaly detected in billing codes – multiple claims submitted for the same service date. Please review manually.\"\nRisk Scoring:\nOutput Example:\n\"Claim #987654: High-Risk Score – 85%. Suggested Action: Conduct a detailed review and request additional information from the provider.\"\nC. Reporting and Communication:\nStatus Update for Stakeholders:\nOutput Example:\n\"Weekly Report: 150 claims processed. Approval Rate: 78%. Denials: 15%. Fraud Alerts: 3 cases flagged for further review.\"\nCustomer Support Response:\nOutput Example:\n\"Thank you for your inquiry. Your claim #112233 is currently under review. Expected completion date: 08/15/2024. Please let us know if you need further assistance.\"\nD. Compliance and Guidelines Adherence:\nRegulatory Compliance Reminder:\nOutput Example:\n\"Reminder: Ensure all claims are compliant with HIPAA guidelines before submission. Please refer to the updated compliance checklist available in the resource section.\"\nGuideline Reference:\nOutput Example:\n\"Reference: All claims must adhere to the American Medical Association (AMA) guidelines for procedure coding. Please verify that the codes used are up-to-date and accurate.\"\n**Customization and Personalization:**\nUser-Specific Responses: Tailor the output based on the user’s role (e.g., claims adjuster, fraud analyst, customer service representative) to provide relevant information quickly.\nInteractive and Contextual: Allow the VA to follow up with relevant suggestions or next steps based on the user’s previous interactions or the content of the current conversation.\n**Error Handling and User Support:**\nGraceful Error Messages:\nOutput Example:\n\"I'm sorry, I couldn't process your request due to incomplete information. Please check the details and try again.\"\nGuidance and Help:\nOutput Example:\n\"It seems you are looking for help with claim submission. Would you like to see the guidelines or contact support?\"\n**Integration and Data Privacy:**\nData Security Notifications:\nOutput Example:\n\"All data shared is encrypted and handled in compliance with GDPR and HIPAA standards. Your privacy is our priority.\"\n"
    )

    time.sleep(1)  # Simulate processing time
    if pdf_text:
        response = model.generate_content(f"{pdf_text} \n\n{prompt}", stream=True)
    else:
        response = model.generate_content(prompt, stream=True)
    response.resolve()
    return response.text


# Function to handle claim status tracking
def update_claim_status(claim_id, status, notes=""):
    """Updates the claim status in the session state.

    Args:
        claim_id (str): The claim ID.
        status (str): The new status of the claim (e.g., "Approved", "Pending", "Denied").
        notes (str, optional): Additional notes about the claim status. Defaults to "".
    """
    st.session_state.claim_status[claim_id] = {
        "status": status,
        "notes": notes,
    }


# Function to display claim status
def display_claim_status():
    """Displays the claim status in a table format."""
    if st.session_state.claim_status:
        st.subheader("Claim Status")
        st.table(st.session_state.claim_status)
    else:
        st.info("No claim status information available.")

# Display the chat history
st.subheader("Conversation History")
for msg in st.session_state.messages:
    with st.container():
        st.markdown(
            f"""<span style='font-size: 14px; color: gray; font-style: italic;'>{time.strftime('%Y-%m-%d %H:%M:%S')}</span>""",
            unsafe_allow_html=True,
        )
        st.chat_message(msg["role"]).write(msg["content"])

# Create the chat input widget (with unique key)
chat_input = st.chat_input(key="chat_input")

# ------------------------------------------------------------
# Move these sections to the main screen
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
# ------------------------------------------------------------

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

    # Get the user's prompt from the chat input (using the same widget)
    if prompt := chat_input:  # Use the same chat_input widget
        # Add user's prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Display the spinner
        is_spinning = True
        st_lottie_spinner(lottie_url="https://assets8.lottiefiles.com/packages/lf20_4g61y05l.json")  # Call the spinner outside the function
        time.sleep(1) # simulate some processing time
        # Generate a response from the model
        msg = process_input(prompt, pdf_text)
        
        # Hide the spinner - we don't need to do this, as soon as the function returns, the spinner will disappear
        is_spinning = False
        st_lottie_spinner(lottie_url="https://assets8.lottiefiles.com/packages/lf20_4g61y05l.json")  # Call the spinner outside the function

        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # Extract claim information from the response (example)
        if "Claim #" in msg:
            claim_id = msg.split("Claim #")[1].split(":")[0].strip()
            update_claim_status(
                claim_id, "Pending", notes="Claim submitted for review"
            )
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt, "response": msg}
            )

# If no file is uploaded, handle user interaction
else:
    # Get the user's prompt from the chat input (using the same widget)
    if prompt := chat_input:  # Use the same chat_input widget
        # Add user's prompt to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Display the spinner
        is_spinning = True
        st_lottie_spinner(lottie_url="https://assets8.lottiefiles.com/packages/lf20_4g61y05l.json")  # Call the spinner outside the function
        time.sleep(1) # simulate some processing time
        # Generate a response from the model
        msg = process_input(prompt)

        # Hide the spinner - we don't need to do this, as soon as the function returns, the spinner will disappear
        is_spinning = False
        st_lottie_spinner(lottie_url="https://assets8.lottiefiles.com/packages/lf20_4g61y05l.json")  # Call the spinner outside the function

        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

        # Store chat history for future reference
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt, "response": msg}
        )

# Display claim status
display_claim_status()

# ------------------------------------------------------------
#  Search Chat History and User Profile
# ------------------------------------------------------------
st.subheader("Search Chat History and User Profile")
options = st.selectbox(
    "Select Option", ["Search Chat History", "User Profile"]
)

if options == "Search Chat History":
    st.subheader("Search Chat History")
    search_query = st.text_input("Enter your search query")
    if search_query:
        matches = search_chat_history(search_query)
        if matches:
            st.subheader("Matching Conversations")
            for entry in matches:
                st.write(f"**User:** {entry['content']}")
                st.write(f"**Assistant:** {entry['response']}")
        else:
            st.info("No matching conversations found.")

elif options == "User Profile":
    st.subheader("User Profile")
    preferred_format_options = ("Structured", "Bullet Points", "Conversation")
    preferred_format_index = preferred_format_options.index(
        st.session_state.user_profile.get("preferred_format", preferred_format_options[0])
    )
    preferred_format = st.selectbox(
        "Preferred Response Format",
        preferred_format_options,
        index=preferred_format_index,
    )
    st.session_state.user_profile["preferred_format"] = preferred_format

    # Save user profile to a file
    with open("user_profile.json", "w") as f:
        json.dump(st.session_state.user_profile, f)
# ------------------------------------------------------------


# Error handling
try:
    # Code to generate response and handle claim status (from previous sections)
    if uploaded_file:
        # Get the PDF content as bytes
        pdf_content = uploaded_file.getvalue()

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))

        # Extract text from all pages
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        # Get the user's prompt from the chat input (with unique key)
        if prompt := chat_input:  # Use the same chat_input widget
            # Add user's prompt to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Generate a response from the model
            msg = process_input(prompt, pdf_text)

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

            # Extract claim information from the response (example)
            if "Claim #" in msg:
                claim_id = msg.split("Claim #")[1].split(":")[0].strip()
                update_claim_status(
                    claim_id, "Pending", notes="Claim submitted for review"
                )
                st.session_state.chat_history.append(
                    {"role": "user", "content": prompt, "response": msg}
                )
    else:
        # Get the user's prompt from the chat input (using the same widget)
        if prompt := chat_input:  # Use the same chat_input widget
            # Add user's prompt to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Generate a response from the model
            msg = process_input(prompt)

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

            # Store chat history for future reference
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt, "response": msg}
            )

except Exception as e:
    st.error(f"An error occurred: {e}")

    # Log error to a file (optional)
    with open("error.log", "a") as f:
        f.write(f"Error: {e}\n")
