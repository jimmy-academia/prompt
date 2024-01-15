import os
import googleapiclient.discovery
import json
import requests
from bs4 import BeautifulSoup
import re
import openai
input("proceed?")
with open('../key') as f:
    openai.api_key = f.read()


def readf(path):
    with open(path) as f:
        return f.read()

N = 10
api_key = readf('../newgooglekey')
search_engine_id = readf('../engineid')

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}

def google_search(query, search_engine_id, api_key, N, start=0):
    service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=api_key)

    request = service.cse().list(
        q=query,
        cx=search_engine_id,
        start=start,
        num=N,
    )

    response = request.execute()

    results = []
    results_str = ["[google search results]\n"]
    url_str = []
    i = 0
    for item in response['items']:
        results_str.append(str(i))
        rdict = {}
        for keywd in ['title', 'htmlTitle']:
            if keywd in item:
                rdict['title'] = item[keywd]
                results_str.append(f'title:{item[keywd]}')
                break

        for keywd in ['snippet', 'htmlSnippet']:
            if keywd in item:
                rdict['snippet'] = item[keywd]
                results_str.append(f'snippet:{item[keywd]}')
                break
        
        for keywd in ['url', 'link', 'displayLink', 'formattedUrl']:
            if keywd in item:
                rdict['url'] = item[keywd]
                results_str.append(f'url:{item[keywd]}')
                url_str.append(f'{i}: {item[keywd]}')
                break
        i += 1
                
        results.append(rdict)
    results_str = '\n'.join(results_str)

    return results, results_str, url_str

def readf(path):
    with open(path) as f:
        return f.read()

def gpt_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]

def get_number(sentence):
    messages = [
        system_struct("you are a robot who understands text sentences and outputs a number mentioned in the sentence. If no number is mentioned, output -1"),
        user_struct('The faculty webpage of Mahmud Shahriar Hossain is 0.'),
        assistant_struct('0'),
        user_struct('I cannot find the faculty webpage of Khoa Nguyen.'),
        assistant_struct('-1'),
        user_struct('The faculty webpage of Lu Han is 5.'),
        assistant_struct('5'),
        user_struct('There is no specific search result that indicates a faculty webpage for Manali Sharma.'),
        assistant_struct('-1'),
        user_struct(sentence)
    ]
    ans = gpt_answer(messages)    
    print('    ', sentence, '----->', ans)
    return ans

def solve_for_name(name, org=None):
    query = name if org is None else f'{name} {org}'
    print(f'Q:) {query}')
    results, results_str, url_str = google_search(query, search_engine_id, api_key, N)
    print('>> R:')

    worker_role = "You are an intelligent worker who follows instructions and do not reply additional information. You answer the precise result without additional comments. You will locate the google search result that best fits the target person who is a data mining computer science researcher. Find the the faculty webpage. If there is none, find the personal webpage. Otherwise, find academic pages such as dbpl or google scholar. Format your answer as: the best fit is result n, where n is a numerical number between 0 to 9"

    messages = [
        system_struct(worker_role),
        system_struct(f"Target person: {name}"),
        system_struct(results_str),
    ]
    # print(messages)
    question = f'Which search result best fits {name}?'
    messages.append(user_struct(question))
    ans = gpt_answer(messages)
    urln = get_number(ans)
    try:
        urln = int(urln)
    except:
        urln = -1

    url = ''
    if urln != -1 and urln < N:
        url = results[urln]['url']
        url_str[urln] = '*'+url_str[urln]
        url_str = '\n'.join(url_str)
        print(url_str)
    return url
        
def main():
    names = readf('input_name')
    organizations = readf('input_organization')

    names = names.split('\n')
    organizations = organizations.split('\n')
    
    
    url_list = []
    if os.path.exists('result_url.txt'):
        url_list = readf('result_url.txt').split('\n')
    start = len(url_list)

    for i in range(start, len(names)):
        name = names[i]
        org = organizations[i]
        print('========== ========== ==========')
        print(f'Working on {i}. {name} in {org}')
        url = solve_for_name(name, org)
        # if url == '':
        # print('==> redo witho org <==')
        # url = solve_for_name(name, org)

        url_list.append(url)
        with open('result_url.txt', 'w') as f:
            f.write('\n'.join(url_list))

if __name__ == '__main__':
    main()

        # for result in results:
        #     print(result['title'])
        #     print(result['snippet'])
        #     print(result['url'])
