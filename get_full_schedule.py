from bs4 import BeautifulSoup
import pandas as pd

# Read HTML code from the file
with open('school.html', 'r', encoding='utf-8') as file:
    html_code = file.read()

# Parse the HTML code
soup = BeautifulSoup(html_code, 'html.parser')

# Find all table rows
rows = soup.find_all('tr')

# Initialize an empty list to store schedule data
schedule_data = []

# Find the maximum number of columns (days in a week)
max_columns = 0

# Loop through each row
for row in rows:
    # Find all cells in the row
    cells = row.find_all('td', class_='TTCell')
    
    # Count the number of cells in the row
    num_cells = len(cells)
    
    # Update max_columns if necessary
    if num_cells > max_columns:
        max_columns = num_cells

# Loop through each row again to extract data
for row in rows:
    # Initialize a list to store data for each day
    day_data = [''] * max_columns
    
    # Find all cells in the row
    cells = row.find_all('td', class_='TTCell')
    
    # Loop through each cell in the row
    for i, cell in enumerate(cells):
        # Find all lesson divs in the cell
        lessons = cell.find_all('div', class_='TTLesson')
        
        # Extract lesson information and append to day_data
        lessons_text = [lesson.get_text().strip() for lesson in lessons]
        day_data[i] = '\n'.join(lessons_text)
    
    # Append day_data to schedule_data
    schedule_data.append(day_data)

# Create column names for the DataFrame
columns = [f'Day_{i+1}' for i in range(max_columns)]

# Create a DataFrame from schedule_data
df = pd.DataFrame(schedule_data, columns=columns)

# Save the DataFrame to a CSV file
df.to_csv('schedule.csv', index=False)

print("Schedule saved to schedule.csv")