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

N = 5
api_key = readf('../newgooglekey')
search_engine_id = readf('../engineid')

user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}

worker_role = "You are an intelligent worker who follows instructions and do not reply additional information. You answer the precise result without additional comments."
# " You are tasked to locate information from google search results for <target person>, a data mining computer scientist. You need to find their faculty webpage, faculty (or job) position and faculty (or job) country."


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
    for item in response['items']:
        results.append({
            'title': item['title'],
            'snippet': item['snippet'],
            'url': item['link']
        })
    results_str = ["[google search result]\n"]
    for i, res in enumerate(results):
        results_str.append(str(i))
        for keywd in ['title', 'snippet', 'url']:
            results_str.append(f'{keywd}:{res[keywd]}')
    results_str = '\n'.join(results_str)

    return results, results_str

def scrape_text_information(url, limit=900):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scrape = soup.get_text()

    scrape = re.sub(r'\n+', '\n', scrape)
    scrape = re.sub(r' +', ' ', scrape)
    scrape_words = scrape.split()
    if len(scrape_words) > limit*2:
        scrape = ' '.join(scrape_words[:limit] + scrape_words[-limit:])

    return scrape

def gpt_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages,
        temperature=0.2,
    )
    return response["choices"][0]["message"]["content"]

def first_example(name):
    results, results_str = google_search(name, search_engine_id, api_key, N)
    system = [
        system_struct(worker_role),
        system_struct(f"<target person>: {name}"),
        system_struct(results_str),
    ]
    pairs = [
        [
            user_struct(f'Which search result is the faculty webpage (or alternatively, google scholar webpage) of {name}?'),
            assistant_struct(f'The faculty webpage of {name} is 0'),
        ],
        [
            user_struct(f'What is the position/job of {name}?'),
            assistant_struct('Assistant Professor'),
        ],
        [
            user_struct('What country?'),
            assistant_struct('United States'),
        ]
    ]
    scrap_ex = [
        system_struct(f"{worker_role} The following is text scrape of the webpage of {name}:"),
        system_struct(scrape_text_information('https://faculty.rpi.edu/lydia-manikonda')),
        user_struct(f"What is the email of {name}?"),
        assistant_struct('manikl@rpi.edu')
    ]

    return system, pairs, scrap_ex

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
    print(sentence)
    ans = gpt_answer(messages)    
    print(ans)
    return ans

def solve_for_name(name, system, pairs, scrap_ex):
    results, results_str = google_search(name, search_engine_id, api_key, N)
    print('google result:')
    print(results_str)
    messages = [
        system_struct(f"Target person: {name}"),
        system_struct(results_str),
    ]
    print(messages)

    Answers = []
    for i, question in enumerate([f'Which search result is the faculty webpage (or alternatively, google scholar webpage) of {name}?', f'What is the position/job of {name}?', 'What country?']):
        print(question)
        messages.append(user_struct(question))
        ans = gpt_answer(system + pairs[i] + messages)
        Answers.append(ans)
        print(ans)

    urln = get_number(Answers[0])
    try:
        urln = int(urln)
    except:
        urln = -1

    url = ''
    ans = ''
    if urln != -1 and urln < N:
        url = results[urln]['url']
        print(url)
        if 'scholar' in url:
            print('...........pass scholar..........')
        else:
            try:
                scrape = scrape_text_information(url)
                messages = scrap_ex
                messages += [
                    system_struct(f"The following is text scrape of the webpage of {name}. locate the email information. change at to @."),
                    system_struct(scrape),
                    user_struct(f"What is the email of {name}?"),
                ]
                print(messages)
                ans = gpt_answer(messages)
                print(ans)
            except:
                print(f'======== cannot scrape for {url} ======== ')
    else:
        print('------- cannot retrieve url ------- ')
    Answers.append('')
    return results, Answers, url
        
def main():
    names = readf('../format_name/input_name')
    names = names.split('\n')
    system, pairs, scrap_ex = first_example(names[0])
    
    url_list = []
    for i in range(19, len(names)):
        name = names[i]
        print('==========')
        print(f'Working on {i}. {name}')
        results, Answers, url = solve_for_name(name, system, pairs, scrap_ex)
        url_list.append(url)

        with open(f'record/{i}', 'w') as f:
            f.write('\n'.join(Answers))

        with open('result_url.txt', 'w') as f:
            f.write('\n'.join(url_list))

if __name__ == '__main__':
    main()

        # for result in results:
        #     print(result['title'])
        #     print(result['snippet'])
        #     print(result['url'])
