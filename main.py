"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import requests, csv
from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
from stackoverflow_scraper import superscraping as stackoverflow_superscraping
from WWR_scraper import superscraping as WWR_superscraping
from remoteok_scraper import superscraping as remoteok_scraper

app = Flask("Scraper_of_RemotableJops")

db = {}
cashlist = []


@app.route("/")
def inputpage():
    global cashlist
    return render_template("inputpage.html", cashlist=cashlist)


# {타이틀:[회사명,지원링크]}
@app.route("/resultpage")
def resultpage():
    term = request.args.get("searchingBy")
    term = term.lower()
    global cashlist
    if term in db:
        BIG_LIST = db[term]
        Total_number = len(BIG_LIST)
    else:
        try:
            BIG_LIST = []
            stackoverflow = stackoverflow_superscraping.scraping(term)
            BIG_LIST.extend(list(stackoverflow.items()))
            weworkremotely = WWR_superscraping.scraping(term)
            BIG_LIST.extend(list(weworkremotely.items()))
            remoteok = remoteok_scraper.scraping(term)
            BIG_LIST.extend(list(remoteok.items()))
            print(BIG_LIST)
            Total_number = len(BIG_LIST)
            cashlist.append(term)
            db[term] = BIG_LIST
        except:
            BIG_LIST = ["없음", ("가공한 URL로 정보를 받아올수 없습니다. 이전화면으로 돌아가십시오", "", "")]
            Total_number = "없음"
    return render_template(
        "resultpage.html", BIG_LIST=BIG_LIST, Total_number=Total_number, term=term
    )


def export_csv(term):
    file = open(f"scraping for {term}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Apply link"])
    for list in db[term]:
        title = list[0]
        company = list[1][0]
        link = list[1][1]
        writer.writerow([title, company, link])
    file.close()


@app.route("/export")
def export():
    try:
        term = request.args.get("searchingBy")
        if not term:
            raise Exception()
        term = term.lower()
        export_csv(term)
    except:
        return redirect("/")
    return render_template("download.html", BIG_LIST=db[term], term=term)


@app.route("/download")
def download():
    try:
        term = request.args.get("searchingBy")
        if not term:
            raise Exception()
        term = term.lower()
        export_csv(term)
    except:
        return redirect("/")
    return send_file(f"scraping for {term}.csv")


app.run(host="0.0.0.0")
