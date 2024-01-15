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

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}


def scrape_text_information(url, limit=1200):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scrape = soup.get_text()

    scrape = re.sub(r'\n+', '\n', scrape)
    scrape = re.sub(r' +', ' ', scrape)
    scrape_words = scrape.split()
    if len(scrape_words) > limit*2:
        scrape = ' '.join(scrape_words[:limit] + scrape_words[-limit:])

    return scrape

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


def solve_for_name(name, org, scrape):
    worker_role = f"You are a worker who locates information instructions in text data. You reply the answer in terms. Do not exceed 5 words. Do not reply additional information. Do not use adjective. Answer without additional comments. You are to locate information from web scrape results for {name} who works in {org}, a researcher in data mining computer science. Find the email, their (faculty or job) position, and the country of their faculty or job."

    messages = [
        system_struct(worker_role),
        system_struct(f"Target person: {name}"),
        system_struct(f"webpage of {name}: {scrape}"),
    ]

    Answers = []
    for i, question in enumerate([f"What is the email of {name}?", f'What is the position/job of {name}?', 'What country?']):
        ans = gpt_answer(messages + [user_struct(question)])
        Answers.append(ans)

    return Answers

def google_again(name, org):
    N = 10
    api_key = readf('../newgooglekey')
    search_engine_id = readf('../engineid')
    service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=api_key)

    query = f"{name} email {org}"
    request = service.cse().list(
        q=query,
        cx=search_engine_id,
        num=N,
    )

    response = request.execute()
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
        
        i += 1
    results_str = '\n'.join(results_str)

    worker_role = f"You are a worker who locates information instructions in text data. You reply the answer in terms. Do not exceed 5 words. Do not reply additional information. Do not use adjective. Answer without additional comments. You are to locate information from google search results for {name} who works in {org}, a researcher in data mining computer science. Find the email, their (faculty or job) position, and the country of their faculty or job."

    messages = [
        system_struct(worker_role),
        system_struct(f"Target person: {name}"),
        system_struct(f"search results of {name}:\n {results_str}"),
    ]

    Answers = []
    for i, question in enumerate([f"What is the email of {name}?", f'What is the position/job of {name}?', 'What country?']):
        ans = gpt_answer(messages + [user_struct(question)])
        Answers.append(ans)

    return Answers

def main():
    names = readf('../format_name/input_name')
    organizations = readf('input_organization')
    urls = readf('result_url.txt')

    names = names.split('\n')
    organizations = organizations.split('\n')
    urls = urls.split('\n')
    
    email_list = []
    position_list = []
    country_list = []

    for i in range(len(names)):
        name = names[i]
        org = organizations[i]
        url = urls[i]
        print('==========')
        print(f'Working on {i}. {name}, {org}, {url}')
        Answers = ['']*3
        if url != '' and 'scholar' not in url:
            try:
                scrape = scrape_text_information(url)
                Answers = solve_for_name(name, org, scrape)
            except:
                print('...')

        if Answers == ['']*3:
            Answers = google_again(name, org)

        print(Answers)
        for ans, _list in zip(Answers, [email_list, position_list, country_list]):
            _list.append(ans)
        with open('output/email.txt', 'w') as f:
            f.write('\n'.join(email_list))
        with open('output/position.txt', 'w') as f:
            f.write('\n'.join(position_list))
        with open('output/country.txt', 'w') as f:
            f.write('\n'.join(country_list))

if __name__ == '__main__':
    main()

