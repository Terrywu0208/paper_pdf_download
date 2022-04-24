import requests
from bs4 import BeautifulSoup
import wget
import re

pmid = []
pattern = re.compile("doi: (.+).")
pdf_pattern = re.compile("(.+)#")

def download_pdf(doi_id):
    print(doi_id)
    url = f"https://sci-hub.se/{doi_id}"
    pdf_rq = requests.get(url)
    pdf_html = BeautifulSoup(pdf_rq.text)
    pdf_url_find = pdf_html.select("embed")
    pdf_url_filter = pdf_pattern.findall(pdf_url_find[0]["src"])
    pdf_url = "https:"+pdf_url_filter[0]
    pdf_url_find = pdf_html.select("embed")
    title = pdf_html.select("#citation > i")
    s = title[0].text
    title_slipt = s.split(".")[0]
    print(pdf_url)
    wget.download(pdf_url,out=title_slipt+".pdf")

for page_num in range(35,50):
    print(page_num)
    url = f'https://pubmed.ncbi.nlm.nih.gov/?term=geographic&filter=years.2009-2015&page={page_num}'
    pubmed_response = requests.get(url)
    response_text = BeautifulSoup(pubmed_response.text)
    topic_a = response_text.select(".docsum-journal-citation.full-journal-citation")
    for i in topic_a:
        doi = pattern.findall(i.text)
        pmid.extend(doi)
print(pmid)
for i in pmid:
    try:
        download_pdf(i)
    except:
        pass