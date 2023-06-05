import os

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
from langchain.chains import Chain
from langchain.llms import OpenAI



# Load environment variables
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI API
openai = OpenAI(api_key=openai_api_key)

# Initialize the Wikipedia API wrapper
wikipedia = WikipediaAPIWrapper()


# Function to update the progress bar and fetch Wikipedia research
def get_wiki_research(topic, progress_bar):
    progress_bar.progress(0.1)
    wiki_research = wikipedia.run(topic)
    progress_bar.progress(0.2)
    return wiki_research


# App framework
st.title('🦷 Perio & Implant dentistry Presentation Creator')

with st.form(key='my_form'):
    main_topic = st.text_input('Enter the main topic')
    subtopic = st.text_input('Enter the subtopic')
    duration = st.text_input('Enter the duration of the presentation')
    audience = st.text_input('Enter the audience for the presentation')
    temperature_mode = st.selectbox('Select the temperature mode', ['Daniel Rodrigo Mode', 'Leticia Sala Mode', 'Robles Mode'])

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    # Validation
    if not main_topic or not subtopic or not duration.isdigit() or not audience:
        st.error("Please fill in all the fields correctly.")
    else:
        # Temperature options
        temperature_options = {
            'Daniel Rodrigo Mode': 0.2,
            'Leticia Sala Mode': 0.5,
            'Robles Mode': 0.9
        }
        temperature = temperature_options.get(temperature_mode, 0.2)

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

        # Initialize conversation buffers
        memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')

        # Initialize chains
        title_chain = Chain([
            get_wiki_research,
            OpenAI(llm=openai, prompt=title_template),
        ], memory=memory)

        intro_chain = Chain([
            get_wiki_research,
            OpenAI(llm=openai, prompt=intro_template),
        ], memory=memory)

        overview_chain = Chain([
            get_wiki_research,
            OpenAI(llm=openai, prompt=overview_template),
        ], memory=memory)

        topic_slide_chain = Chain([
            get_wiki_research,
            OpenAI(llm=openai, prompt=topic_slide_template),
        ], memory=memory)

        conclusion_chain = Chain([
            get_wiki_research,
            OpenAI(llm=openai, prompt=conclusion_template),
        ], memory=memory)

        # Progress bar
        progress_bar = st.progress(0)

        # Fetch Wikipedia research for each of the topics and update the progress bar
        main_topic_research = get_wiki_research(main_topic, progress_bar)
        subtopic_research = get_wiki_research(subtopic, progress_bar)

        # Run the chains and update the progress bar
        progress_bar.progress(0.3)
        title = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience, progress_bar=progress_bar)
        progress_bar.progress(0.4)
        intro = intro_chain.run(main_topic=main_topic, subtopic=subtopic, progress_bar=progress_bar)
        progress_bar.progress(0.5)
        overview = overview_chain.run(main_topic=main_topic, subtopic=subtopic, progress_bar=progress_bar)
        progress_bar.progress(0.6)
        topic_slide = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=main_topic_research + "\n\n" + subtopic_research, progress_bar=progress_bar)
        progress_bar.progress(0.7)
        conclusion = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic, progress_bar=progress_bar)
        progress_bar.progress(1.0)

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
