---
title: DoctorDemma
emoji: 👀
colorFrom: yellow
colorTo: blue
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


Here’s a **README** file for your healthcare diagnosis and treatment planner project:

---

# **Healthcare Diagnosis and Treatment Planner**

This project is a healthcare application that utilizes multiple AI agents to analyze symptoms, medical history, lab reports, and external knowledge sources (Wikipedia and arXiv) to provide a diagnosis, suggest treatments, and check the compatibility of medications. The app is built using **Streamlit** for the user interface and **LangChain** to manage interactions between the AI models.

## **Features**
- **Symptom Analysis**: Input symptoms and receive a possible diagnosis based on AI models.
- **Lab Report Analysis**: Upload a PDF lab report, and the app will extract and summarize the key findings.
- **Wikipedia and arXiv Summaries**: Fetch relevant information from Wikipedia and arXiv research papers based on the symptoms provided.
- **Treatment Suggestions**: Based on the diagnosis and medical history, the app suggests treatment options.
- **Medication Compatibility Check**: The app checks the compatibility of the suggested treatments with the patient's current medications and medical history.

## **Technologies Used**
- **Python**
- **Streamlit**: For the web interface.
- **LangChain**: To manage prompts and agents for diagnosis, lab report analysis, and treatment suggestions.
- **ChatGroq**: For using an AI language model (e.g., Llama).
- **Wikipedia and ArXiv API Wrappers**: To fetch real-time data from external sources.
- **PyMuPDF**: To extract text from uploaded PDF lab reports.

## **Installation**

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/healthcare-diagnosis-app.git
cd healthcare-diagnosis-app
```

### 2. **Create a Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. **Install Required Packages**
```bash
pip install -r requirements.txt
```

### 4. **Set Up Environment Variables**
Create a `.env` file in the project directory and add your API keys:
```bash
GROQ_API_KEY=your_groq_api_key
```

### 5. **Run the App**
```bash
streamlit run app.py
```

## **Usage**

### 1. **Enter Symptoms**
- Input the patient's symptoms in the text box provided.

### 2. **Enter Medical History**
- Provide relevant medical history, such as chronic illnesses or previous diagnoses.

### 3. **Enter Current Medications**
- Input the medications the patient is currently taking.

### 4. **Upload a Lab Report (PDF)**
- Upload a PDF file containing the lab report for analysis.

### 5. **Get Diagnosis and Treatment Plan**
- After filling in the necessary fields and uploading the lab report, click the **"Get Diagnosis and Treatment Plan"** button. The app will:
  1. Analyze the lab report.
  2. Fetch external information from Wikipedia and arXiv.
  3. Generate a diagnosis.
  4. Suggest treatments.
  5. Check treatment compatibility with current medications.

### 6. **Visual Feedback**
- Spinners will appear to indicate the system's progress while interacting with various agents (lab report analysis, Wikipedia, arXiv, etc.).

## **Demo**

Add a link to the live demo of the app if you have deployed it on Streamlit Cloud or any other platform.

## **File Structure**
```bash
├── app.py                   # Main Streamlit application file
├── README.md                # Project documentation
├── requirements.txt         # Dependencies for the project
├── .env                     # Environment variables
└── utils.py                 # Utility functions (if any)
```

## **Dependencies**
- **Python 3.9+**
- **LangChain**: For prompt management and AI agent orchestration.
- **Streamlit**: Web framework to build and host the app.
- **PyMuPDF**: To extract content from PDF files.
- **WikipediaAPIWrapper** and **ArxivAPIWrapper**: For fetching data from Wikipedia and arXiv.
- **ChatGroq**: AI model for natural language processing tasks.

## **Future Improvements**
- **Expand Compatibility Checks**: Add more in-depth compatibility analysis for various treatment options.
- **Additional Data Sources**: Integrate more external data sources for more comprehensive information.
- **User Authentication**: Implement secure user authentication for personalized medical history and treatment plans.
- **Enhanced UI/UX**: Improve the user interface for better interaction and data visualization.

## **Contributing**
If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. Any contributions, issues, or suggestions are welcome!

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Let me know if you'd like to customize any section further!
