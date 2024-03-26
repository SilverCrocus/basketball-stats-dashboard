# 🏀 NBA Player Stats Web Scraper and Dashboard

This project consists of two main components:
1. A Python script that scrapes statistical data for NBA players Michael Jordan and LeBron James from the Basketball Reference website and stores the data in separate SQLite databases for each player.
2. An interactive dashboard built with Streamlit that allows users to visualize and compare the statistical data of Michael Jordan and LeBron James.

## 📋 Prerequisites

Before running the script and the dashboard, ensure you have the following dependencies installed:

- Python 3.x
- seleniumbase
- pandas
- sqlite3
- streamlit
- plotly

You can install the required packages using pip:

'''bash
pip install seleniumbase pandas streamlit plotly
'''

## 🚀 Usage

### Web Scraper
1. Clone the repository or download the `main.py` file.

2. Open the `main.py` file in a text editor.

3. In the `urls` dictionary, you can modify the URLs for the players you want to scrape data for. By default, the script is set to scrape data for Michael Jordan and LeBron James.

4. Run the script using the following command:

   ```bash
   python main.py
   ```

5. The script will launch a browser using Selenium and navigate to the specified URLs for each player.

6. It will find all the tables on each player's page and extract data from tables within the desired range (tables 21 to 39).

7. The extracted data will be saved to separate SQLite databases for each player:
   - `michael_jordan_stats.db` for Michael Jordan
   - `lebron_james_stats.db` for LeBron James

8. The script will ensure that both databases have all the tables by checking if a table exists in one database but not the other. If a table is missing in one database, it will be created using the data from the other database.

9. Once the script finishes executing, you will have two SQLite databases containing the scraped statistical data for each player.

### Interactive Dashboard
1. After running the web scraper and obtaining the SQLite databases, navigate to the directory containing the `dashboard.py` file.

2. Run the following command to start the Streamlit dashboard:

   ```bash
   streamlit run src/app.py
   ```

3. The dashboard will open in your default web browser.

4. Use the dropdown menus to select the desired table, x-axis variable, graph type (Line, Bar, Scatter), and variables to plot.

5. The dashboard will dynamically generate graphs based on your selections, allowing you to visualize and compare the statistical data of Michael Jordan and LeBron James.

6. Interact with the graphs, explore different combinations of variables, and gain insights into the players' performance throughout their careers.

## 📊 Output

### Web Scraper
The script will display the following information during execution:

- The player being processed
- The number of tables found on each player's page
- The table number, ID, and title being processed
- Confirmation when a table's data is saved to the database
- Notification if a missing table is created in one of the databases

### Interactive Dashboard
The dashboard provides an intuitive interface to visualize and compare the statistical data of Michael Jordan and LeBron James. Users can select different tables, variables, and graph types to customize the data visualization according to their preferences.

## 📝 Notes

- The web scraper uses Selenium with Chrome in incognito mode to scrape the data. Make sure you have Chrome installed on your system.
- The web scraper assumes that the tables of interest are within the range of 21 to 39 on each player's page. If the table structure changes on the Basketball Reference website, you may need to adjust the range accordingly.
- If a table title element is not found or an exception occurs during web scraping, the script will use a default title in the format "Table X" or "Playoffs Table X".
- The web scraper creates separate SQLite databases for each player to store their respective data.
- If a table exists in one player's database but not the other, the web scraper will create the missing table in the other database using the available data.
- The interactive dashboard uses relative file paths to locate the SQLite databases. Make sure the directory structure is maintained as expected.
