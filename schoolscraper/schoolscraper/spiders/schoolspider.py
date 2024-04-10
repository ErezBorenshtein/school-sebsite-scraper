import scrapy
from scrapy import FormRequest
import pandas as pd

class SchoolspiderSpider(scrapy.Spider):
    name = "schoolspider"
    allowed_domains = ["ironih.iscool.co.il"]
    start_urls = ["https://ironih.iscool.co.il"]

    def __init__(self, classNumber=1, *args, **kwargs):
        super(SchoolspiderSpider, self).__init__(*args, **kwargs)
        self.classNumber = classNumber

    def parse(self, response):
        classes_values = response.css("select#dnn_ctr3413_TimeTableView_ClassesList option::attr(value)").extract()
        requests = {
            '__EVENTTARGET': 'dnn$ctr3413$TimeTableView$btnTimeTable',
            'dnn$ctr3413$TimeTableView$ClassesList': classes_values[self.classNumber],
            'dnn$ctr3413$TimeTableView$ControlId':'1',
        }
    
        yield FormRequest.from_response(response, formdata=requests, callback=self.parse_school)

    def parse_school(self, response):

        place_holder_data = response.css("div.PlaceHolder").getall() # Extract the HTML code of the div.PlaceHolder element

        if place_holder_data:
            with open(r"C:\Users\Desktop\OneDrive\erez\School_website_scraper\school-sebsite-scraper\school.html", "w", encoding="utf-8") as f: 
                f.write("\n".join(place_holder_data)) # Write the HTML code to a file
        else:
            self.logger.warning("No data found in div.PlaceHolder") # Log a warning message if no data is found
