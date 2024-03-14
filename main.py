from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import sqlite3
from io import StringIO

urls = {
    "Michael Jordan": "https://www.basketball-reference.com/players/j/jordami01.html",
    "LeBron James": "https://www.basketball-reference.com/players/j/jamesle01.html"
}

# Create connections to the SQLite databases (they will be created if they don't exist)
conn_mj = sqlite3.connect("michael_jordan_stats.db")
conn_lj = sqlite3.connect("lebron_james_stats.db")

all_table_ids = set()

for player, url in urls.items():
    print(f"Processing {player}...")

    driver = Driver(uc=True, incognito=True)
    driver.get(url)

    # Find all the tables on the page
    tables = driver.find_elements(By.TAG_NAME, "table")

    # Print the number of tables found
    print(f"Number of tables found: {len(tables)}")

    # Extract data from each table within the desired range and save it to the database
    for i, table in enumerate(tables, start=1):
        if 21 <= i <= 39:
            table_id = table.get_attribute("id")
            all_table_ids.add(table_id)

            try:
                if table_id.startswith("playoffs_"):
                    # If the table ID starts with "playoffs_", find the corresponding non-playoff table title
                    non_playoff_table_id = table_id.replace("playoffs_", "")
                    title_element = driver.find_element(By.XPATH, f"//*[@id='{non_playoff_table_id}_sh']/h2")
                    table_title = "Playoffs " + title_element.text.strip()
                else:
                    title_element = driver.find_element(By.XPATH, f"//*[@id='{table_id}_sh']/h2")
                    table_title = title_element.text.strip()
            except NoSuchElementException:
                # If the title element is not found or an exception occurs, use a default title
                if table_id.startswith("playoffs_"):
                    table_title = f"Playoffs Table {i}"
                else:
                    table_title = f"Table {i}"

            if table_id:
                print(f"Processing Table {i}: {table_title}")

                # Extract data from the table using pandas
                table_html = table.get_attribute("outerHTML")
                table_html_io = StringIO(table_html)
                df = pd.read_html(table_html_io)[0]

                # Save the data to the respective SQLite database
                table_name = f"table_{i}_{table_id}"
                if player == "Michael Jordan":
                    df.to_sql(table_name, conn_mj, if_exists="replace", index=False)
                else:
                    df.to_sql(table_name, conn_lj, if_exists="replace", index=False)

                print(f"Table {i} data saved to the database.")
                print()

    driver.quit()

# Ensure both databases have all the tables
for table_id in all_table_ids:
    table_name = f"table_{table_id}"
    
    # Check if the table exists in Michael Jordan's database
    mj_table_exists = not pd.read_sql_query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'", conn_mj).empty
    
    # Check if the table exists in LeBron James' database
    lj_table_exists = not pd.read_sql_query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'", conn_lj).empty
    
    if mj_table_exists and not lj_table_exists:
        # Table exists in Michael Jordan's database but not in LeBron James' database
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn_mj)
        df.to_sql(table_name, conn_lj, if_exists="replace", index=False)
        print(f"Created table {table_name} in LeBron James' database.")
    elif lj_table_exists and not mj_table_exists:
        # Table exists in LeBron James' database but not in Michael Jordan's database
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn_lj)
        df.to_sql(table_name, conn_mj, if_exists="replace", index=False)
        print(f"Created table {table_name} in Michael Jordan's database.")

# Close the database connections
conn_mj.close()
conn_lj.close()