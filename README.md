# YouNotes 📒

YouNotes is an agentic study assistant powered by Gemini AI. It allows you to turn any YouTube video or PDF into a study guide and quiz in seconds. The application uses advanced AI techniques to chunk, summarize, synthesize, and generate quizzes from the provided content.

---
DEPLOYED LINK : https://younotes.streamlit.app/
---

## Features
- **YouTube Transcript Extraction**: Extracts transcripts from YouTube videos and processes them into study materials.
- **PDF Text Extraction**: Extracts text from uploaded PDF files and converts them into study guides.
- **AI-Powered Summarization**: Summarizes large chunks of text into concise, readable summaries.
- **Study Guide Generation**: Synthesizes summaries into a cohesive study guide in Markdown format.
- **Quiz Creation**: Generates a 5-question multiple-choice quiz based on the study guide.

**Technology Stack**:
- **Python**: Core programming language(Python)
- **Streamlit**: Interactive web app framework.
- **LangChain**: Framework for building agentic AI workflows.
- **LangGraph**:For DAG and node creation.
- **Gemini AI**: Language model for text generation.
- **YouTube Transcript API**: Extracts transcripts from YouTube videos.
- **PyPDF2**: Extracts text from PDF files.


---

## Installation and Setup
Follow these simple steps to get started:

1. **Clone the Repository**:
Run the following commands in your terminal:
```bash
   git clone https://github.com/sharonn-madan/YouNotes
   cd YouNotes
```
2. **Set Up a Virtual Environment**:
Run the following commands in your terminal:
```bash
   python -m venv venv
   .\venv\Scripts\activate
```

3. **Install Dependencies**:
Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. **Set Up Environment Variables**: Create a .env file in the root directory and add your Gemini API key:
Install the required Python packages:
```bash
GOOGLE_API_KEY=your_google_api_key
```


### Run the Application
```bash
streamlit run app3.py
```

---

## Usage
**Provide Input**:
-YouTube Link: Paste a YouTube video URL to extract its transcript.
-PDF File: Upload a PDF file to extract its text.
**Generate Study Materials**:Click the "Build Study Guide & Quiz" button to generate the study guide and quiz.
**View Results**:The study guide and quiz will appear in their respective sections.

---

## How It Works
1.**Text Extraction**:
-YouTube transcripts are fetched using the youtube_transcript_api.
-PDF text is extracted using PyPDF2.
2.**Agentic Workflow**:
-The study_agents3.py file defines an agentic workflow using LangChain and LangGraph.
-The workflow includes nodes for chunking, summarizing, synthesizing, and quiz creation.
3.**Streamlit Interface**:
-The app provides an interactive interface for users to upload files or paste links.
-Results are displayed dynamically in the app.

---


## Known Issues
-**YouTube Transcript Errors**: Some videos may not have transcripts available.
-**Large PDFs**: Processing very large PDFs may take time or fail due to memory limits

---

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

Project Creators: 
Hemant Dubey - [gitHub Profile](https://github.com/frizzyfreak)
Sharon Madan - [GitHub Profile](https://github.com/sharonn-madan)

Project Link: [YouNotes](https://github.com/frizzyfreak/YouNotes)

---

Thank you for using YouNotes! 

