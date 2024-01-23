import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st
from pydantic import BaseModel
from typing import Type
from tools import search, ScrapeWebsiteTool
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import SystemMessage

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

llm = ChatOpenAI(model_name='gpt-4-1106-preview')

tools = [
    Tool(name="Search", func=search, description="Answer questions using current events/data. Be specific."),
    ScrapeWebsiteTool(),
]

system_message_content = """..."""

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": SystemMessage(content=system_message_content),
}

memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=False,
    max_iterations=5,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Fall Intern", page_icon=":bird:")
    st.header(":globe_with_meridians: Fall Intern")
    st.subheader('Go deeper on topics and questions.')
    query = st.text_input("Research goal")
    st.sidebar.title('About the app')
    st.sidebar.markdown("Fall Intern is a research assistant that will answer your query by searching, scraping and summmarizing real time results from across the web and return a cogent document with citations.")

    if query:
        with st.spinner("Researching..."):
            result = agent({"input": query})
        st.info(result['output'])

if __name__ == '__main__':
     main()