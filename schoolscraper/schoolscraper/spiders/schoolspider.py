import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser
import pandas as pd
import re


class SchoolSpider(scrapy.Spider):
    name = "schoolspider"
    start_urls = ["https://beitbiram.iscool.co.il/default.aspx"]

    def __init__(self, classNumber=1, *args, **kwargs):
        super(SchoolSpider, self).__init__(*args, **kwargs)
        self.classNumber = classNumber
        self.final_df = pd.DataFrame

    def parse(self, response):
        classes_values = response.css("select#dnn_ctr7126_TimeTableView_ClassesList option::attr(value)").extract()

        for value in classes_values:
            data = {
                '__EVENTTARGET': 'dnn$ctr7126$TimeTableView$btnTimeTable',
                'dnn$ctr7126$TimeTableView$ClassesList': value,
                'dnn$ctr7126$TimeTableView$ControlId': "8",
            }
            yield FormRequest.from_response(response, formdata=data, callback=self.parse_school)

    def parse_school(self, response):
        def extract_text_in_parentheses(text):
            pattern = r'\(.*?\)'
            matches = re.findall(pattern, text)
            return matches

        dfs = pd.read_html(response.text)
        for i, df in enumerate(dfs):
            if i == 11:
                df.drop(columns=0, inplace=True)
                df.drop(0, inplace=True)
                df = df.applymap(lambda x: extract_text_in_parentheses(str(x)))
