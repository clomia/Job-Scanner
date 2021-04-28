import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def get_soup(term):
    term = term.lower()
    url = f"https://stackoverflow.com/jobs?r=true&q={term}"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


class superscraping:
    def scraping(term):
        soup = get_soup(term)
        soup_1 = soup.find("div", class_="listResults")
        soup_2 = soup_1.find_all("div", class_="grid--cell fl1")
        dictionary = {}
        for soup in soup_2:
            Apply_link = soup.find("a", class_="s-link stretched-link")["href"]
            Apply_link = f"https://stackoverflow.com/{Apply_link}"
            Title = soup.find("a", class_="s-link stretched-link")["title"]
            From = "→ from stackoverflow ←"
            Company = soup.find("h3", class_="fc-black-700 fs-body1 mb4").find("span").string
            if Company == None:
                Company = "No Company"
            print(f"stackoverflow || 딕셔너리에 추가 {Title}")
            dictionary[Title] = [Company.strip(), Apply_link, From]
        return dictionary
