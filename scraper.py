from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from datetime import datetime as dt
import re

url = 'http://calendar.uoit.ca/content.php?catoid=22&navoid=881'

# get data from the link
client = uReq(url)
pageHtml = client.read()
client.close()

# create parsabel html
html = soup(pageHtml, "html.parser")

header = html.h2
headTables= header.find_next_siblings("table")

list_of_rows = []

# Loop through the sibling tables of h2 and find tr
for i in headTables:
  rows = i.find_all("tr")

  # loop through all the tr's and find td's
  for j in rows:
    list_of_cells = []
    cols = j.find_all("td")

    # loop through all the td's and get data
    for data in cols:
      event = data.text
      
      # assignment based on regex
      time = re.match(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",event)
      doubleTime = re.match(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}", event)
      doubleDates = re.match(r"[ADFJMNOS]\w* [\d]{1,2} and [\d]{1,2}, [\d]{4}", event)
        
      global updateEvent

      # converts Month Day, Year
      if time:
        timeVal = dt.strptime(time.group(), "%B %d, %Y")
        updateEvent = timeVal
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",str(timeVal), event)
      
      # convets date in format: Month Day to Day, Year
      elif doubleTime:
        dates = re.split(r"\ to\ |\ |,\ ", event)
        startDates = " ".join([dates[0],dates[1],dates[3]])
        endDates = " ".join([dates[0],dates[2],dates[3]])
        startTime = dt.strptime(startDates, "%B %d %Y")
        updateEvent = str(startTime)
        endTime = dt.strptime(endDates, "%B %d %Y")
        finalDates = ' to '.join([str(startTime), str(endTime)])
        # print(finalDates)
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}",str(finalDates), event)
      
      # converts Month Day and Day, Year
      elif doubleDates:
        dates = re.split(r"\ and\ |\ |,\ ", event)
        startDates = " ".join([dates[0],dates[1],dates[3]])
        endDates = " ".join([dates[0],dates[2],dates[3]])
        startTime = dt.strptime(startDates, "%B %d %Y")
        updateEvent = str(startTime)
        endTime = dt.strptime(endDates, "%B %d %Y")
        finalDates = ' to '.join([str(startTime), str(endTime)])
        # print(finalDates)
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} and [\d]{1,2}, [\d]{4}",str(finalDates), event)
      
      # print(updateEvent)
      else :
        # print(updateEvent)

        event = re.sub(r"\xa0", str(updateEvent), event)

      #append to list of cols
      list_of_cells.append(event)
    
    #append to rows
    list_of_rows.append(list_of_cells)

outfile = open("./events.csv", "w")
writer = csv.writer(outfile)    
writer.writerow(["Date", "Event(s)"])
writer.writerows(list_of_rows)