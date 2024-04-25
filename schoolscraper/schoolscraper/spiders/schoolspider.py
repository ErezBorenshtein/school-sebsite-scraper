from time import sleep

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
                'dnn$ctr7126$TimeTableView$ClassesList': value,
                'dnn$ctr7126$TimeTableView$MainControl$WeekShift': "0",
                'dnn$ctr7126$TimeTableView$ControlId': "8"
            }
            self.log(f'Now logging {value}..')
            yield FormRequest.from_response(response, formdata=data, callback=self.parse_school, meta={'value': value})
            sleep(2.0)

    def parse_school(self, response):
        def extract_text_in_parentheses(text):  # remove everything that is not inside parenthesis
            pattern = r'\(([^)]*)\)'
            matches = re.findall(pattern, text)
            return matches

        dfs = pd.read_html(response.text)
        for i, df in enumerate(dfs):
            if i == 11:
                df.drop(columns=0, inplace=True)
                df.drop(0, inplace=True)
                df = df.map(lambda x: extract_text_in_parentheses(str(x)))  # keep only the classes
                self.final_dfs.append(df)  # append the dataframe into the array of final dataframes

    def closed(self, reason):
        def combine_dataframes(dataframes):
            # Create an empty dataframe to store the combined data
            combined_df = pd.DataFrame()

            # Iterate over each dataframe in the input array
            for dataframe in dataframes:
                # Iterate over each row in the dataframe
                for index, row in dataframe.iterrows():
                    # Iterate over each column in the row
                    for col_name, cell_value in row.items():
                        if isinstance(cell_value, list):
                            # if it's a list convert to string
                            combined_df.at[index, col_name] = ', '.join(map(str, cell_value))
                        else:
                            # Otherwise store value directly
                            combined_df.at[index, col_name] = cell_value

            return combined_df

        df = combine_dataframes(self.final_dfs)  # combine all the dataframes
        df.to_csv("result.csv")  # write to file named result.csv
