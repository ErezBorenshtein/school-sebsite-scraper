import scrapy
from scrapy import FormRequest
import pandas as pd

class SchoolspiderSpider(scrapy.Spider):
    name = "schoolspider"
    allowed_domains = ["ironih.iscool.co.il"]
    start_urls = ["https://ironih.iscool.co.il"]


    def parse(self, response):
        requests = {
            '__EVENTTARGET': 'dnn$ctr3413$TimeTableView$btnTimeTable',
            'dnn$ctr3413$TimeTableView$ClassesList': '1',
            'dnn$ctr3413$TimeTableView$ControlId':'1',
        }
        yield FormRequest.from_response(response, formdata=requests, callback=self.parse_school)


        """for i in range(1,38):
            print("i",i)
            print("******")
            requests['dnn$ctr3413$TimeTableView$ClassesList'] = str(i)
            
            time.sleep(1)  # Add a delay of 2 seconds between requests to avoid triggering rate limits
            print("******")"""

    def parse_school(self, response):

        place_holder_data = response.css("div.PlaceHolder").getall() # Extract the HTML code of the div.PlaceHolder element

        if place_holder_data:
            with open("school.html", "w", encoding="utf-8") as f: 
                f.write("\n".join(place_holder_data)) # Write the HTML code to a file
        else:
            self.logger.warning("No data found in div.PlaceHolder") # Log a warning message if no data is found

