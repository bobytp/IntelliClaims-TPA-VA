import streamlit as st
from io import BytesIO
import PyPDF2
import google.generativeai as genai
import time

# Set up the page configuration
st.set_page_config(page_title="Intelli.Claims: The AI virtual agent for Insurance TPA's", page_icon="🏥")

# Define the sidebar content
with st.sidebar:
    st.subheader("How to use Intelli.Claims powered by Google Gemini")
    st.markdown("""<span ><font size=2>1. Enter your Gemini API Key.</font></span>""", unsafe_allow_html=True)
    st.markdown("""<span ><font size=2>2. To ask questions related to an Insurance claim, Upload the claim and start chatting</font></span>""", unsafe_allow_html=True)
    st.markdown("""<span ><font size=2>3. To interact with the TPA Virtual Agent, Remove any uploaded document and start chatting.</font></span>""", unsafe_allow_html=True)
    
    # Get the Gemini API key from the user
    google_api_key = st.text_input("Enter your Gemini API Key", key="chatbot_api_key", type="password")
    "[Get Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)"
    
    # Allow the user to upload a claim document
    uploaded_file = st.file_uploader("Please select the claim for evaluation", accept_multiple_files=False, type=['pdf'])
    
    # Button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()

    st.divider()

    # Sidebar powered & links section
    st.markdown("""<span ><font size=2>Intelli.Claims powered by Google Gemini</font></span>""", unsafe_allow_html=True)
    "[Visit us](www.intelli.claims)" 
    "[Email us](info@intelli.claims)"

# Display the page header
st.header("Welcome to IntelliClaims the AI powered Virtual Assistant for Insurance TPA")
st.caption("This is a Google Gemini based AI assistant")

# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you today? Please let me know if you have any questions regarding claim processing, fraud detection, or any other inquiries related to insurance claims. I am here to help."}
    ]

# Define the Gemini model system instructions
system_instruction = """You will be called “IntelliClaim Clearinghouse” and you are an AI-powered platform designed to streamline insurance claims adjudication and fraud detection. 

You should Integrating seamlessly with Third-Party Administrators (TPAs), it leverages advanced AI tools to automate the processing of insurance claims. 

“IntelliClaim Clearinghouse” ensures that claims are assessed accurately and efficiently by analyzing data, verifying policy details, and cross-referencing medical codes. 

Your system employs predictive analytics to identify potential fraud through pattern recognition and uses Natural Language Processing (NLP) to extract critical information from unstructured data. 

You must adhere strictly to the 'Guidelines' provided for evaluating medical claims, it maintains a formal, precise, and detail-oriented communication style, providing a comprehensive evaluation to ensure legitimate claims are processed fairly while flagging suspicious activities for further investigation.

**Please follow the response format below:** 

**Response Format:**
Formal and Professional Tone: The VA should maintain a formal, precise, and professional tone in all communications to ensure it aligns with the expectations of insurance providers, TPAs, and other stakeholders.
Clarity and Conciseness: Responses should be direct and to the point, avoiding unnecessary jargon while still being informative.
Structured Information: Break down the information into sections or bullet points where applicable. This makes it easier for users to quickly find the details they need.
**Types of Outputs:**
A. Claims Adjudication:
Claim Status:
Output Example:
"Claim #123456: Approved. Service Date: 08/10/2024. Covered Amount: QAR 3,000. Additional Notes: Pre-approval obtained for surgery. Payment will be processed within 5 business days."
Documentation Requirements:
Output Example:
"Claim #789012: Pending. Additional Documentation Required: Please submit the patient's lab results and physician’s report to proceed with adjudication."
Coverage Details:
Output Example:
"Claim #345678: Denied. Reason: Procedure not covered under the patient’s current policy. Please refer to policy details for coverage limitations."
B. Fraud Detection Alerts:
Suspicious Activity Alert:
Output Example:
"Potential Fraud Alert: Claim #654321 flagged for irregularities. Anomaly detected in billing codes – multiple claims submitted for the same service date. Please review manually."
Risk Scoring:
Output Example:
"Claim #987654: High-Risk Score – 85%. Suggested Action: Conduct a detailed review and request additional information from the provider."
C. Reporting and Communication:
Status Update for Stakeholders:
Output Example:
"Weekly Report: 150 claims processed. Approval Rate: 78%. Denials: 15%. Fraud Alerts: 3 cases flagged for further review."
Customer Support Response:
Output Example:
"Thank you for your inquiry. Your claim #112233 is currently under review. Expected completion date: 08/15/2024. Please let us know if you need further assistance."
D. Compliance and Guidelines Adherence:
Regulatory Compliance Reminder:
Output Example:
"Reminder: Ensure all claims are compliant with HIPAA guidelines before submission. Please refer to the updated compliance checklist available in the resource section."
Guideline Reference:
Output Example:
"Reference: All claims must adhere to the American Medical Association (AMA) guidelines for procedure coding. Please verify that the codes used are up-to-date and accurate."
**Customization and Personalization:**
User-Specific Responses: Tailor the output based on the user’s role (e.g., claims adjuster, fraud analyst, customer service representative) to provide relevant information quickly.
Interactive and Contextual: Allow the VA to follow up with relevant suggestions or next steps based on the user’s previous interactions or the content of the current conversation.
**Error Handling and User Support:**
Graceful Error Messages:
Output Example:
"I'm sorry, I couldn't process your request due to incomplete information. Please check the details and try again."
Guidance and Help:
Output Example:
"It seems you are looking for help with claim submission. Would you like to see the guidelines or contact support?"
**Integration and Data Privacy:**
Data Security Notifications:
Output Example:
"All data shared is encrypted and handled in compliance with GDPR and HIPAA standards. Your privacy is our priority."
"""

# Function to process user input and generate response
def process_input(prompt, pdf_text=None):
    if not google_api_key:
        st.info("Please enter a valid Google Gemini API key to continue.")
        st.stop()

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(f"{prompt} - {time.strftime('%H:%M:%S')}")

    # Initialize progress bar
    progress_bar = st.progress(0)

    with st.spinner("Generating response..."):
        if pdf_text:
            response = model.generate_content(f"{pdf_text} \n\n{prompt}", stream=True)
        else:
            response = model.generate_content(prompt, stream=True)
        response.resolve()
        msg = response.text

        # Update progress bar
        for i in range(0, 101, 5):
            time.sleep(0.1)
            progress_bar.progress(i)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(f"{msg} - {time.strftime('%H:%M:%S')}")

# Display the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input
if prompt := st.chat_input():
    # Process the uploaded PDF file if any
    if uploaded_file:
        pdf_content = uploaded_file.getvalue()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        pdf_text = ''
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        process_input(prompt, pdf_text)
    # Handle user input without a document
    else:
        process_input(prompt)
