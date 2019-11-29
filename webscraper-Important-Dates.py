from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import datetime as dt
import re
import copy
import MySQLdb    

dataBase = MySQLdb


userInput1 = str(input("Please Provide with Calendar link: "))
userInput2 = str(input("Please Provide a file name ending in .sql: "))
userInput3 = str(input("Please select student type: (undergrad or graduate): "))

url = userInput1

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
      event = data.text.replace("\r\n\t\t\t",' ')

      # assignment based on regex
      time = re.match(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",event)
      doubleTime = re.match(r"[ADFJMNOS]\w* [\d]{1,2} to [\d]{1,2}, [\d]{4}", event)
      doubleDates = re.match(r"[ADFJMNOS]\w* [\d]{1,2} and [\d]{1,2}, [\d]{4}", event)
      crossYear = re.match(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4} to [ADFJMNOS]\w* [\d]{1,2}, [\d]{4}", event)
      
      global updateEvent

      if crossYear:

        dates = re.split(r"\ to \ |\ |,\ ",event)
        # get the start date numbers and join
        startDates = " ".join([dates[0],dates[1],dates[2]])
        # get the end date values and join
        endDates = " ".join([dates[4],dates[5],dates[6]])
        startTime = dt.strptime(startDates, "%B %d %Y")
        endTime = dt.strptime(endDates, "%B %d %Y")
        finalDates = ' to '.join([str(startTime), str(endTime)])
        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2}, [\d]{4} to [ADFJMNOS]\w* [\d]{1,2}, [\d]{4}",str(finalDates), event)
        # print(event)
      # converts Month Day, Year
      elif time:
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
        endTime = dt.strptime(endDates, "%B %d %Y")
        #global variable for empty date
        updateEvent = str(startTime)

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
        endTime = dt.strptime(endDates, "%B %d %Y")
        updateEvent = str(startTime)
        finalDates = ' to '.join([str(startTime), str(endTime)])

        event = re.sub(r"[ADFJMNOS]\w* [\d]{1,2} and [\d]{1,2}, [\d]{4}",str(finalDates), event)

      else :
        # Fill in all the date values that are empty with date value
        # before it
        event = re.sub(r"\xa0", str(updateEvent), event)

      #append to list of cols
      list_of_cells.append(event)

    newCells = copy.deepcopy(list_of_cells[0])

    toSplit = re.match(r"[\d]{4}-[\d]{1,2}-[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2} to [\d]{4}-[\d]{1,2}-[\d]{1,2} [\d]{1,2}:[\d]{1,2}:[\d]{1,2}", newCells)
    
    global endTimes
    if toSplit:
      # print(toSplit.group())
      newSplit = toSplit.group().split(' to')
      endTimes = newSplit[1].replace("00:00:00","11:59:59")
    else:
      endTimes = newCells.replace("00:00:00","11:59:59")
    
    list_of_cells.append(endTimes)

    startDate = list_of_cells[0].split('to')

    strParts = list_of_cells[1].split('. ')

    global title, description
    if len(strParts) > 1:
      title = str(strParts[0])
      description = str(strParts[1])
    else:
      title= str(strParts[0])
      description = str(strParts[0])

    newTitle =str(dataBase.escape_string(title))
    newDesc =str(dataBase.escape_string(description))
    
    query = "INSERT INTO tbl_entries ( event_name, event_description, event_categories, event_tags, event_startdate, event_enddate, open_to, location_building, location_room, location_campus, location_other, start_hour, start_minute, start_ampm, end_hour, end_minute, end_ampm, contact_event_firstname, contact_event_lastname, contact_event_phonenumber, contact_event_phoneext, contact_event_email, contact_firstname, contact_lastname, contact_phonenumber, contact_phoneext, contact_email, event_url, event_url_protocol, upload_image, date_submitted, date_approved, repeated, repeat_freq, repeat_day, repeat_until, repeat_until_date, repeat_until_num, clickable, pending, approved, archived, cancelled, frontpage, submission_ip) VALUES "

    registrars = str(dataBase.escape_string("'Registar's'"))[1:]

    global values
    if userInput3 == 'undergrad':
      values = "(" + str(newTitle)[1:] + " ," + str(newDesc)[1:]+ ", '73', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0', '"+ startDate[0] + "','" + endTimes + "', '29', 0, '', 2, 'Ontario Tech', 0, 0, 'am', 11, 59, 'pm', "+ registrars +", 'Office', '905.721.3190', '', 'connect@uoit.ca', " + registrars + ", 'Office', '905.721.3190', '', 'connect@uoit.ca', '" + url + "', 'https', NULL, '" + str(dt.now())+ "', '" + str(dt.now()) + "', 0, '', '', 0, '" + str(dt.now()) + "', 0, 1, 0, 1, 0, 0, 0, '00.000.0.000'),"

    elif userInput3 == 'graduate':
      values = "(" + str(newTitle)[1:] + " ," + str(newDesc)[1:]+ ", '74', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0', '"+ startDate[0] + "','" + endTimes + "', '29', 0, '', 2, 'Ontario Tech', 0, 0, 'am', 11, 59, 'pm','School of Graduate', 'and Postdoctoral Studies', '905.721.8668', '6209', 'connect@uoit.ca', 'School of Graduate', 'and Postdoctoral Studies', '905.721.8668', '6209','connect@uoit.ca', '" + url + "', 'https', NULL, '" + str(dt.now())+ "', '" + str(dt.now()) + "', 0, '', '', 0, '" + str(dt.now()) + "', 0, 1, 0, 1, 0, 0, 0, '00.000.0.000'),"

    #append to rows
    list_of_rows.append(values)

lastString = str(list_of_rows.pop(len(list_of_rows)-1))
lastString = lastString[:-1] +';'
list_of_rows.append(lastString)

outfile = open(userInput2, "w") 
outfile.write(query)
for item in list_of_rows:
  outfile.write("%s\n" % item)
outfile.close 