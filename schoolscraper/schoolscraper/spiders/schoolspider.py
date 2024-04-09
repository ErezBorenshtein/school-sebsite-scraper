import scrapy
from scrapy import FormRequest
import time
import pandas as pd

class SchoolspiderSpider(scrapy.Spider):
    name = "schoolspider"
    allowed_domains = ["ironih.iscool.co.il"]
    start_urls = ["https://ironih.iscool.co.il"]


    def parse(self, response):
        class_list =[]
        requests = {
            '__EVENTTARGET': 'dnn$ctr3413$TimeTableView$btnTimeTable',
            'dnn$ctr3413$TimeTableView$ClassesList': '27',
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

        timetable_table = response.css('table.TTTable')

        if timetable_table:
            rows = timetable_table.css('tr')
            data = []
            for row in rows:
                cells = row.css('td')
                row_data = []
                for cell in cells:
                    cell_data = cell.css('::text').get()
                    row_data.append(cell_data.strip() if cell_data else '')  # Strip whitespace and handle empty cells
                data.append(row_data)

            df = pd.DataFrame(data)
            df.to_csv('timetable.csv', index=False, header=False, encoding='utf-8-sig')
            self.logger.info('Timetable data saved to timetable.csv')
        else:
            self.logger.info('Timetable table not found in the response')

        """timetable_table = response.css('table.TTTable')

        if timetable_table:
            rows = timetable_table.css('tr')
            for row in rows:
                cells = row.css('td')
                for cell in cells:
                    # Extract data from each cell as needed
                    cell_data = cell.css('::text').get()
                    print(cell_data)
        else:
            self.logger.info('Timetable table not found in the response')"""


        #table_rows = response.css("tr::text").getall()
        #lessons = response.css("td.TTcell::text").getall()
        #cname = response.css("b::text").getall()
        #print(response.css("div::text").getall())
        #print("something",response.css("div.PlaceHolder").getall())
        #print("something",response.text)
        #print("something",response.css("tr").getall())
        #print(response.xpath("//select/option/text()").getall())
        
        
        #print("table_rows:", table_rows)
        #print("lessons:", lessons)

        """day = response.css("td.CTitle::text").get()
        first_class = response.css("td.TTLesson::text").get()
        print("Day:", day)
        print("first_class:", first_class)"""
