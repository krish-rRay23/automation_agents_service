from langgraph.graph import StateGraph, END
from typing import TypedDict

# Step 1: Define the state schema
class AgentState(TypedDict):
    input: str

# Step 2: Build the graph
builder = StateGraph(AgentState)

# Step 3: Define agent node functions
def scraper_agent(state):
    print("Scraper Agent running...")
    return {"input": f"Scraped: {state['input']}"}

def summarizer_agent(state):
    print("Summarizer Agent running...")
    return {"input": f"Summarized: {state['input']}"}

def emailer_agent(state):
    print("Emailer Agent running...")
    return {"input": f"Emailed: {state['input']}"}

# Step 4: Add nodes to the graph
builder.add_node("scraper", scraper_agent)
builder.add_node("summarizer", summarizer_agent)
builder.add_node("emailer", emailer_agent)

# Step 5: Define workflow sequence
builder.set_entry_point("scraper")
builder.add_edge("scraper", "summarizer")
builder.add_edge("summarizer", "emailer")
builder.add_edge("emailer", END)

# Step 6: Compile the graph
graph = builder.compile()

# Step 7: Run the graph
result = graph.invoke({"input": "Start task"})

print("\nFinal Result:")
print(result)
