import bs4
import pandas as pd
import re
from get_room_schedule import extract_room_schedule

# Read the HTML file
html_file = "school.html"
with open(html_file, 'r', encoding='utf-8') as file:
    html_code = file.read()
