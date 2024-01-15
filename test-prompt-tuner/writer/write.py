import json
import openai

from instructions import *
input("proceed?")
openai.api_key = readf('../keys/openai_apikey')

worker_role = "You are skilled writer. computer scientist. data mining paper."
task = "rewrite the abstract. keep the length within 1000 words."

def gpt_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]

def main():
    messages = [
        system_struct(worker_role),
        user_struct(readf('text')),
        system_struct(task),
    ]

    ans = gpt_answer(messages)
    writef('output', ans)

    print(ans)

if __name__ == '__main__':
    main()

