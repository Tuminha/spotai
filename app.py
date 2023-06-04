import os 
os.environ['OPENAI_API_KEY'] = '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'

import streamlit as st 
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

# App framework
st.title('🦷 Perio & Implant dentistry Presentation Creator')
main_topic = st.text_input('Enter the main topic')
subtopic = st.text_input('Enter the subtopic')
duration = st.text_input('Enter the duration of the presentation')
audience = st.text_input('Enter the audience for the presentation')

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
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(prompt=title_template, llm=llm, memory=title_memory)
intro_chain = LLMChain(prompt=intro_template, llm=llm, memory=intro_memory)
topic_slide_chain = LLMChain(prompt=topic_slide_template, llm=llm, memory=topic_slide_memory)
conclusion_chain = LLMChain# The assistant code was cut off in the previous message. Continue the code here.
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

    # Generate content for each slide
    slides = []

    # Title slide
    title_slide = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience)
    slides.append(("SLIDE 1: **{}**".format(title_slide.upper()), ''))

    # Introduction slides
    intro_slide = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE 2: **INTRODUCTION**", intro_slide))

    # Topic slides
    num_topic_slides = duration // 3  # 1 slide per 3 minutes of duration
    for i in range(num_topic_slides):
        topic_slide = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=wiki_research_combined)
        image_prompt = "Imagine a depiction of {main_topic} and {subtopic}. 4K, Realistic".format(main_topic=main_topic, subtopic=subtopic)
        slides.append(("SLIDE {}: **{}**".format(i+3, topic_slide.upper()), topic_slide, image_prompt))

    # Conclusion slide
    conclusion_slide = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE {}: **CONCLUSION**".format(num_topic_slides+3), conclusion_slide))

    # Display the generated slides
    for slide in slides:
        st.markdown(slide[0])  # Slide title in uppercase and bold
        st.write("• " + slide[1].replace(". ", ".\n• "))  # Bullet points for slide content
        if len(slide) > 2:
            st.write("Image Prompt: " + slide[2])  # Image generation prompt
        st.write("\n*Reference: Placeholder for bibliographic reference*\n")  # Placeholder for bibliographic reference

    with st.expander('Wikipedia Research - Main Topic'): 
        st.info(wiki_research_main_topic)

    with st.expander('Wikipedia Research - Combined Topic'): 
        st.info(wiki_research_combined)