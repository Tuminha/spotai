import os 

import streamlit as st 
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
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
    selected_temperature = st.selectbox('Select the temperature mode. The different modes represent different expected output', list(temperature_options.keys()))
    
    submit_button = st.form_submit_button(label='Submit')

    # ADD: New memory class to keep track of previous slide content
    class ExtendedConversationBufferMemory(ConversationBufferMemory):
        def __init__(self, input_key, memory_key, slide_content_key):
            super().__init__(input_key, memory_key)
            self.slide_content_key = slide_content_key

        def update_memory(self, input_data, output_data):
            super().update_memory(input_data, output_data)
            if self.slide_content_key in input_data:
                self.memory[self.slide_content_key] = input_data[self.slide_content_key]

        def get_memory(self):
            memory = super().get_memory()
            if self.slide_content_key in self.memory:
                memory[self.slide_content_key] = self.memory[self.slide_content_key]
            return memory


if submit_button:
    # Validation
    if not main_topic or not subtopic or not duration.isdigit() or not audience:
        st.error("Please fill in all the fields correctly.")
    else:
        temperature = temperature_options[selected_temperature]

        # Initialize the OpenAI API with the API key from Heroku config vars
        llm = ChatOpenAI(api_key=openai_api_key, temperature=temperature, model_name="gpt-3.5-turbo")

        # Prompt templates
        # CHANGE: Varying the prompt templates to provide more context and guidance

        title_template = PromptTemplate(
            input_variables=['main_topic'],
            template='Create an attention-grabbing title for a presentation on {main_topic} that captures the audience\'s interest and clearly conveys the main message.'
        )


        intro_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Engage the audience by sharing a captivating story or presenting a thought-provoking question related to {main_topic} and {subtopic}. Then, introduce the importance of these topics, their relevance in the field, and recent advancements.'
        )

        overview_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Create a detailed roadmap for this presentation on {main_topic} and {subtopic}. Highlight key subtopics to be covered, their significance, and provide tips on how to structure the presentation effectively, such as using visual aids or storytelling techniques.'
        )


        topic_slide_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic', 'wikipedia_research', 'previous_slide_content'],
            template='Continuing from the previous slide which discussed {previous_slide_content}, create a structured slide on {main_topic} and {subtopic} drawing from this research: {wikipedia_research}. The slide should contain a clear header, 3-5 bullet points, a brief summary, and incorporate best practices from Nancy Duarte\'s presentations. Alternatively, create controversy by presenting contrasting viewpoints on the topic.'
        )


        conclusion_template = PromptTemplate(
            input_variables=['main_topic', 'subtopic'],
            template='Conclude this presentation on {main_topic} and {subtopic} with a memorable closing statement or call-to-action that inspires the audience to take action or further explore the presented topics. Summarize the main points discussed and thank the audience for their attention.'
        )





    # The original memory class for the chains
    title_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
    intro_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
    overview_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
    topic_slide_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')
    conclusion_memory = ConversationBufferMemory(input_key='main_topic', memory_key='chat_history')


    # GPT model
    title_chain = LLMChain(prompt=title_template, llm=llm, memory=title_memory)
    intro_chain = LLMChain(prompt=intro_template, llm=llm, memory=intro_memory)
    overview_chain = LLMChain(prompt=overview_template, llm=llm, memory=overview_memory)
    topic_slide_chain = LLMChain(prompt=topic_slide_template, llm=llm, memory=topic_slide_memory)
    conclusion_chain = LLMChain(prompt=conclusion_template, llm=llm, memory=conclusion_memory)

    # Wikipedia
    wiki = WikipediaAPIWrapper()

    # Show results
    input_key_main_topic = main_topic
    input_key_combined = f"{main_topic} {subtopic}"
    duration = int(duration)  # Convert duration to an integer

    progress_bar = st.progress(0)  # Initialize progress bar

    # Perform separate queries to Wikipedia
    wiki_research_main_topic = get_wiki_research(input_key_main_topic, 25/100)
    wiki_research_combined = get_wiki_research(input_key_combined, 50/100)

    # Generate content for each slide
    slides = []

    # Title slide
    title_slide = title_chain.run(main_topic=main_topic, subtopic=subtopic, duration=duration, audience=audience)
    slides.append(("SLIDE 1: **{}**".format(title_slide.upper()), ''))
    progress_bar.progress(60/100)  # Update the progress bar

    # Introduction slide
    intro_slide = intro_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE 2: **INTRODUCTION**", intro_slide))
    progress_bar.progress(70/100)  # Update the progress bar

    # Overview slide
    overview_slide = overview_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE 3: **OVERVIEW**", overview_slide))
    progress_bar.progress(75/100)  # Update the progress bar

        # Topic slides
    num_topic_slides = duration // 3  # 1 slide per 3 minutes of duration

    # CHANGE: Include the content of the previous slide when running the chain
    previous_slide_content = ""
    for i in range(num_topic_slides):
        topic_slide = topic_slide_chain.run(main_topic=main_topic, subtopic=subtopic, wikipedia_research=wiki_research_combined, previous_slide_content=previous_slide_content)
        previous_slide_content = topic_slide  # update previous_slide_content

    # Conclusion slide
    conclusion_slide = conclusion_chain.run(main_topic=main_topic, subtopic=subtopic)
    slides.append(("SLIDE {}: **CONCLUSION**".format(num_topic_slides+4), conclusion_slide))
    progress_bar.progress(90/100)  # Update the progress bar

    # Display the generated slides
    for slide in slides:
        slide_title = slide[0]
        slide_content = slide[1]
        slide_image_prompt = slide[2] if len(slide) > 2 else None
        slide_content_formatted = "• " + slide_content.replace(". ", ".\n• ")  # Bullet points for slide content

        st.markdown(slide_title)
        st.markdown(slide_content_formatted)
        if slide_image_prompt:
            st.markdown(f"**Image Prompt:** {slide_image_prompt}")
        st.markdown("\n_Reference: Placeholder for bibliographic reference_\n")
        st.markdown("---")

    progress_bar.progress(100/100)  # Complete the progress bar

    with st.expander('Wikipedia Research - Main Topic'): 
        st.info(wiki_research_main_topic)

    with st.expander('Wikipedia Research - Combined Topic'): 
        st.info(wiki_research_combined)

