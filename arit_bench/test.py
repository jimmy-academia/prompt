import random 

import openai
input("proceed?")
with open('keys/openai_apikey') as f:
    openai.api_key = f.read()

def readf(path):
    with open(path) as f:
        return f.read()

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}

worker_role = "You are an intelligent worker who follows instructions and do not reply additional information. You answer the precise result without additional comments. Given the arithmetic expression, only reply the numerical answer. Use decimal if needed."


def gpt_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        # temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]


# symbol_list = ['+', '-', '*', '/', '**', '%', '//', '&', '|', '^', '>>', '<<']
symbol_list = ['+', '-', '*']
numel_list = list(map(str, range(10)))

def gen_sequence(L):
    assert L >= 3
    sequence = []
    for index in range(L):
        match index:
            case 0:
                element = random.choice(numel_list[1:])
            case x if x == L - 1:
                element = random.choice(numel_list)
            case _:
                if element in symbol_list:
                    element = random.choice(numel_list[1:])
                else:
                    element = random.choice(numel_list+symbol_list)
        sequence.append(element)

    if not any(symbol in sequence for symbol in symbol_list):
        replace_index = random.randint(1, L - 2)
        sequence[replace_index] = random.choice(symbol_list)
        if sequence[replace_index+1] == '0':
            sequence[replace_index+1] = random.choice(numel_list[1:])

    sequence = ''.join(sequence)
    return sequence

def main():
    Acc_list = []
    for L in range(3, 10):
        repeat = 3
        correct = 0
        for j in range(repeat):
            sequence = gen_sequence(L)
            messages = [
                system_struct(worker_role),
                user_struct(sequence),
            ]
            out = gpt_answer(messages)    
            ans = str(eval(sequence))
            if out == ans:
                correct += 1
            print(sequence, out, ans)
        Acc_list.append(correct/repeat)

    print(Acc_list)

if __name__ == '__main__':
    main()
    # messages = [
    #     system_struct(''),
    #     user_struct('say hello world'),
    # ]
    # print(gpt_answer(messages))



