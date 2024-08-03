from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime, timedelta

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the webpage
driver.get("https://news.metal.com/list/industry/aluminium")

# Function to load all news by clicking the "Load More" button until no more articles are available
def load_all_news(driver):
    while True:
        try:
            # Find the "Load More" button
            load_more_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".footer___PvIjk"))
            )
            print("Found 'Load More' button. Attempting to click...")
            # Scroll the button into view and click it using JavaScript
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Clicked 'Load More' button.")
            # Wait for the new content to load
            time.sleep(5)
        except Exception as e:
            print(f"No more articles or an error occurred: {e}")
            break

# Load all news articles
load_all_news(driver)

# Extract the news articles
titles = driver.find_elements(By.CSS_SELECTOR, ".title___1baLV")
summaries = driver.find_elements(By.CSS_SELECTOR, ".description__z7ktb.descriptionspec__lj3uG")
dates = driver.find_elements(By.CSS_SELECTOR, ".date___3dzkE")

# Print the lengths of the lists for debugging
print(f"Number of titles: {len(titles)}")
print(f"Number of summaries: {len(summaries)}")
print(f"Number of dates: {len(dates)}")

if not titles or not dates:
    print("No articles found.")
    driver.quit()
    exit()

# Use today's date as the start date
start_date = datetime.now()
end_date = start_date - timedelta(days=45)

# Print the date range
print(f"Starting Date: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"End Date (45 days back): {end_date.strftime('%Y-%m-%d %H:%M:%S')}")

# Prepare the data for CSV
news_data = []

for i in range(len(titles)):
    title = titles[i].text
    summary = summaries[i].text if i < len(summaries) else "No summary"
    date_str = dates[i].text
    
    # Print raw date string for debugging
    print(f"Raw date string for index {i}: '{date_str}'")

    try:
        # Parse date string into datetime object
        article_date = datetime.strptime(date_str, "%b %d, %Y %H:%M")  # Adjust format if needed
        
        # Check if the article date is within the specified range
        if end_date <= article_date <= start_date:
            news_data.append([title, summary, article_date.strftime("%Y-%m-%d %H:%M:%S")])
            print(f"Title: {title}, Date: {article_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"Article date {article_date} is out of range.")
    except ValueError:
        # Handle date parsing error if the date format is different
        print(f"Date format error for article: {title} with date string: '{date_str}'")

# Save the data to a CSV file
csv_file = "news_data.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Summary", "Date"])
    writer.writerows(news_data)

print(f"Data saved to {csv_file}")

# Close the driver
driver.quit()