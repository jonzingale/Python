# https://xlrd.readthedocs.io/en/latest/api.html
from pdb import set_trace as st
import xlrd
import csv
import re

HEADER = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

def csv_from_excel():
    wb = xlrd.open_workbook('seoAudit.xlsx')

    for sh in wb.sheets():
      your_csv_file = open('audit/'+sh.name+'.csv', 'w')
      wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

      for rownum in range(sh.nrows):
          wr.writerow(sh.row_values(rownum))

      your_csv_file.close()

# returns all sheets as csvs:
# csv_from_excel()

def urlsToSitemap():
  file = open("audit/urls.csv", "r")
  body = ""
  for url in file:
    body += '<url><loc>' + url + '</loc><lastmod>2018-09-26</lastmod></url>'
  xml = HEADER + body + '</urlset>'

  file = open("sitemap_1.xml", "w")
  file.write(xml)
  file.close()

# compose sitemap from valid urls
# urlsToSitemap()

def getUrls():
  wb = xlrd.open_workbook('seoAudit.xlsx')
  file = open("urls.csv", "a")

  urlText = wb.sheets()[0].col(0)[1:]
  urls = []
  for u in urlText:
    mm = re.match("text:\'(.*)\'", str(u))
    if mm: file.write(mm[1]+"\n")
  file.close()

# get Urls from excel and create csv
getUrls()
# st()
