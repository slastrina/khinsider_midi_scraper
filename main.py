import os
from collections import defaultdict
import concurrent.futures

import requests
from bs4 import BeautifulSoup

workers = 10
output_path = 'output'
content_url = 'https://www.khinsider.com/midi'

counts = defaultdict(int)

def process_href(href, sub_path):
    # make a request to the href and print the response content
    response = requests.get(href)
    td_tags = BeautifulSoup(response.content, 'html.parser').findAll('td')
    for td in td_tags:
        a_tags = td.find_all('a')
        for a in a_tags:
            game_href = a.get('href')
            game_href_text = a.text

            # Create Sub-path
            game_sub_path = os.path.join(sub_path, game_href_text)
            try:
                os.mkdir(game_sub_path)
            except FileExistsError:
                pass

            # Get the songs
            game_response = requests.get(game_href)
            game_td_tags = BeautifulSoup(game_response.content, 'html.parser').findAll('td')
            for game_td in game_td_tags:
                game_a_tags = game_td.find_all('a')
                for game_a in game_a_tags:
                    song_href = game_a.get('href')
                    song_href_filename = os.path.basename(song_href)

                    song_output_path = os.path.join(game_sub_path, song_href_filename)

                    print(f'Downloading: {song_href_filename} to {song_output_path}')

                    try:
                        r_song = requests.get(song_href)
                        with open(f'{song_output_path}', 'wb') as f:
                            for chunk in r_song.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                    except FileExistsError:
                        pass
                    except Exception as ex:
                        print(ex)



if not os.path.exists(output_path):
    os.mkdir(output_path)

print(f'Scraping: {content_url}')

request = requests.get(content_url)

if request.status_code == 404:
    print("Site Unreachable (404)")
    exit(1)

td_tags = BeautifulSoup(request.content, 'html.parser').findAll('td')

# create a thread pool with a maximum of 10 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    # loop through all 'td' tags and find the 'a' tags
    for td in td_tags:
        a_tags = td.find_all('a')
        for a in a_tags:
            href = a.get('href')
            href_text = a.text

            # Create Sub-path
            sub_path = os.path.join(output_path, href_text)
            try:
                os.mkdir(sub_path)
            except FileExistsError:
                pass

            # submit the 'process_href' function with the 'href' to the thread pool
            executor.submit(process_href, href, sub_path)

print('\nDone')