import scrapy
from scrapy import FormRequest

class SchoolSpider(scrapy.Spider):
    name = "schoolspider"
    allowed_domains = ["ironih.iscool.co.il"]
    start_urls = ["https://ironih.iscool.co.il"]

    def __init__(self, classNumber=1, *args, **kwargs):
        super(SchoolSpider, self).__init__(*args, **kwargs)
        self.classNumber = classNumber

    def parse(self, response):
        classes_values = response.css("select#dnn_ctr3413_TimeTableView_ClassesList option::attr(value)").extract()

        print("classes_values", classes_values, "len: ", len(classes_values))

        if len(classes_values) == 0:
            self.logger.error("No classes found")
            return
        
        requests = {
            '__EVENTTARGET': 'dnn$ctr3413$TimeTableView$btnTimeTable',
            'dnn$ctr3413$TimeTableView$ClassesList': classes_values[int(self.classNumber)-1],
            'dnn$ctr3413$TimeTableView$ControlId':'1',
        }
        self.logger.info(f"class value: {classes_values[int(self.classNumber)]}")

        # Debugging info
       # self.logger.info(f"Form data: {requests}")

        yield FormRequest.from_response(response, formdata=requests, callback=self.parse_school)

    def parse_school(self, response):
        place_holder_data = response.css("div.PlaceHolder").getall()
        self.logger.info(f"current class: {response.css('select#dnn_ctr3413_TimeTableView_ClassesList option[selected]::text').get()}")

        # Debugging info
        #self.logger.info(f"Place holder data: {place_holder_data}")

        if place_holder_data:
            with open(r"C:\Users\Desktop\OneDrive\erez\School_website_scraper\school-sebsite-scraper\school.html", "w", encoding="utf-8") as f:
                f.write("\n".join(place_holder_data))
        else:
            self.logger.warning("No data found in div.PlaceHolder")
