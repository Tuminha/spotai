# Presentation Generator

The Presentation Generator is an application powered by the GPT3.5 language model. It allows users to create presentations by simply providing a topic. The application utilizes the LangChain framework for developing language model-powered applications.<br>
<!-- ![The app](presentation-generator.mp4) -->
<video width="320" height="240" controls>
  <source src="presentation-generator.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

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

## Acknowledgments

LangChain: https://langchain.org
OpenAI: https://openai.com
