import os 
os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY'

import streamlit as st 
from langchain.llms import OpenAI
from langchain import PromptTemplate, HuggingFaceHub
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

# App framework
st.title('😁🔗 Presentation Generator')
prompt = st.text_input('Plug in your subject here') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write me a presentation title about {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a presentation script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# GPT model
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(prompt=title_template, verbose=True, output_key='title', llm=llm, memory=title_memory)
script_chain = LLMChain(prompt=script_template, verbose=True, output_key='script', llm=llm, memory=script_memory)

# Wikipedia
wiki = WikipediaAPIWrapper()

# Show results
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(script) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
