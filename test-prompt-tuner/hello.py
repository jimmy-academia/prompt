import json
import openai
input("proceed?")
with open('keys/openai_apikey') as f:
    openai.api_key = f.read()

strict_servent = "you are a good servent. you follow orders. no more. no less."
servent = "you are a good servent"

prompt_translate = "Translate the following English text to French: 'Hello World'"
prompt_sayhello = "say: \"hello world\""

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [
        system_struct(strict_servent),
        # user_struct(prompt_sayhello)
        user_struct(prompt_translate)
        ],
    temperature=0.5,
    # max_tokens=30,
    # top_p=1,
    # frequency_penalty=0.2,
    # presence_penalty=0,
    # stop=["\"\"\""]
)

# print(response)
print(response["choices"][0]["message"]["content"])