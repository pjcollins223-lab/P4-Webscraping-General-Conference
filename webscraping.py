# Sarah Walker
# this program scrapes the talks from the April 2026 General Conference

from bs4 import BeautifulSoup
import requests
import main

# get valid talk links from the church website
def get_talk_urls() :
    # load main conference page
    oResponse = requests.get("https://www.churchofjesuschrist.org/study/general-conference/2026/04?lang=eng")
    soup = BeautifulSoup(oResponse.text, 'html.parser')

    # find all the a tags and get the links if it leads to an actual conference talk
    links = soup.find_all('a')

    # stores links to talks
    talk_urls = []
    base_url = "https://www.churchofjesuschrist.org"

    for link in links :
        href = link.get("href")
        if href:
            # make sure link is a talk link, not a full session link 
            if "/study/general-conference/2026/04/" in href :
                # add link if it is not a session video
                if "session" not in href.lower():
                    full_url = base_url + href
                    if full_url not in talk_urls: 
                        talk_urls.append(full_url)

    return talk_urls

# retrieves talk urls from get_talk_urls and loops through the titles. If valid, pass it to process_talk
def loop_through_talks():
    urls = get_talk_urls()

    for url in urls:
        print(f"trying to scrape url: {url}")

        oResponse = requests.get(url)
        soup = BeautifulSoup(oResponse.text, 'html.parser')

        article = soup.find("article", id="main")

        if article:
            content_type = article.get("data-content-type")

            # filter out anything marked as business
            if content_type == "general-conference-business":
                print("Business, not a talk. Skipping...")
                
            # real talks
            if content_type == "general-conference-talk":
                print(content_type)
                main.process_talk(url)