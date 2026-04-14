#Porter Collins

import requests
from bs4 import BeautifulSoup

def process_talk(url, standard_works_dict):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Speaker
    speaker_tag = soup.find('p', class_='author-name')
    speaker = speaker_tag.text.replace("By ", "").strip().replace('\xa0', ' ')

    # Title
    title_tag = soup.find('h1')
    title = title_tag.text.strip().replace('\xa0', ' ')

    # Kicker
    kicker_tag = soup.find('p', class_='kicker')
    kicker = kicker_tag.text.strip().replace('\xa0', ' ')

    # Footnotes
    footnotes_section = soup.find('footer', class_='notes')
    footnotes_text = footnotes_section.text if footnotes_section else ""

    # Copy dictionary
    talk_data = standard_works_dict.copy()

    # Count references
    for book in talk_data:
        if book not in ["Speaker_Name", "Talk_Name", "Kicker"]:
            talk_data[book] = footnotes_text.count(book)

    # Add main info
    talk_data["Speaker_Name"] = speaker
    talk_data["Talk_Name"] = title
    talk_data["Kicker"] = kicker

    return talk_data
