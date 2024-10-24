import os
import streamlit as st
import PyPDF2  # Replacing fitz with PyPDF2 for PDF reading
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the GROQ API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Groq API Key is missing.")
    st.stop()

# Initialize the ChatGroq model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.2-1b-preview")

# Initialize Wikipedia and arXiv API Wrappers
wiki_tool = WikipediaAPIWrapper()
arxiv_tool = ArxivAPIWrapper()

# Define Prompts
diagnosis_prompt = PromptTemplate(
    input_variables=["symptoms", "history", "lab_report", "wiki_summary", "arxiv_summary"],
    template=(
        "Based on the previous conversation: {history}, "
        "the patient now presents with the following symptoms: {symptoms}. "
        "The following lab report details were provided: {lab_report}. "
        "In addition, a summary from Wikipedia: {wiki_summary} and from arXiv: {arxiv_summary}. "
        "What are the possible diagnoses?"
    ),
)

lab_analysis_prompt = PromptTemplate(
    input_variables=["lab_content"],
    template="Analyze the following lab report and summarize the key findings: {lab_content}"
)

treatment_prompt = PromptTemplate(
    input_variables=["diagnosis", "history"],
    template="Given the diagnosis: {diagnosis} and the patient's previous data: {history}, what are the recommended treatments?"
)

compatibility_prompt = PromptTemplate(
    input_variables=["treatments", "medical_history", "current_medications", "history"],
    template=(
        "From the previous context: {history}, the patient's medical history includes: {medical_history}. "
        "They are currently taking: {current_medications}. Are these treatments safe: {treatments}? "
        "Provide a compatibility check."
    ),
)

# LangChain Agents
diagnosis_chain = LLMChain(llm=llm, prompt=diagnosis_prompt)
lab_analysis_chain = LLMChain(llm=llm, prompt=lab_analysis_prompt)
treatment_chain = LLMChain(llm=llm, prompt=treatment_prompt)
compatibility_chain = LLMChain(llm=llm, prompt=compatibility_prompt)

def update_history(history, new_message):
    return history + "\n" + new_message if history else new_message

# Function to extract text from uploaded PDF
def extract_pdf_content(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    content = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        content += page.extract_text()
    return content

# Fetch summaries from Wikipedia and arXiv
def fetch_external_summaries(symptoms):
    with st.spinner("Fetching information from Wikipedia..."):
        wiki_summary = wiki_tool.run(symptoms)  # Query Wikipedia
    with st.spinner("Fetching information from arXiv..."):
        arxiv_summary = arxiv_tool.run(symptoms)  # Query arXiv
    return wiki_summary, arxiv_summary

# Main Healthcare Workflow Function
def healthcare_planner(symptoms, medical_history, current_medications, lab_report_content="", history=""):
    # Step 1: Lab Report Analysis
    with st.spinner("Analyzing the lab report..."):
        lab_summary = lab_analysis_chain.run(lab_content=lab_report_content)
    new_history = update_history(history, f"Lab Report Summary: {lab_summary}")
    st.write(f"Lab Report Summary: {lab_summary}")

    # Step 2: Fetch Wikipedia and arXiv summaries
    wiki_summary, arxiv_summary = fetch_external_summaries(symptoms)
    new_history = update_history(new_history, f"Wikipedia Summary: {wiki_summary}")
    new_history = update_history(new_history, f"arXiv Summary: {arxiv_summary}")
    st.write(f"Wikipedia Summary: {wiki_summary}")
    st.write(f"arXiv Summary: {arxiv_summary}")

    # Step 3: Generate Diagnosis
    with st.spinner("Generating diagnosis..."):
        diagnosis = diagnosis_chain.run(
            symptoms=symptoms, 
            history=new_history, 
            lab_report=lab_summary, 
            wiki_summary=wiki_summary, 
            arxiv_summary=arxiv_summary
        )
    new_history = update_history(new_history, f"Diagnosis: {diagnosis}")
    st.write(f"Diagnosis: {diagnosis}")

    # Step 4: Generate Treatments
    with st.spinner("Recommending treatments..."):
        treatments = treatment_chain.run(diagnosis=diagnosis, history=new_history)
    new_history = update_history(new_history, f"Suggested Treatments: {treatments}")
    st.write(f"Suggested Treatments: {treatments}")

    # Step 5: Compatibility Check
    with st.spinner("Checking treatment compatibility..."):
        compatibility = compatibility_chain.run(
            treatments=treatments,
            medical_history=medical_history,
            current_medications=current_medications,
            history=new_history,
        )
    new_history = update_history(new_history, f"Compatibility Check: {compatibility}")
    st.write(f"Compatibility Check: {compatibility}")

    return diagnosis, treatments, compatibility, new_history

# Streamlit UI
st.title('Healthcare Diagnosis and Treatment Planner')

if "history" not in st.session_state:
    st.session_state.history = ""

# User Input
symptoms = st.text_input('Enter Symptoms')
medical_history = st.text_input('Enter Medical History')
current_medications = st.text_input('Enter Current Medications')

# Lab Report Upload
uploaded_file = st.file_uploader("Upload Lab Report (PDF)", type="pdf")

lab_report_content = ""
if uploaded_file is not None:
    lab_report_content = extract_pdf_content(uploaded_file)
    st.write("Lab Report Content:")
    st.text(lab_report_content)

if st.button('Get Diagnosis and Treatment Plan'):
    diagnosis, treatments, compatibility, updated_history = healthcare_planner(
        symptoms, medical_history, current_medications, lab_report_content, st.session_state.history
    )
    
    # Update session history
    st.session_state.history = updated_history

    # Display Results
    st.write(f"Diagnosis: {diagnosis}")
    st.write(f"Suggested Treatments: {treatments}")
    st.write(f"Compatibility Check: {compatibility}")
