import os
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain import load_qa_with_sources_chain
from dotenv import load_dotenv
from typing import List
import asyncio
from langchain.chains import Chain
from langchain import LLMStep

# Get the OpenAI API key from Heroku config vars
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Function to update the progress bar and fetch Wikipedia research
def get_wiki_research(topic, progress):
    wiki_research = wiki.run(topic)
    progress_bar.progress(progress)
    return wiki_research

async def get_relevant_documents(query: str) -> List[str]:
    # Call the Langchain API to get relevant documents
    # TODO: replace with actual API call
    return ["Document 1", "Document 2", "Document 3"]

# App framework
st.title('🦷 Perio & Implant dentistry Presentation Creator')
with st.form(key='my_form'):
    main_topic = st.text_input('Enter the main topic')
    subtopic = st.text_input('Enter the subtopic')
    duration = st.text_input('Enter the duration of the presentation')
    audience = st.text_input('Enter the audience for the presentation')

    # Temperature options
    temperature_options = {
        0: {'label': 'Daniel Rodrigo Mode', 'value': 0.2},
        1: {'label': 'Leticia Sala Mode', 'value': 0.5},
        2: {'label': 'Robles Mode', 'value': 0.9}
    }
    selected_temperature = st.slider('Select the temperature mode', min_value=0, max_value=2, format="%d")
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Validation
    if not main_topic or not subtopic or not duration.isdigit() or not audience:
        st.error("Please fill in all the fields correctly.")
    else:
        temperature = temperature_options[selected_temperature]['value']

        # Initialize the OpenAI API with the API key from Heroku config vars
        llm = OpenAI(api_key=openai_api_key, temperature=temperature)

        # Prompt templates
        title_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic', 'duration', 'audience'], 
            template='Write me a presentation title about {main_topic} and provide some details about the {subtopic} for a {duration}-minute presentation for {audience}.'
        )

        intro_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Write an engaging introduction about {main_topic} and provide some details about the {subtopic}.'
        )

        overview_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Provide an overview of the topics to be covered in the presentation on {main_topic} and {subtopic}.'
        )

        topic_slide_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic', 'wikipedia_research'],
            template='Create a slide about {main_topic} and {subtopic} based on this research: {wikipedia_research}.'
        )

        conclusion_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Write a compelling conclusion for a presentation on {main_topic} and {subtopic}.'
        )



   # Memory 
memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')

# GPT model
llm = OpenAI(temperature=0.5)

title_chain = Chain([
    get_relevant_documents,
    LLMStep(llm, prompt=title_template)
], memory=memory)

intro_chain = Chain([
    get_relevant_documents,
    LLMStep(llm, prompt=intro_template)
], memory=memory)

overview_chain = Chain([
    get_relevant_documents,
    LLMStep(llm, prompt=overview_template)
], memory=memory)

topic_slide_chain = Chain([
    get_relevant_documents,
    LLMStep(llm, prompt=topic_slide_template)
], memory=memory)

conclusion_chain = Chain([
    get_relevant_documents,
    LLMStep(llm, prompt=conclusion_template)
], memory=memory)

# Initialize Wikipedia API wrapper
wiki = WikipediaAPIWrapper()

# Progress bar
progress_bar = st.progress(0)
progress = 0.1
progress_bar.progress(progress)

# Fetch Wikipedia research for each of the topics and update the progress bar
main_topic_research = get_wiki_research(main_topic, progress)
progress += 0.1

subtopic_research = get_wiki_research(subtopic, progress)
progress += 0.1

# Run the chains and update the progress bar
title = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience)
progress += 0.1
progress_bar.progress(progress)

intro = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
progress += 0.1
progress_bar.progress(progress)

overview = overview_chain.run(main_topic=main_topic, subtopic=subtopic)
progress += 0.1
progress_bar.progress(progress)

topic_slide = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=main_topic_research + "\n\n" + subtopic_research)
progress += 0.1
progress_bar.progress(progress)

conclusion = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
progress += 0.1
progress_bar.progress(progress)

# Show the results
st.success('Presentation generated successfully!')
st.header('Presentation Title')
st.write(title)

st.header('Introduction')
st.write(intro)

st.header('Overview')
st.write(overview)

st.header('Main Topic Slide')
st.write(topic_slide)

st.header('Conclusion')
st.write(conclusion)
