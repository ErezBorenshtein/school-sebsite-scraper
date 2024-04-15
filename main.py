import csv
from bs4 import BeautifulSoup
import re
from multiprocessing import Process
from schoolscraper.schoolscraper.spiders.schoolspider import SchoolSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

schedule = [[[] for _ in range(6)] for _ in range(13)]  # Assuming 13 hours, 6 days

def add_room_schedule_to_list(html_file):
    global schedule
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            html_code = file.read()
    except FileNotFoundError:
        print(f"Error: HTML file '{html_file}' not found.")
        return

    soup = BeautifulSoup(html_code, 'html.parser')
    rows = soup.find_all('tr')

    if len(rows) - 1 > len(schedule):
        schedule.extend([[''] * 6 for _ in range(len(rows) - 1 - len(schedule))])

    for i, row in enumerate(rows[1:], 0):
        cells = row.find_all('td', class_='TTCell')

        for _ in range(len(cells) - len(schedule[i])):
            schedule[i].append('')

        for j, cell in enumerate(cells, 0):
            lessons = cell.find_all('div', class_='TTLesson')
            room_numbers = []
            for lesson in lessons:
                lesson_text = lesson.get_text().strip()
                room_matches = re.findall(r'\d{3}', lesson_text)
                room_numbers.extend(room_matches)

            schedule[i][j] = ','.join(room_numbers)

def crawl_and_update(class_number):
    global schedule
    print(f"Scraping data for class number {class_number}...")
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(SchoolSpider, classNumber=class_number)
        process.start(stop_after_crawl=True)
    except Exception as e:
        print(f"Error occurred during scraping: {e}")
        return

    try:
        add_room_schedule_to_list('school.html')
    except Exception as e:
        print(f"Error occurred during schedule update: {e}")
    print("Schedule updated:", schedule)

def write_schedule_to_csv(filename):
    global schedule
    
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = list(range(0, 14))

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + days)
        writer.writerow(["Hour"] + [""] * len(days))
        
        for hour, hour_schedule in zip(hours, schedule):
            flattened_row = [','.join(cell) if isinstance(cell, list) else cell for cell in hour_schedule]
            writer.writerow([f"{hour}"] + flattened_row)

def main():
    global schedule
    processes = []
    for i in range(27, 31):  # Assuming 50 classes
        p = Process(target=crawl_and_update, args=(i,))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

    print("All processes completed.")
    print("Schedule:", schedule)
    
    write_schedule_to_csv('schedule.csv')  # Move this line outside of the loop

    print("Schedule saved as 'schedule.csv'.")

if __name__ == "__main__":
    main()
