from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,HumanMessage

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

model = ChatOpenAI()

def chat_node(state : ChatState) :

    messages = state['messages']

    response = model.invoke(messages)

    return {'messages' : [response]}

#  Checkpointer

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)