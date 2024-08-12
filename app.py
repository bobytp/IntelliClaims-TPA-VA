import streamlit as st
from io import BytesIO
import PyPDF2
import google.generativeai as genai

# Set up the page configuration
st.set_page_config(
    page_title="Intelli.Claims: The AI virtual agent for Insurance TPA's",
    page_icon="🏥",
    layout="wide",  # Use wide layout for better visual presentation
)

# Define the sidebar content
with st.sidebar:
    st.subheader("Intelli.Claims powered by Google Gemini")
    st.markdown(
        """<span ><font size=2>Intelli.Claims is an AI-powered virtual assistant designed to streamline your insurance claims process. Here's how to use it:</font></span>""",
        unsafe_allow_html=True,
    )

    # Get the Gemini API key from the user
    google_api_key = st.text_input(
        "Enter your Gemini API Key",
        key="chatbot_api_key",
        type="password",
        placeholder="Paste your API key here",
    )
    st.markdown(
        "[Get Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)"
    )

    # Allow the user to upload a claim document
    uploaded_file = st.file_uploader(
        "Upload a Claim Document (PDF)",
        accept_multiple_files=False,
        type=["pdf"],
        help="Upload a claim document for AI-powered analysis.",
    )

    # Button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        st.session_state.conversation_context = ""  # Clear context

    st.divider()

    # Sidebar powered & links section
    st.markdown(
        """<span ><font size=2>Powered by Google Gemini</font></span>""",
        unsafe_allow_html=True,
    )
    "[Visit us](www.intelli.claims)"
    "[Email us](info@intelli.claims)"

# Display the page header
st.header("Welcome to IntelliClaims")
st.subheader("The AI powered Virtual Assistant for Insurance TPA")

# Initialize the chat history and conversation context if they don't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Welcome to IntelliClaim TPA Virtual Assistant! I'm ready to help you streamline your claims process. To get started, tell me about the claim you'd like to evaluate. If you'd like to submit a claim, upload the document for me to review.",
        }
    ]
if "conversation_context" not in st.session_state:
    st.session_state["conversation_context"] = ""

# Display the chat history in a more user-friendly format
st.chat_messages(st.session_state.messages)

# Process the uploaded PDF file if any
if uploaded_file:
    # Get the PDF content as bytes
    pdf_content = uploaded_file.getvalue()

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))

    # Extract text from all pages
    pdf_text = ''
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    # Create a container for the user input and response
    with st.container():
        # Use st.chat_input for a more interactive input field
        if prompt := st.chat_input("Ask me anything about the claim"):
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

            # Add user's prompt to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Show a spinner while processing the response
            with st.spinner("Processing your request..."):
                # Generate a response from the model
                response = model.generate_content(
                    f"{pdf_text} \n\n{prompt}", stream=True
                )
                response.resolve()
                msg = response.text

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

            # Update conversation context
            st.session_state.conversation_context += (
                f"\n\n**User:** {prompt}\n**Assistant:** {msg}"
            )

# If no file is uploaded, handle user interaction
else:
    # Create a container for the user input and response
    with st.container():
        # Use st.chat_input for a more interactive input field
        if prompt := st.chat_input("Ask me anything about claims"):
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

            # Add user's prompt to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Show a spinner while processing the response
            with st.spinner("Processing your request..."):
                # Generate a response from the model
                response = model.generate_content(
                    f"{st.session_state.conversation_context} \n\n{prompt}",
                    stream=True,
                )
                response.resolve()
                msg = response.text

            # Add assistant's response to chat history
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

            # Update conversation context
            st.session_state.conversation_context += (
                f"\n\n**User:** {prompt}\n**Assistant:** {msg}"
            )
