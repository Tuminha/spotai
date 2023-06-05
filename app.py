import os 

import streamlit as st 
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 
from dotenv import load_dotenv

# Get the OpenAI API key from Heroku config vars
openai_api_key = os.environ.get('OPENAI_API_KEY')

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
    topic_slide_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
    conclusion_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')

    # GPT model
    title_chain = LLMChain(prompt=title_template, llm=llm, memory=title_memory)
    intro_chain = LLMChain(prompt=intro_template, llm=llm, memory=intro_memory)
    topic_slide_chain = LLMChain(prompt=topic_slide_template, llm=llm, memory=topic_slide_memory)
    conclusion_chain = LLMChain(prompt=conclusion_template, llm=llm, memory=conclusion_memory)

    # Wikipedia
    wiki = WikipediaAPIWrapper()

    # Show results
    if main_topic and subtopic and duration and audience: 
        input_key_main_topic = main_topic
        input_key_combined = f"{main_topic} {subtopic}"
        duration = int(duration)  # Convert duration to an integer

        # Perform separate queries to Wikipedia
        wiki_research_main_topic = wiki.run(input_key_main_topic)
        wiki_research_combined = wiki.run(input_key_combined)

    progress_bar = st.progress(0)  # Initialize progress bar
    progress_bar.progress(10 / 100)  # Update the progress bar

    wiki_research_main_topic = wiki.run(input_key_main_topic)
    progress_bar.progress(25/100)  # Update the progress bar

    wiki_research_combined = wiki.run(input_key_combined)
    progress_bar.progress(50/100)  # Update the progress bar

    # Generate content for each slide
    slides = []

    # Title slide
    title_slide = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience)
    slides.append(("SLIDE 1: **{}**".format(title_slide.upper()), ''))
    progress_bar.progress(60/100)  # Update the progress bar

    # Introduction slides
    intro_slide = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE 2: **INTRODUCTION**", intro_slide))
    progress_bar.progress(70/100)  # Update the progress bar

    # Topic slides
    num_topic_slides = duration // 3  # 1 slide per 3 minutes of duration
    for i in range(num_topic_slides):
        topic_slide = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=wiki_research_combined)
        image_prompt = "Imagine a depiction of {main_topic} and {subtopic}. 4K, Realistic".format(main_topic=main_topic, subtopic=subtopic)
        slides.append(("SLIDE {}: **{}**".format(i+3, topic_slide.upper()), topic_slide, image_prompt))
        progress_bar.progress((70 + i*10/num_topic_slides) / 100)  # Update the progress bar

    # Conclusion slide
    conclusion_slide = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE {}: **CONCLUSION**".format(num_topic_slides+3), conclusion_slide))
    progress_bar.progress(90/100)  # Update the progress bar

    # Display the generated slides
    for slide in slides:
        st.markdown(slide[0])  # Slide title in uppercase and bold
        st.write("• " + slide[1].replace(". ", ".\n• "))  # Bullet points for slide content
        if len(slide) > 2:
            st.write("Image Prompt: " + slide[2])  # Image generation prompt
        st.write("\n*Reference: Placeholder for bibliographic reference*\n")  # Placeholder for bibliographic reference

    progress_bar.progress(100)  # Update the progress bar to complete

    with st.expander('Wikipedia Research - Main Topic'): 
        st.info(wiki_research_main_topic)

    with st.expander('Wikipedia Research - Combined Topic'): 
        st.info(wiki_research_combined)
