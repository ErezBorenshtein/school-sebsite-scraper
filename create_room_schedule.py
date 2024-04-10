"""import re
from bs4 import BeautifulSoup
import pandas as pd

def extract_room_schedule(html_file, output_csv):
    # Read HTML code from the file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_code = file.read()

    # Parse the HTML code
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find all table rows
    rows = soup.find_all('tr')

    # Initialize an empty list to store schedule data
    schedule_data = []

    # Find the maximum number of rows and columns (days in a week and lesson numbers)
    max_columns = 0
    max_rows = len(rows)

    # Loop through each row to find the maximum number of columns
    for row in rows:
        # Find all cells in the row
        cells = row.find_all('td', class_='TTCell')
        
        # Count the number of cells in the row
        num_cells = len(cells)
        
        # Update max_columns if necessary
        if num_cells > max_columns:
            max_columns = num_cells

    # Loop through each row again to extract data
    for i, row in enumerate(rows):
        # Initialize a list to store data for each day
        day_data = [''] * max_columns
        
        # Find all cells in the row
        cells = row.find_all('td', class_='TTCell')
        
        # Loop through each cell in the row
        for j, cell in enumerate(cells):
            # Find all lesson divs in the cell
            lessons = cell.find_all('div', class_='TTLesson')
            
            # Extract room numbers from lesson information and append to day_data
            room_numbers = []
            for lesson in lessons:
                lesson_text = lesson.get_text().strip()
                room_matches = re.findall(r'\d{3}', lesson_text)  # Extract 3-digit numbers (room numbers)
                room_numbers.extend(room_matches)
            
            day_data[j] = ','.join(room_numbers)  # Combine room numbers into a comma-separated string
        
        # Append day_data to schedule_data
        schedule_data.append(day_data)

    # Create column names for the DataFrame
    columns = [f'Lesson_{i+1}' for i in range(max_columns)]

    # Create a DataFrame from schedule_data
    df = pd.DataFrame(schedule_data, columns=columns)

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)

    print(f"Schedule saved to {output_csv}")

# Usage
extract_room_schedule('school.html', 'rooms_schedule.csv')"""

import re
import pandas as pd
from bs4 import BeautifulSoup

def add_room_schedule_to_csv(html_file, output_csv):
    print("Reading HTML file...")
    # Read HTML code from the file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_code = file.read()

    print("Parsing HTML...")
    # Parse the HTML code
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find all table rows
    rows = soup.find_all('tr')

    # Initialize an empty list to store schedule data
    schedule_data = []

    # Find the maximum number of rows and columns (days in a week and lesson numbers)
    max_columns = 0
    max_rows = len(rows)

    # Loop through each row to find the maximum number of columns
    for row in rows:
        # Find all cells in the row
        cells = row.find_all('td', class_='TTCell')
        
        # Count the number of cells in the row
        num_cells = len(cells)
        
        # Update max_columns if necessary
        if num_cells > max_columns:
            max_columns = num_cells

    # Loop through each row again to extract data
    for i, row in enumerate(rows):
        # Initialize a list to store data for each day
        day_data = [''] * max_columns
        
        # Find all cells in the row
        cells = row.find_all('td', class_='TTCell')
        
        # Loop through each cell in the row
        for j, cell in enumerate(cells):
            # Find all lesson divs in the cell
            lessons = cell.find_all('div', class_='TTLesson')
            
            # Extract room numbers from lesson information and append to day_data
            room_numbers = []
            for lesson in lessons:
                lesson_text = lesson.get_text().strip()
                room_matches = re.findall(r'\d{3}', lesson_text)  # Extract 3-digit numbers (room numbers)
                room_numbers.extend(room_matches)
            
            day_data[j] = ','.join(room_numbers)  # Combine room numbers into a comma-separated string
        
        # Append day_data to schedule_data
        schedule_data.append(day_data)

    # Create column names for the DataFrame
    columns = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Create a DataFrame from schedule_data
    new_df = pd.DataFrame(schedule_data, columns=columns)

    print("Checking existing CSV file...")
    # Read existing CSV file, if it exists
    try:
        existing_df = pd.read_csv(output_csv)
        print("Existing CSV file found.")
    except FileNotFoundError:
        existing_df = pd.DataFrame(index=range(1, max_rows+1), columns=columns)
        print("Existing CSV file not found.")

    # Merge new data with existing DataFrame based on index (lesson hours)
    merged_df = existing_df.combine_first(new_df)

    # Reorder columns
    merged_df = merged_df[columns]

    # Save the DataFrame to a CSV file
    merged_df.to_csv(output_csv, index=False)

    print(f"Schedule appended to {output_csv}")

if __name__ == "__main__":
    add_room_schedule_to_csv('school.html', 'schedule_template.csv')

