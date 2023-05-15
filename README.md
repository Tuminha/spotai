# Presentation Generator

The Presentation Generator is an application powered by the GPT3.5 language model. It allows users to create presentation scripts by simply providing a topic. The application utilizes the LangChain framework for developing language model-powered applications.<br>
<!-- ![The app](presentation-generator.mp4) -->



https://github.com/mehdi0807/presentation-generator-gpt/assets/92737907/5d443dec-3924-4d14-b432-1d3bc359fc71


## Features

- Generate presentation titles: The application prompts the GPT3.5 model to generate a suitable title for the presentation based on the provided topic.
- Research using Wikipedia: The application employs LangChain's agent and tools to gather relevant information from Wikipedia based on the generated title.
- Presentation generation: The GPT3.5 model generates the actual presentation content by utilizing the title and the research obtained from Wikipedia.

## Requirements

To run the Presentation Generator, ensure you have the following:

- Python
- LangChain
- OpenAI GPT3.5 API key

## Usage

1. Run the application:
<pre>
stramlit run app.py
</pre>

2. Enter a topic for your presentation when prompted.

3. The application will generate a suitable title for your presentation using the GPT3.5 model.

4. The LangChain agent will retrieve information from Wikipedia based on the generated title.

5. The GPT3.5 model will generate the content for the presentation using the title and Wikipedia research.

6. The generated presentation will be displayed or saved, depending on your configuration.

## Configuration

- OpenAI API Key: Replace the placeholder `'YOUR_API_KEY'` in the `app.py` file with your actual OpenAI GPT3.5 API key. 

<pre>
os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY'
</pre>

## Limitations

The accuracy and quality of the generated presentation heavily depend on the GPT3.5 model's performance and the accuracy of the information retrieved from Wikipedia.

## Motivation

The Presentation Generator was created out of a personal need and experience. Over the past few months, I found myself giving numerous presentations for various school subjects and projects. I realized that creating engaging and informative presentations from scratch can be time-consuming and challenging, especially when juggling multiple assignments.

This application aims to address this issue by providing a tool that can quickly generate presentation content based on a given topic. By leveraging the power of the GPT3.5 language model and the research capabilities of LangChain, the Presentation Generator can assist students, like myself, in kickstarting their presentations with relevant and well-structured content.

The goal is to simplify the process of creating presentations, allowing users to focus more on refining and delivering their ideas rather than spending excessive time on research and content generation.

I hope that by sharing this application, it can benefit other students and individuals who face similar challenges when preparing presentations for academic or professional purposes.

## Acknowledgments

LangChain: https://langchain.org

OpenAI: https://openai.com
