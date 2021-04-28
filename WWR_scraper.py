import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


def get_soup(term):
    term = term.lower()
    url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


class superscraping:
    def scraping(term):
        soup = get_soup(term)
        article_list_soup = soup.find_all("article")
        dictionary = {}
        for article in article_list_soup:
            title_category = article.find("h2").find("a").string
            soup_1 = article.find("ul")
            soup_2 = soup_1.find_all("li")
            for soup in soup_2:
                a_tag = soup.find_all("a")
                Alist = a_tag
                if len(str(a_tag)) <= 150:
                    print("WWR || 파지네이션을 감지하였습니다 이 태그는 continue처리 합니다 \narticle마지막이기 때문일 수 있습니다")
                    continue
                try:
                    a_tag = a_tag[1]
                except IndexError:
                    print("WWR || a_tag가 하나이므로 인덱싱값 '0'을 대신 적용합니다")
                    a_tag = a_tag[0]
                Apply_link = a_tag["href"]
                Apply_link = f"https://weworkremotely.com{Apply_link}"
                try:
                    Company = a_tag.find("span", class_="company").string
                except AttributeError:
                    print("WWR || 예외적인 경우를 발견하였으며 인덱싱값 '0'을 대신 적용합니다")
                    a_tag = Alist[0]
                    Apply_link = a_tag["href"]
                    Apply_link = f"https://weworkremotely.com{Apply_link}"
                    Company = a_tag.find("span", class_="company").string
                if Company == None:
                    Company = "No Company"
                Title = a_tag.find("span", class_="title").string
                From = f"→ from weworkremotely to {title_category} category ←"
                dictionary[Title] = [Company.strip(), Apply_link, From]
                print(f"WWR || 딕셔너리에 추가 {Title}")
        return dictionary
