# chatbot_workflow.py
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[List, add_messages]

embeddings = OpenAIEmbeddings()
db = FAISS.load_local("vectorstore", embeddings)
retriever = db.as_retriever()
llm = ChatOpenAI(temperature=0.3)

def retrieve_and_respond(state: State) -> State:
    question = state["messages"][-1].content
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    answer = chain.run(question)
    state["messages"].append(AIMessage(content=answer))
    return state

graph = StateGraph(State)
graph.add_node("answer", retrieve_and_respond)
graph.set_entry_point("answer")
graph.set_finish_point("answer")
app = graph.compile()
