from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from datetime import datetime as dt
import re

url = 'http://calendar.uoit.ca/content.php?catoid=22&navoid=881'

client = uReq(url)
pageHtml = client.read()
client.close()

html = soup(pageHtml, "html.parser")

header = html.h2
headTables= header.find_next_siblings("table")

list_of_rows = []
for i in headTables:
  rows = i.find_all("tr")
  for j in rows:
    list_of_cells = []
    # loop through rows and separate td's
    cols = j.find_all("td")
    for data in cols:
    # loop through the td's and get values
      event = data.text

        # convert Date to formatable time
      time = re.match(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",event)
      doubleTime = re.match(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}", event)
        
      if time:
        timeVal = dt.strptime(time.group(), "%B %d, %Y")
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",str(timeVal), event)
      elif doubleTime:
        dates = re.split(r"\ to\ |\ |,\ ", event)
        startDates = " ".join([dates[0],dates[1],dates[3]])
        endDates = " ".join([dates[0],dates[2],dates[3]])
        
        startTime = dt.strptime(startDates, "%B %d %Y")
        # print(startTime)
        endTime = dt.strptime(endDates, "%B %d %Y")
        # print(endTime)
        finalDates = ' to '.join([str(startTime), str(endTime)])
        print(finalDates)
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}",str(finalDates), event)
        # print(event)

      list_of_cells.append(event)
    list_of_rows.append(list_of_cells)
  
outfile = open("./events.csv", "w")
writer = csv.writer(outfile)    
writer.writerow(["Date", "Event(s)"])
writer.writerows(list_of_rows)