# Ontario Tech University Web Scrapers

## Repository Contents:

### Requirements:
   1. __Python3__.
   2. __Python3 Libraries__:
        - ___Pandas___: For creating data frames.
        - ___bs4___: For the package BeautifulSoup which parses web pages.
        - ___urllib.request___: For the urlopen package to open links to the pages that need to be parsed.
   3. __Special Import Case__:
       - ___MySQLdb___: for the important dates parser, helps with escaped strings.
       - ___re___: used for regex matching.
       - ___copy___: used to copy and manipulate data.
       - ___datetime___: used to convert to datetime.
       
### Web Scrapers:
   1. __Important Dates Scraper__:
        - Used for parsing and creating MySQL queries from the Important Dates page.
        - Link to Important Dates page: https://bit.ly/37RmY4m
        
   2. __Accordion Parser__:
        - This scraper is used parse any FAQ's that use Accordion's.
        - Example of Accordion page: https://bit.ly/33xnEsD
     
   3. __Strong Tags Parser__:
        - This scraper parses pages that have information in ```<strong></strong>``` tags. 
        - Example of page with strong tags: https://bit.ly/2OALU8Z
        
