# 🏀 NBA Player Stats Web Scraper

This Python script scrapes statistical data for NBA players Michael Jordan and LeBron James from the Basketball Reference website and stores the data in separate SQLite databases for each player.

## 📋 Prerequisites

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- seleniumbase
- pandas
- sqlite3

You can install the required packages using pip:

```bash
pip install seleniumbase pandas
```
# 🚀 Usage
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

## 📊 Output

The script will display the following information during execution:

- The player being processed
- The number of tables found on each player's page
- The table number, ID, and title being processed
- Confirmation when a table's data is saved to the database
- Notification if a missing table is created in one of the databases

## 📝 Notes

- The script uses Selenium with Chrome in incognito mode to scrape the data. Make sure you have Chrome installed on your system.
- The script assumes that the tables of interest are within the range of 21 to 39 on each player's page. If the table structure changes on the Basketball Reference website, you may need to adjust the range accordingly.
- If a table title element is not found or an exception occurs, the script will use a default title in the format "Table X" or "Playoffs Table X".
- The script creates separate SQLite databases for each player to store their respective data.
- If a table exists in one player's database but not the other, the script will create the missing table in the other database using the available data.
