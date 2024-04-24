import scrapy
from scrapy import FormRequest
import pandas as pd
import re


class SchoolSpider(scrapy.Spider):
    name = "schoolspider"
    start_urls = ["https://beitbiram.iscool.co.il/default.aspx"]

    def __init__(self, classNumber=1, *args, **kwargs):
        super(SchoolSpider, self).__init__(*args, **kwargs)
        self.classNumber = classNumber
        self.final_dfs = []

    def parse(self, response):
        classes_values = response.css("select#dnn_ctr7126_TimeTableView_ClassesList option::attr(value)").extract()

        self.log(f'\nclasses values: {classes_values}\n')

        for value in classes_values:
            data = {
                '__EVENTTARGET': 'dnn$ctr7126$TimeTableView$btnTimeTable',
                'dnn$ctr7126$TimeTableView$ClassesList': value,
                'dnn$ctr7126$TimeTableView$ControlId': "8"
            }
            self.log(f'Now logging {value}..')
            yield FormRequest.from_response(response, formdata=data, callback=self.parse_school, meta={'value': value})

    def parse_school(self, response):
        def extract_text_in_parentheses(text):
            pattern = r'\(.*?\)'
            matches = re.findall(pattern, text)
            return matches

        dfs = pd.read_html(response.text)
        for i, df in enumerate(dfs):
            if i == 11:  # Assuming the 11th DataFrame contains schedule data
                df.drop(columns=0, inplace=True)
                df.drop(0, inplace=True)
                df = df.applymap(lambda x: extract_text_in_parentheses(str(x)))
                self.final_dfs.append(df)

    def closed(self, reason):
        for i, df in enumerate(self.final_dfs):
            df.to_csv(f'schedule_{i}.csv', index=False)
