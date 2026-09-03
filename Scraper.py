import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.timeanddate.com/weather/?low=c")
time.sleep(3) 

# Find the table by its specific classes
table = driver.find_element(By.CSS_SELECTOR, "table.zebra.fw.tb-theme")
rows = table.find_elements(By.TAG_NAME, "tr")

weather_data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    
    # The table has 8 columns (4 for the first city, 4 for the second)
    # We loop in steps of 4 to extract both cities from one row
    for i in range(0, len(cells), 4):
        try:
            city_name = cells[i].text.strip()
            local_time = cells[i+1].text.strip()
            
            # Extract weather description from the img 'title' attribute
            try:
                weather_img = cells[i+2].find_element(By.TAG_NAME, "img")
                weather_desc = weather_img.get_attribute("title")
            except:
                weather_desc = "N/A"
                
            temp = cells[i+3].text.strip()

            if city_name:  # Ensure we don't add empty rows
                weather_data.append({
                    "City": city_name,
                    "Local Time": local_time,
                    "Condition": weather_desc,
                    "Temperature": temp
                })
        except IndexError:
            continue

driver.quit()


# Save raw data
os.makedirs('data', exist_ok=True)
with open('data/raw_weather.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['City', 'Local Time', 'Temperature', 'Condition'])
    writer.writeheader()
    writer.writerows(weather_data)

# Preview first few records
if weather_data:
    print("Sample data:")
    for i, record in enumerate(weather_data[:5]):
        print(f"{i+1}. {record}")
