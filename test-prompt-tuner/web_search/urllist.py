import googleapiclient.discovery
import json
import requests
from bs4 import BeautifulSoup

def google_search(query, search_engine_id, api_key, startN, N):
    service = googleapiclient.discovery.build('customsearch', 'v1', developerKey=api_key)

    request = service.cse().list(
        q=query,
        cx=search_engine_id,
        start=startN,
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

    return results

def scrape_text_information(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return text

def readf(path):
    with open(path) as f:
        return f.read()

def process_web_text(url):
    # goal: find information of email, position, and country of institute
    text = scrape_text_information(url)

def main():
    N = 5
    api_key = readf('../googlekey')
    search_engine_id = readf('../engineid')
    names = readf('../format_name/input_name')
    names = names.split('\n')

    url_list = []

    for name in names:
        print()
        print(f'Choose url for {name}')
        startN = 0
        while True:
            results = google_search(name, search_engine_id, api_key, startN, N)
            for i, result in enumerate(results):
                print(i, result['url'])
            userchoice = input('choose result (n for next 5) (enter to skip)')

            if userchoice in ''.join([str(i) for i in range(N)]):
                userchoice = int(userchoice)
                url = results[userchoice]['url']
                url_list.append(url)
                break
            elif userchoice == 'n':
                startN += N
            else:
                url_list.append('')
                break

        if (len(url_list)+1)%10 == 0:
            print()
            print('last 10 results')
            print(url_list[-10:])
            print('saving....')
            with open('result_url.txt', 'w') as f:
                f.write('\n'.join(url_list))

def test():
    N = 5
    startN = 0
    api_key = readf('../googlekey')
    search_engine_id = readf('../engineid')
    names = readf('../format_name/input_name')
    names = names.split('\n')

    results = google_search(names[1], search_engine_id, api_key, startN, N)
    for i, result in enumerate(results):
        print(f'[result {i}]')
        for keywd in ['title', 'snippet', 'url']:
            print(f'{keywd}: {result[keywd]}')


if __name__ == '__main__':
    # main()
    test()
    input()
    import re
    scrape = scrape_text_information('https://faculty.rpi.edu/lydia-manikonda')
    n = re.sub(r'\n+', '\n', scrape)
    n = re.sub(r' +', ' ', n)
    n = ' '.join(n.split()[:3000])
    print(n)
    # import code
    # code.interact(local=locals())
    print()
        