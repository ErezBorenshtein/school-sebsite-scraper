import bs4
import pandas as pd
import re
import time
from create_room_schedule import add_room_schedule_to_csv
from create_tamplate import create_schedule
from schoolscraper.schoolscraper.spiders.schoolspider import SchoolspiderSpider
from scrapy.crawler import CrawlerProcess
import subprocess

def run_spider(num):
    process = CrawlerProcess()
    process.crawl(SchoolspiderSpider, classNumber=num)
    process.start()
    time.sleep(3)  # Adjust the delay as needed
    process.stop()

def main():
    for i in range(38):
        print(f"Class number: {i}")
        run_spider(i)
        add_room_schedule_to_csv('school.html', 'schedule_template.csv')
        time.sleep(3)  # Adjust the delay as needed
    print("Done")

if __name__ == "__main__":
    create_schedule()  # Create the initial schedule template
    main()

    
