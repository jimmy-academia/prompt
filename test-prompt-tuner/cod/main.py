import openai

import sys
sys.path.append('..')
from utils import *

input('proceed?')

system_instruction = """I will provide you with piece of content (e.g. articles, papers, documentation, etc.)

        You will generate increasingly concise, entity-dense summaries of the content.

        Repeat the following 2 steps 5 times.

        Step 1. Identify 1-3 informative Entities (";" delimited) from the Article which are missing from the previously generated summary.

        Step 2. Write a new, denser summary of identical length which covers every entity and detail from the previous summary plus the Missing Entities.

        A Missing Entity is:

        Relevant: to the main story.
        Specific: descriptive yet concise (5 words or fewer).
        Novel: not in the previous summary.
        Faithful: present in the content piece.
        Anywhere: located anywhere in the Article.

        Guidelines:

        The first summary should be long (5 sentences, -80 words) yet highly non-specific, containing little information beyond the entities marked as missing. Use overly verbose language and fillers (e.g., "this article discusses") to reach -80 words.
        Make every word count: re-write the previous summary to improve flow and make space for additional entities.
        Make space with fusion, compression, and removal of uninformative phrases like "the article discusses".
        The summaries should become highly dense and concise yet self-contained, e.g., easily understood without the Article.
        Missing entities can appear anywhere in the new summary.
        Never drop entities from the previous summary. If space cannot be made, add fewer new entities.
        Remember, use the exact same number of words for each summary.
        Answer in JSON. The JSON should be a list (length 5) of dictionaries whose keys are "Missing_Entities" and "Denser_Summary"."""


def main():
    input_text = readf('input.txt')
    messages = [
        system_struct(system_instruction),
        user_struct(f"Here is the input text for you to summarise using the 'Missing_Entities' and 'Denser_Summary' approach:\n\n{input_text}")
    ]

    parameters = {
        "model": 'gpt-4-0613',
        "messages": messages,
        "n": 1,
    }

    max_attempts = 10  # Maximum number of retry attempts
    retry_gap = 3.0  # Initial gap between retries in seconds

    openai.api_key = readf('../keys/openai_apikey')

    for attempt in range(max_attempts):
        try:
            print(f"attempt: {attempt}")
            completion = openai.ChatCompletion.create(**parameters)
            break
        except Exception as e:
            print(f"Request failed on attempt {attempt + 1}. Error: {str(e)}")
            if attempt < max_attempts - 1:
                retry_gap *= 1.5  # Increase the retry gap exponentially
                time.sleep(retry_gap)


    content = completion["choices"][0]["message"]["content"]

    # Write the output to file
    writef(content, 'output.txt')
    dumpj(completion, 'output.txt')
    print(content)

if __name__ == '__main__':
    main()