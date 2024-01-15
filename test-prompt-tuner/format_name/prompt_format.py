import json
import openai
input("proceed?")
with open('../key') as f:
    openai.api_key = f.read()

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}

secretary_role = "You are a good secretary who follows instructions and conform to examples. Take the list of names seperated by \n and put \t between first, middle, and last name. If the persone does not have a middle name, put two \t\t to leave the middle name blank. Example:"

with open('input_name') as f:
    input_name = f.read()

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [
        system_struct(secretary_role),
        user_struct('Lydia Manikonda\nMichael E. Houle\nMarinka Zitnik\nMario Alfonso Prado Romero\nMarcin Sydow\nMarco Botta\nMarco Luca Sbodio'),
        assistant_struct('Lydia\t\tManikonda\nMichael\tE.\tHoule\nMarinka\t\tZitnik\nMario\tAlfonso\tPrado Romero\nMarcin\t\tSydow\nMarco\t\tBotta\nMarco\tLuca\tSbodio'),
        system_struct('Now process the list of names:'),
        user_struct(input_name),
        ],
    temperature=0.3,
)

print(response)
with open('response.json', 'w') as f:
    json.dump(response, f, indent=4)

with open('name.txt', 'w') as f:
    f.write(response["choices"][0]["message"]["content"])

