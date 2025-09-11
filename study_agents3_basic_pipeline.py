import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate

# --- Load API key ---
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- Text chunking ---
def chunk_text(text, chunk_size=8000, overlap=1000):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)

# --- Summarize a chunk ---
def summarize_chunk(chunk):
    prompt = ChatPromptTemplate.from_template(
        "You are an expert summarizer. Summarize this text chunk clearly:\n\n{text}"
    )
    messages = prompt.format_messages(text=chunk)
    return llm(messages).content

# --- Create study guide from all summaries ---
def synthesize_guide(summaries):
    joined = "\n\n---\n\n".join(summaries)
    prompt = ChatPromptTemplate.from_template(
        "You are a skilled academic writer. "
        "Synthesize the following summaries into a single, cohesive study guide in Markdown:\n\n{summaries}"
    )
    messages = prompt.format_messages(summaries=joined)
    return llm(messages).content

# --- Create quiz from final study guide ---
def create_quiz(study_guide):
    prompt = ChatPromptTemplate.from_template(
        "You are an expert exam writer. Based on the following study guide, "
        "write a 5-question multiple-choice quiz with answers at the end:\n\n{guide}"
    )
    messages = prompt.format_messages(guide=study_guide)
    return llm(messages).content

# --- Main pipeline ---
def create_study_material(text_content):
    chunks = chunk_text(text_content)
    
    # Step 1: Summarize each chunk
    summaries = [summarize_chunk(c) for c in chunks]
    
    # Step 2: Synthesize into guide
    study_guide = synthesize_guide(summaries)
    
    # Step 3: Generate quiz
    quiz = create_quiz(study_guide)
    
    return {
        "study_guide": study_guide,
        "quiz": quiz
    }
