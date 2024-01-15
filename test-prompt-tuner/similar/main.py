import openai

import sys
sys.path.append('..')
from utils import *

input('proceed?')

system_instruction = """I will provide you with a piece of first draft content (e.g. sentences, paragraphs, etc.) and a piece of target anchor content (e.g. sentences, paragraphs, etc.)

        You will generate a series of revisions of the first draft content that is increasingly similar to the target anchor content.

        Repeat the following 3 steps 5 times.

        Step 1. Identify 1-3 Unfamiliar Part (";" delimited) from the latest draft content which are the most different to the writing style of the target anchor content.

        Step 2. Rewrite every Unfamiliar Part into Revised Part using the style, word choice, and sentence structure following the target anchor content.

        Step 3. Write a new, revision for the draft content of identical length which replaces every Unfamiliar Part with the Revised Part and so that it becomes more similar to the target anchor content than the first draft content.

        A Unfamiliar Part is:

        Unfamiliar Style: to the target anchor content.
        Specific: Locate the sentence or phrase (15 words or fewer).
        Novel: not found in the previous Unfamiliar Part.
        Anywhere: located anywhere in the Article.

        Guidelines:

        Make every word count: re-write the previous draft to improve flow and connection before and after Revised Parts.
        Make space with fusion, compression, and removal of uninformative phrases like "the article discusses".
        The draft should become highly similar to the target anchor content yet retains all information from the first draft.
        Unfamiliar Part can appear anywhere in the draft.
        Never drop parts from the previous draft content. 
        Remember, use the exact same number of words for each draft. 
        Answer in JSON. The JSON should be a list (length 5) of dictionaries whose keys are "Unfamiliar_Part", "Revised_Part" and "Revised_Draft"."""


def main():
    anchor_text = readf('anchor.txt')
    first_draft = readf('draft.txt')
    messages = [
        system_struct(system_instruction),
        user_struct(f"Here is the target anchor content for you follow for the writing style, vocabulary, and sentence structure:\n\n{anchor_text}"),
        user_struct(f"Here is the first draft content for you to revise using the 'Unfamiliar_Part', 'Revised_Part' and 'Revised_Draft' approach:\n\n{first_draft}")
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
    try:
        dumpj(content, 'output.json')
    except:
        writf(content, 'output.txt')
    dumpj(completion, 'log.json')
    print(content)

if __name__ == '__main__':
    main()