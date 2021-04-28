import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def get_soup(term):
    term = term.lower()
    url = f"https://remoteok.io/remote-{term}-jobs"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


class superscraping:
    def scraping(term):
        dictionary = {}
        soup = get_soup(term)
        bigtable = soup.find("table", id="jobsboard")
        td_list = bigtable.find_all("td", class_="company position company_and_position")
        for td in td_list:
            Company = td.find("h3")
            Company = Company.string if Company != None else "No Company"
            Title = td.find("h2")
            Title = Title.string if Title != None else "No Title"
            From = "→ from remoteok ←"
            Apply = td.find("a", class_="preventLink")
            Apply = f"https://remoteok.io{Apply['href']}" if Apply != None else "No Apply Link"
            print(f"remoteok || 딕셔너리에 추가 = {Title}")
            dictionary[Title] = [Company.strip(), Apply, From]
        return dictionary
