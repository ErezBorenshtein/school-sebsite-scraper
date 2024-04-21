School Schedule Scraper & Discord Bot

Description:
This project is designed to scrape my school schedule using Scrapy, a web crawling and web scraping framework in Python, and utilizes a Discord bot to display empty rooms for each hour. By integrating Scrapy with a Discord bot, this tool provides a convenient way to visualize and access room availability throughout your school day.

Schedule Scraping: The Scrapy framework is employed to extract schedule information from my school's website.
Room Availability: The Discord bot analyzes the scraped data to identify empty rooms for each hour of the school day.
Real-time Updates: The bot provides real-time updates on room availability, ensuring accurate and up-to-date information.
Requirements:
Python 3.x
Discord bot & server to add it to

Installation:
Clone this repository to your local machine.
Install the required dependencies using pip:
pip install -r requirements.txt

Change the token from the file token.txt.
Once the bot is running and connected to your Discord server, you can interact with it using commands. Here are some example commands:

!help: show all of the commands
!empty classes [day] [hour]: Displays the empty rooms for a specific day hour.
!empty rooms today [hour]: Displays the empty rooms for today in a specific hour.
!empty rooms: Displays the empty rooms for today in the closest(next) hour

Contributing:
Contributions are welcome! If you find any issues or have ideas for improvements.

Disclaimer:
This project works only on my school's website.
