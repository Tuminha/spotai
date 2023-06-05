import os
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate, Wikipedia
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 
from dotenv import load_dotenv

# Get the OpenAI API key from Heroku config vars
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Function to update the progress bar and fetch Wikipedia research
def get_wiki_research(topic, progress):
    wiki_research = wiki.run(topic)
    progress_bar.progress(progress)
    return wiki_research

# Function to format slide content into bullet points
def format_slide_content(content):
    return content.replace(". ", ".\n• ")

# App framework
st.title('🦷 Perio & Implant dentistry Presentation Creator')
with st.form(key='my_form'):
    main_topic = st.text_input('Enter the main topic')
    subtopic = st.text_input('Enter the subtopic')
    duration = st.text_input('Enter the duration of the presentation')
    audience = st.text_input('Enter the audience for the presentation')

    # Temperature options
    temperature_options = {
        'Daniel Rodrigo Mode': 0.2,
        'Leticia Sala Mode': 0.5,
        'Robles Mode': 0.9
    }
    selected_temperature = st.selectbox('Select the temperature mode', list(temperature_options.keys()))
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Validation
    if not main_topic or not subtopic or not duration.isdigit() or not audience:
        st.error("Please fill in all the fields correctly.")
    else:
        temperature = temperature_options[selected_temperature]

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
        title_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
        intro_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
        overview_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
        topic_slide_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
        conclusion_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')

        # Chains
        title_chain = LLMChain(llm=llm, prompt=title_template, memory=title_memory)
        intro_chain = LLMChain(llm=llm, prompt=intro_template, memory=intro_memory)
        overview_chain = LLMChain(llm=llm, prompt=overview_template, memory=overview_memory)
        topic_slide_chain = LLMChain(llm=llm, prompt=topic_slide_template, memory=topic_slide_memory)
        conclusion_chain = LLMChain(llm=llm, prompt=conclusion_template, memory=conclusion_memory)

        wiki = WikipediaAPIWrapper()

        # Generate slide 1: Cover slide
        st.header('Slide 1: Cover Slide')
        st.subheader(f'Title: {main_topic}')
        st.subheader(f'Subtopic: {subtopic}')

        # Generate slide 2: Learning objectives
        st.header('Slide 2: Learning Objectives')
        st.subheader('Learning Objectives:')
        st.markdown("""
        - Objective 1
        - Objective 2
        - Objective 3
        """)

        # Generate slide 3: Presentation Overview
        st.header('Slide 3: Presentation Overview')
        st.subheader('Index and Key Points:')
        st.markdown("""
        - Introduction to {main_topic}
        - Key Point 1
        - Key Point 2
        - Key Point 3
        """)

        # Generate slide 4: Introduction
        st.header('Slide 4: Introduction')
        st.subheader(f'Introduction to {main_topic}')
        intro_slide_content = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
        st.write(format_slide_content(intro_slide_content))

        # Generate content slides
        num_slides = (int(duration) - 4) // 3  # Number of content slides based on duration
        for slide_number in range(5, 5 + num_slides):
            st.header(f'Slide {slide_number}: Slide Title')
            st.subheader('Slide Title')
            slide_content = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research="Research for Slide " + str(slide_number))
            st.write(format_slide_content(slide_content))

        # Generate conclusion slide
        st.header(f'Slide {num_slides + 5}: Conclusion')
        st.subheader('Conclusion')
        conclusion_slide_content = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
        st.write(format_slide_content(conclusion_slide_content))

        # Show the results
        st.success('Presentation generated successfully!')
