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
    wiki_research = Wikipedia.run(topic)
    progress_bar.progress(progress)
    return wiki_research

# Function to format slide content into bullet points
def format_slide_content(content):
    return "• " + content.replace(". ", ".\n• ")

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

        topic_slide_template1 = PromptTemplate(
            input_variables=['main_topic', 'subtopic', 'wikipedia_research'],
            template='Create a slide about {main_topic} and {subtopic} focusing on advantage based on this research: {wikipedia_research}.'
        )

        topic_slide_template2 = PromptTemplate(
            input_variables=['main_topic', 'subtopic', 'wikipedia_research'],
            template='Create a slide about {main_topic} and {subtopic} focusing on procedure based on this research: {wikipedia_research}.'
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
        topic_slide_chain1 = LLMChain(llm=llm, prompt=topic_slide_template1, memory=topic_slide_memory)
        topic_slide_chain2 = LLMChain(llm=llm, prompt=topic_slide_template2, memory=topic_slide_memory)
        conclusion_chain = LLMChain(llm=llm, prompt=conclusion_template, memory=conclusion_memory)

        # Progress bar
        progress_bar = st.progress(0)

        # Fetch Wikipedia research for each of the topics and update the progress bar
        main_topic_research = get_wiki_research(main_topic, 0.1)
        subtopic_research = get_wiki_research(subtopic, 0.2)

        # Run the chains and update the progress bar
        progress_bar.progress(0.3)
        title = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience)
        progress_bar.progress(0.4)
        intro = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
        progress_bar.progress(0.5)
        overview = overview_chain.run(main_topic=main_topic, subtopic=subtopic)
        progress_bar.progress(0.6)
        topic_slide1 = topic_slide_chain1.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=main_topic_research + "\n\n" + subtopic_research)
        progress_bar.progress(0.7)
        topic_slide2 = topic_slide_chain2.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=main_topic_research + "\n\n" + subtopic_research)
        progress_bar.progress(0.8)
        conclusion = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
        progress_bar.progress(1.0)

        # Show the results
        st.success('Presentation generated successfully!')

        st.header('Presentation Title')
        st.write(format_slide_content(title))

        st.header('Introduction')
        st.write(format_slide_content(intro))

        st.header('Overview')
        st.write(format_slide_content(overview))

        st.header('Main Topic Slide 1')
        st.write(format_slide_content(topic_slide1))

        st.header('Main Topic Slide 2')
        st.write(format_slide_content(topic_slide2))

        st.header('Conclusion')
        st.write(format_slide_content(conclusion))
