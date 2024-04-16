import csv
from bs4 import BeautifulSoup
import re
from multiprocessing import Process
from schoolscraper.schoolscraper.spiders.schoolspider import SchoolSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Dictionary to store the schedule data
schedule = {}

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

    for i, row in enumerate(rows[1:], 0):
        cells = row.find_all('td', class_='TTCell')

        for j, cell in enumerate(cells, 0):
            lessons = cell.find_all('div', class_='TTLesson')
            room_numbers = []
            for lesson in lessons:
                lesson_text = lesson.get_text().strip()
                room_matches = re.findall(r'\d{3}', lesson_text)
                room_numbers.extend(room_matches)

            if (i, j) not in schedule:
                schedule[(i, j)] = set()
            schedule[(i, j)].update(room_numbers)

def add_to_csv():
    global schedule

    # Create a list of lists to store the timetable data
    timetable = [['' for _ in range(7)] for _ in range(13)]

    # Fill the timetable with the schedule data
    for (hour, day), used_classes in schedule.items():
        timetable[hour][day] = ','.join(used_classes)

    # Write the timetable data to the CSV file
    with open('schedule.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hour', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

        for hour, classes_per_hour in enumerate(timetable):
            writer.writerow([hour] + classes_per_hour)

    print("Schedule saved as 'schedule.csv'.")


def crawl_and_update(class_number):
    print(f"Scraping data for class number {class_number}...")
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(SchoolSpider, classNumber=class_number)
        process.start(stop_after_crawl=True)
    except Exception as e:
        print(f"Error occurred during scraping: {e}")
        return

def main():
    global schedule
    
    number_of_classes = 50
    #number_of_classes = 40

    processes = []
    for i in range(1, number_of_classes+1):
        p = Process(target=crawl_and_update, args=(i,))
        p.start()
        processes.append(p)
        p.join()


    # After all processes completed, add data to CSV
    for i in range(1, number_of_classes+1):  
        add_room_schedule_to_list(f'htmls\\class{i}.html')

    add_to_csv()
    print("All processes completed.")
    print("Schedule saved as 'schedule.csv'.")

if __name__ == "__main__":
    main()
