import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# --- Load API key ---
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- 1. Define the State for our Agent ---
# This is the "memory" of our agent. It holds all the data as it's processed.
class AgentState(TypedDict):
    text_content: str
    chunks: List[str]
    summaries: List[str]
    study_guide: str
    quiz: str

# --- 2. Define the Nodes (Tools) for our Agent ---
# Each function is a "tool" the agent can use. It takes the current state and returns an update.

def chunk_text_node(state: AgentState):
    """Chunks the initial text content."""
    print("---NODE: CHUNKING TEXT---")
    text_content = state["text_content"]
    splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=1000)
    chunks = splitter.split_text(text_content)
    return {"chunks": chunks}

def summarize_chunks_node(state: AgentState):
    """Summarizes each chunk of text."""
    print("---NODE: SUMMARIZING CHUNKS---")
    chunks = state["chunks"]
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert summarizer. Summarize this text chunk clearly:\n\n{text}"
    )
    summarize_chain = prompt | llm
    
    # Using invoke for single calls, or batch for parallel calls
    summaries = summarize_chain.batch( [{"text": chunk} for chunk in chunks] )
    # Extract the content from the AI message objects
    summary_contents = [summary.content for summary in summaries]
    
    return {"summaries": summary_contents}

def synthesize_guide_node(state: AgentState):
    """Synthesizes summaries into a study guide."""
    print("---NODE: SYNTHESIZING GUIDE---")
    summaries = state["summaries"]
    joined = "\n\n---\n\n".join(summaries)
    
    prompt = ChatPromptTemplate.from_template(
        "You are a skilled academic writer. "
        "Synthesize the following summaries into a single, cohesive study guide in Markdown:\n\n{summaries}"
    )
    synthesize_chain = prompt | llm
    study_guide = synthesize_chain.invoke({"summaries": joined}).content
    return {"study_guide": study_guide}

def create_quiz_node(state: AgentState):
    """Creates a quiz from the study guide."""
    print("---NODE: CREATING QUIZ---")
    study_guide = state["study_guide"]
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert exam writer. Based on the following study guide, "
        "write a 5-question multiple-choice quiz with answers at the end:\n\n{guide}"
    )
    quiz_chain = prompt | llm
    quiz = quiz_chain.invoke({"guide": study_guide}).content
    return {"quiz": quiz}

# --- 3. Define the Edges (Decision Logic) ---
# This function decides which node to run next. This is the "brain" of the agent.
def router(state: AgentState):
    """Decides the next step based on the current state."""
    print("---ROUTER: DECIDING NEXT STEP---")
    if not state.get("chunks"):
        return "chunk_text"
    if not state.get("summaries"):
        return "summarize_chunks"
    if not state.get("study_guide"):
        return "synthesize_guide"
    if not state.get("quiz"):
        return "create_quiz"
    return "end"

# --- 4. Build and Compile the Graph ---
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("chunk_text", chunk_text_node)
workflow.add_node("summarize_chunks", summarize_chunks_node)
workflow.add_node("synthesize_guide", synthesize_guide_node)
workflow.add_node("create_quiz", create_quiz_node)
# workflow.add_node("router", router)

# The entry point is the router
workflow.set_entry_point("chunk_text")

# Add conditional edges. The router's output determines the next node.
workflow.add_conditional_edges(
    # The "decider" is now called AFTER the chunking step
    "chunk_text",
    router,
    {
        # If the router says "summarize_chunks", go to that node
        "summarize_chunks": "summarize_chunks",
        # This path shouldn't be taken, but good to be explicit
        "end": END,
    },
)
workflow.add_conditional_edges(
    "summarize_chunks",
    router,
    {
        "synthesize_guide": "synthesize_guide",
        "end": END,
    },
)
workflow.add_conditional_edges(
    "synthesize_guide",
    router,
    {
        "create_quiz": "create_quiz",
        "end": END,
    },
)


# An edge to loop back to the router after each step
# workflow.add_edge("chunk_text", "router")
# workflow.add_edge("summarize_chunks", "router")
# workflow.add_edge("synthesize_guide", "router")
workflow.add_edge("create_quiz", END)

# Compile the graph into a runnable app
agentic_study_app = workflow.compile()

# --- Main pipeline function (now uses the agentic graph) ---
def create_study_material(text_content: str):
    """
    Runs the agentic graph to create study materials.
    """
    # The initial state to start the graph
    initial_state = {"text_content": text_content}
    
    # Invoke the graph and get the final state
    final_state = agentic_study_app.invoke(initial_state)
    
    return {
        "study_guide": final_state["study_guide"],
        "quiz": final_state["quiz"],
    }