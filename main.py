import bs4
import pandas as pd
import re
import time
from add_rooms_to_schedule import add_room_schedule_to_csv
from create_tamplate import create_schedule
from schoolscraper.schoolscraper.spiders.schoolspider import SchoolSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

def crawl_and_update(class_number):
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(SchoolSpider, classNumber=class_number)
    process.start(stop_after_crawl=True)  # Start the crawler and stop after crawl completes
    add_room_schedule_to_csv('school.html', 'schedule_template.csv')  # Update CSV after each crawl

def main():
    create_schedule()  # Create the initial schedule template

    processes = []
    for i in range(1, 38):
        print(f"Class number: {i}")
        p = Process(target=crawl_and_update, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()  # Wait for all processes to complete

    print("Done")

if __name__ == "__main__":
    main()
