import streamlit as st
from content_extractor3 import get_youtube_transcript, get_pdf_text
# from study_agents import create_study_crew
from study_agents3 import create_study_material
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="YouNotes",
    page_icon="📒",
    layout="wide"
)

# --- Custom CSS for Styling ---
# This CSS will help us create the card-like appearance and match the screenshot's style.
st.markdown("""
<style>
    /* Card-like containers created with st.container(border=True) have a default padding.
       We can adjust it if needed, but the default is often good for adapting to themes. */
    
    /* Style for buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #007BFF;
        background-color: #007BFF;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
        border: 1px solid #0056b3;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        padding: 10px;
    }
    /* In dark mode, the selected tab might need a different color for better contrast */
    [data-theme="dark"] .stTabs [aria-selected="true"] {
         background-color: #2F3136; /* A slightly off-black for dark mode */
    }
    [data-theme="light"] .stTabs [aria-selected="true"] {
         background-color: #E0E0E0;
    }

</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if 'generated_materials' not in st.session_state:
    st.session_state.generated_materials = None
if 'agent_log' not in st.session_state:
    st.session_state.agent_log = "Progress will appear here."
if 'error' not in st.session_state:
    st.session_state.error = None

st.markdown("""
    <style>
        div.block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("📒YouNotes")
st.markdown("Agentic study assistant powered by Gemini—turn any YouTube link or PDF into study notes and a quiz in seconds.")


# --- Main Layout (2x2 Grid) ---
col1, col2 = st.columns(2, gap="large")

# --- Top Row ---
with col1:
    # Using st.container(border=True) for a theme-adaptive card effect
    with st.container(border=True):
        st.subheader("Sources")
        st.markdown("Provide a YouTube link or a PDF to build your study guide.")
        
        input_tab1, input_tab2 = st.tabs(["🔗 Link", "📄 PDF"])
        source_content = ""

        with input_tab1:
            youtube_url = st.text_input("YouTube URL", placeholder="https://...", label_visibility="collapsed")
            if youtube_url:
                with st.spinner("Fetching transcript..."):
                    transcript, err = get_youtube_transcript(youtube_url)
                    if transcript:
                        source_content = transcript
                    else:
                        st.session_state.error = err or "Transcript not found."
            
        with input_tab2:
            MAX_FILE_SIZE_MB = 25
            uploaded_file = st.file_uploader(
                "Upload a PDF", 
                type="pdf",
                label_visibility="collapsed",
                help=f"Max file size: {MAX_FILE_SIZE_MB} MB"
            )
            if uploaded_file:
                if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                    st.session_state.error = f"File exceeds {MAX_FILE_SIZE_MB}MB limit."
                else:
                    with st.spinner("Extracting text..."):
                        text = get_pdf_text(uploaded_file)
                        if err: st.session_state.error = err
                        else: source_content = text

        generate_button = st.button("Build Study Guide & Quiz")

with col2:
     with st.container(border=True):
        st.subheader("Agent Log")
        # The log will be updated dynamically via the placeholder
        log_placeholder = st.empty()
        log_placeholder.info(st.session_state.agent_log, icon="🤖")

# --- Bottom Row ---
with col1:
     with st.container(border=True):
        st.subheader("Study Guide")
        guide_placeholder = st.empty()
        if st.session_state.generated_materials:
            guide_placeholder.markdown(st.session_state.generated_materials['study_guide'])
        else:
            guide_placeholder.info("Your study guide will appear here after processing.")

with col2:
     with st.container(border=True):
        st.subheader("Quiz")
        quiz_placeholder = st.empty()
        if st.session_state.generated_materials:
            quiz_placeholder.markdown(st.session_state.generated_materials['quiz'])
        else:
            quiz_placeholder.info("Your practice questions will appear here.")


# --- Generation Logic ---
if st.session_state.error:
    st.error(f"An error occurred: {st.session_state.error}", icon="🚨")
    st.session_state.error = None # Clear the error after displaying

if generate_button:
    if not source_content:
        st.warning("Please provide a source (YouTube link or PDF) first.", icon="⚠️")
    else:
        # Clear previous results and logs
        st.session_state.generated_materials = None
        st.session_state.agent_log = "Agents are assembling... 🤖"
        log_placeholder.info(st.session_state.agent_log, icon="🤖")
        guide_placeholder.info("Your study guide will appear here after processing.")
        quiz_placeholder.info("Your practice questions will appear here.")

        try:
            # A simple way to show progress updates
            time.sleep(1)
            st.session_state.agent_log = "Analyzing text chunks... 📚"
            log_placeholder.info(st.session_state.agent_log, icon="🤖")

            # This is the long-running call to our AI crew
            results = create_study_material(source_content)
            
            st.session_state.agent_log = "Task complete! ✅"
            log_placeholder.success(st.session_state.agent_log, icon="🎉")
            st.session_state.generated_materials = results
            
            # Rerun the script to update the placeholders with the final content
            st.rerun()

        except Exception as e:
            st.session_state.agent_log = f"An error occurred during generation: {e}"
            log_placeholder.error(st.session_state.agent_log, icon="🔥")

