from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from datetime import datetime as dt
import re
import copy

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
        # global variable for storage of date value
        updateEvent = timeVal
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",str(timeVal), event)
      
      # convets date in format: Month Day to Day, Year
      elif doubleTime:
        dates = re.split(r"\ to\ |\ |,\ ", event)
        # get the start date numbers and join
        startDates = " ".join([dates[0],dates[1],dates[3]])
        # get the end date values and join
        endDates = " ".join([dates[0],dates[2],dates[3]])
        startTime = dt.strptime(startDates, "%B %d %Y")
        #global variable for empty dates
        updateEvent = str(startTime)
        
        endTime = dt.strptime(endDates, "%B %d %Y")
        finalDates = ' to '.join([str(startTime), str(endTime)])
        # print(finalDates)
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}",str(finalDates), event)
      
      # converts Month Day and Day, Year
      elif doubleDates:
        dates = re.split(r"\ and\ |\ |,\ ", event)
        # get the start date numbers and join
        startDates = " ".join([dates[0],dates[1],dates[3]])
        # get the end date values and join
        endDates = " ".join([dates[0],dates[2],dates[3]])
        startTime = dt.strptime(startDates, "%B %d %Y")
        #global variable for empty dates
        updateEvent = str(startTime)
        endTime = dt.strptime(endDates, "%B %d %Y")
        finalDates = ' to '.join([str(startTime), str(endTime)])

        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} and [\d]{1,2}, [\d]{4}",str(finalDates), event)

      else :
        # Fill in all the date values that are empty with date value
        # before it
        event = re.sub(r"\xa0", str(updateEvent), event)

      #append to list of cols
      list_of_cells.append(event)

    newCells = copy.deepcopy(list_of_cells[0])
    endTimes = newCells.replace("00:00:00","12:59:59")
    list_of_cells.append(endTimes)
      
    #append to rows
    list_of_rows.append(list_of_cells)


query = "INSERT INTO tbl_entries ( id, event_name, event_description, event_categories, event_tags, " + " event_startdate, event_enddate, open_to, location_building, location_room, location_campus, location_other, start_hour, start_minute, start_ampm, end_hour, end_minute, end_ampm, contact_event_firstname," + " contact_event_lastname, contact_event_phonenumber, contact_event_phoneext, contact_event_email, contact_firstname, contact_lastname, contact_phonenumber, contact_phoneext, contact_email,  " + "event_url, event_url_protocol, upload_image, date_submitted, date_approved, repeated, repeat_freq, " + "repeat_day, repeat_until, repeat_until_date, repeat_until_num, clickable, " + "pending, approved, archived, cancelled, frontpage, submission_ip) " + ")"

print(query)

outfile = open("./events.csv", "w")
writer = csv.writer(outfile)    
writer.writerow(["Start Date", "Description", "End Date"])
writer.writerows(list_of_rows)