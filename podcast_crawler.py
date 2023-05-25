import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

urls = [
    'https://www.stitcher.com/show/super-soul-8521721',
    'https://www.stitcher.com/show/the-plot-thickens-podcast',
    'https://www.stitcher.com/show/jeff-lewis-has-issues',
    'https://www.stitcher.com/show/unladylike',
    'https://www.stitcher.com/show/the-problem-with-jon-stewart',
    'https://www.stitcher.com/show/wiser-than-me-with-julia-louis-dreyfus',
    'https://www.stitcher.com/show/cold',
    'https://www.stitcher.com/show/the-deck-investigates',
    'https://www.stitcher.com/show/let-s-talk-off-camera-with-kelly-ripa',
    'https://www.stitcher.com/show/comedy-gold-minds-with-kevin-hart',
    'https://www.stitcher.com/show/hbos-succession-podcast',
    'https://www.stitcher.com/show/bedtime-stories-of-the-ingleside-inn',
    'https://www.stitcher.com/show/la-brega',
    'https://www.stitcher.com/show/weird-finance',
    'https://www.stitcher.com/show/dateline-2',
    'https://www.stitcher.com/show/klepper',
    'https://www.stitcher.com/show/levar-burton-reads',
    'https://www.stitcher.com/show/not-skinny-but-not-fat'
]

podcasts = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    podcast_list = soup.find_all('div', class_='ma-0 episode mobileItemListPadding v-list-item v-list-item--link theme--light')

    for podcast_item in podcast_list:
        podcast = {}
        
        podcast["id"] = len(podcasts) + 1
        podcast["episodio"] = podcast_item.find('div', class_='text-truncate text-grey5').get_text().strip()
        duracao = podcast_item.find('div', class_='v-list-item__subtitle text-grey4 episodeInfo').get_text().strip().split('|')
        podcast["duracao"] = duracao[0].strip()
        podcast["data"] = duracao[1].strip()

        podcast["data"] = datetime.strptime(podcast["data"], "%b %d, %Y").strftime("%Y-%m-%d")

        link = podcast_item.find('a', class_='text-none episode-link')['href']
        podcast["link"] = 'www.stitcher.com' + link
        subtitulo = podcast_item.find('div', class_='v-list-item__subtitle episodeDescription hidden-sm-and-down-bak hidden-xs-only text-grey5 mt-0 mt-md-1').get_text().strip().split('.')
        podcast["descricao"] = subtitulo[0].strip()
        
        podcasts.append(podcast)

with open('podcasts.json', 'w', encoding='UTF-8') as f:
    json.dump(podcasts, f, indent=2)
