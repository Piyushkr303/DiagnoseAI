import os
import streamlit as st
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the GROQ API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Groq API Key is missing.")
    st.stop()  # Stop execution if key is missing

# Initialize the ChatGroq model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.2-1b-preview")

# Define prompts with contextual input
diagnosis_prompt = PromptTemplate(
    input_variables=["symptoms", "history"],
    template=(
        "Based on the previous conversation: {history}, "
        "the patient now presents with the following symptoms: {symptoms}. "
        "What are the possible diagnoses?"
    ),
)

treatment_prompt = PromptTemplate(
    input_variables=["diagnosis", "history"],
    template=(
        "Given the diagnosis: {diagnosis} and the patient's previous data: {history}, "
        "what are the recommended treatments?"
    ),
)

compatibility_prompt = PromptTemplate(
    input_variables=["treatments", "medical_history", "current_medications", "history"],
    template=(
        "From the previous context: {history}, the patient's medical history includes: {medical_history}. "
        "They are currently taking: {current_medications}. Are these treatments safe: {treatments}? "
        "Provide a compatibility check."
    ),
)

# Create Langchain LLMChains
diagnosis_chain = LLMChain(llm=llm, prompt=diagnosis_prompt)
treatment_chain = LLMChain(llm=llm, prompt=treatment_prompt)
compatibility_chain = LLMChain(llm=llm, prompt=compatibility_prompt)

# Store and maintain chat history
def update_history(history, new_message):
    return history + "\n" + new_message if history else new_message

# Define the workflow function
def healthcare_planner(symptoms, medical_history, current_medications, history=""):
    # Step 1: Generate diagnosis with history
    diagnosis = diagnosis_chain.run(symptoms=symptoms, history=history)
    new_history = update_history(history, f"Diagnosis: {diagnosis}")
    print(f"Diagnosis: {diagnosis}")

    # Step 2: Generate treatments based on diagnosis and history
    treatments = treatment_chain.run(diagnosis=diagnosis, history=new_history)
    new_history = update_history(new_history, f"Suggested Treatments: {treatments}")
    print(f"Suggested Treatments: {treatments}")

    # Step 3: Check compatibility with medical history and current medications
    compatibility = compatibility_chain.run(
        treatments=treatments,
        medical_history=medical_history,
        current_medications=current_medications,
        history=new_history,
    )
    new_history = update_history(new_history, f"Compatibility Check: {compatibility}")
    print(f"Compatibility Check: {compatibility}")

    return diagnosis, treatments, compatibility, new_history

# Streamlit UI
st.title('Healthcare Diagnosis and Treatment Planner')

# Initialize or load chat history
if "history" not in st.session_state:
    st.session_state.history = ""

# Input fields for user data
symptoms = st.text_input('Enter Symptoms')
medical_history = st.text_input('Enter Medical History')
current_medications = st.text_input('Enter Current Medications')

if st.button('Get Diagnosis and Treatment Plan'):
    # Call the healthcare planner with the session's history
    diagnosis, treatments, compatibility, updated_history = healthcare_planner(
        symptoms, medical_history, current_medications, st.session_state.history
    )
    
    # Update the session's history
    st.session_state.history = updated_history

    # Display results
    st.write(f"Diagnosis: {diagnosis}")
    st.write(f"Suggested Treatments: {treatments}")
    st.write(f"Compatibility Check: {compatibility}")
